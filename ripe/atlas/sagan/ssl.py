# Copyright (c) 2016 RIPE NCC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pytz
import codecs

from datetime import datetime

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.backends import openssl
    from cryptography.hazmat.primitives import hashes
except ImportError:
    logging.warning(
        "cryptography module is not installed, without it you cannot parse SSL "
        "certificate measurement results"
    )

from .base import Result, ParsingDict
from .helpers.compatibility import string


EXT_SAN = "subjectAltName"


class Certificate(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.subject_cn = None
        self.subject_o = None
        self.subject_c = None
        self.issuer_cn = None
        self.issuer_o = None
        self.issuer_c = None

        self.valid_from = None
        self.valid_until = None

        self.checksum_md5 = None
        self.checksum_sha1 = None
        self.checksum_sha256 = None

        self.has_expired = None

        self.extensions = {}

        cert = x509.load_pem_x509_certificate(data.encode("ascii"), openssl.backend)

        if cert:
            self.checksum_md5 = self._colonify(cert.fingerprint(hashes.MD5()))
            self.checksum_sha1 = self._colonify(cert.fingerprint(hashes.SHA1()))
            self.checksum_sha256 = self._colonify(cert.fingerprint(hashes.SHA256()))

            self.valid_from = pytz.utc.localize(cert.not_valid_before)
            self.valid_until = pytz.utc.localize(cert.not_valid_after)

            self.has_expired = self._has_expired()

            self._add_extensions(cert)

        if cert and cert.subject:
            self.subject_cn, self.subject_o, self.subject_c = \
                self._parse_x509_name(cert.subject)

        if cert and cert.issuer:
            self.issuer_cn, self.issuer_o, self.issuer_c = \
                self._parse_x509_name(cert.issuer)

    # OID name lookup of the common abbreviations
    # In reality probably only CN will be used
    _oid_names = {
        NameOID.COMMON_NAME: "CN",
        NameOID.ORGANIZATION_NAME: "O",
        NameOID.ORGANIZATIONAL_UNIT_NAME: "OU",
        NameOID.COUNTRY_NAME: "C",
        NameOID.STATE_OR_PROVINCE_NAME: "S",
        NameOID.LOCALITY_NAME: "L",
    }

    def _get_oid_name(self, oid):
        return self._oid_names.get(oid, oid.dotted_string)

    def _name_attribute_to_string(self, name):
        """
        Build a /-separated string from an x509.Name.
        """
        return "".join(
            "/{}={}".format(
                self._get_oid_name(attr.oid),
                attr.value,
            )
            for attr in name
        )

    def _get_subject_alternative_names(self, ext):
        """
        Return a list of Subject Alternative Name values for the given x509
        extension object.
        """
        values = []
        for san in ext.value:
            if isinstance(san.value, string):
                # Pass on simple string SAN values
                values.append(san.value)
            elif isinstance(san.value, x509.Name):
                # In theory there there could be >1 RDN here...
                values.extend(
                    self._name_attribute_to_string(rdn) for rdn in san.value.rdns
                )
        return values

    def _add_extensions(self, cert):
        for ext in cert.extensions:
            if ext.oid._name == EXT_SAN:
                self.extensions[EXT_SAN] = self._get_subject_alternative_names(ext)

    @staticmethod
    def _colonify(bytes):
        hex = codecs.getencoder("hex_codec")(bytes)[0].decode("ascii").upper()
        return ":".join(a+b for a, b in zip(hex[::2], hex[1::2]))

    @staticmethod
    def _parse_x509_name(name):
        cn = None
        o = None
        c = None
        for attr in name:
            if attr.oid == NameOID.COUNTRY_NAME:
                c = attr.value
            elif attr.oid == NameOID.ORGANIZATION_NAME:
                o = attr.value
            elif attr.oid == NameOID.COMMON_NAME:
                cn = attr.value
        return cn, o, c

    def _has_expired(self):
        now = pytz.utc.localize(datetime.utcnow())
        return self.valid_from <= now <= self.valid_until

    @property
    def cn(self):
        return self.subject_cn

    @property
    def o(self):
        return self.subject_o

    @property
    def c(self):
        return self.subject_c

    @property
    def common_name(self):
        return self.cn

    @property
    def organisation(self):
        return self.o

    @property
    def country(self):
        return self.c

    @property
    def checksum(self):
        return self.checksum_sha256


class Alert(ParsingDict):

    # Taken from https://tools.ietf.org/html/rfc5246#section-7.2
    DESCRIPTION_MAP = {
        0: "close_notify",
        10: "unexpected_message",
        20: "bad_record_mac",
        21: "decryption_failed_RESERVED",
        22: "record_overflow",
        30: "decompression_failure",
        40: "handshake_failure",
        41: "no_certificate_RESERVED",
        42: "bad_certificate",
        43: "unsupported_certificate",
        44: "certificate_revoked",
        45: "certificate_expired",
        46: "certificate_unknown",
        47: "illegal_parameter",
        48: "unknown_ca",
        49: "access_denied",
        50: "decode_error",
        51: "decrypt_error",
        60: "export_restriction_RESERVED",
        70: "protocol_version",
        71: "insufficient_security",
        80: "internal_error",
        90: "user_canceled",
        100: "no_renegotiation",
        110: "unsupported_extension",
    }

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data

        self.level = self.ensure("level", int)
        self.description = self.ensure("decription", int)
        if self.description is None:
            self.description = self.ensure("description", int)

    @property
    def description_string(self):
        return self.DESCRIPTION_MAP.get(self.description, "Unknown")


class SslResult(Result):

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.af = self.ensure("af", int)
        self.destination_address = self.ensure("dst_addr", str)
        self.destination_name = self.ensure("dst_name", str)
        self.source_address = self.ensure("src_addr", str)
        self.port = self.ensure("dst_port", int)
        self.method = self.ensure("method", str)
        self.version = self.ensure("ver", str)
        self.response_time = self.ensure("rt", float)
        self.time_to_connect = self.ensure("ttc", float)

        if "error" in self.raw_data:
            self._handle_error(self.raw_data["error"])

        # Older versions used named ports
        if self.port is None and self.raw_data.get("dst_port") == "https":
            self.port = 443

        self.alert = None
        self.certificates = []
        self.is_self_signed = False

        if "alert" in self.raw_data:
            self.alert = Alert(self.raw_data["alert"], **kwargs)
            self._handle_error(self.alert.description_string)

        if "cert" in self.raw_data and isinstance(self.raw_data["cert"], list):

            for certificate in self.raw_data["cert"]:
                self.certificates.append(Certificate(certificate, **kwargs))

            if len(self.raw_data["cert"]) == 1:
                certificate = self.certificates[0]
                if certificate.subject_cn == certificate.issuer_cn:
                    self.is_self_signed = True

    @property
    def checksum_chain(self):
        """
        Returns a list of checksums joined with "::".
        """

        checksums = []
        for certificate in self.certificates:
            checksums.append(certificate.checksum)

        return "::".join(checksums)


__all__ = (
    "SslResult"
)

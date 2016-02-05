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
import re

from datetime import datetime
from dateutil.relativedelta import relativedelta

try:
    import OpenSSL
except ImportError:
    logging.warning(
        "pyOpenSSL is not installed, without it you cannot parse SSL "
        "certificate measurement results"
    )

from .base import Result, ResultParseError, ParsingDict


class Certificate(ParsingDict):

    TIME_FORMAT = "%Y%m%d%H%M%SZ"
    TIME_REGEX = re.compile(
        "(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\+|\-)(\d\d)(\d\d)"
    )

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

        # Clean up the certificate data and use OpenSSL to parse it
        x509 = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM,
            data.replace("\\/", "/").replace("\n\n", "\n")
        )
        subject = dict(x509.get_subject().get_components())
        issuer = dict(x509.get_issuer().get_components())

        if x509 and subject and issuer:

            self.subject_cn = self._string_from_dict_or_none(subject, b"CN")
            self.subject_o = self._string_from_dict_or_none(subject, b"O")
            self.subject_c = self._string_from_dict_or_none(subject, b"C")
            self.issuer_cn = self._string_from_dict_or_none(issuer, b"CN")
            self.issuer_o = self._string_from_dict_or_none(issuer, b"O")
            self.issuer_c = self._string_from_dict_or_none(issuer, b"C")

            self.checksum_md5 = x509.digest("md5").decode()
            self.checksum_sha1 = x509.digest("sha1").decode()
            self.checksum_sha256 = x509.digest("sha256").decode()

            self.has_expired = bool(x509.has_expired())

            self.valid_from = None
            self.valid_until = None
            self._process_validation_times(x509)

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

    def _process_validation_times(self, x509):
        """
        PyOpenSSL uses a kooky date format that *usually* parses out quite
        easily but on the off chance that it's not in UTC, a lot of work needs
        to be done.
        """

        valid_from = x509.get_notBefore()
        valid_until = x509.get_notAfter()

        try:
            self.valid_from = pytz.UTC.localize(datetime.strptime(
                valid_from.decode(),
                self.TIME_FORMAT
            ))
        except ValueError:
            self.valid_from = self._process_nonstandard_time(valid_from)

        try:
            self.valid_until = pytz.UTC.localize(datetime.strptime(
                valid_until.decode(),
                self.TIME_FORMAT
            ))
        except ValueError:
            self.valid_until = self._process_nonstandard_time(valid_until)

    def _process_nonstandard_time(self, string):
        """
        In addition to `YYYYMMDDhhmmssZ`, PyOpenSSL can also use timestamps
        in `YYYYMMDDhhmmss+hhmm` or `YYYYMMDDhhmmss-hhmm`.
        """

        match = re.match(self.TIME_REGEX, string)

        if not match:
            raise ResultParseError(
                "Unrecognised time format: {s}".format(s=string)
            )

        r = datetime(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
            int(match.group(6)),
            0,
            pytz.UTC
        )
        delta = relativedelta(
            hours=int(match.group(8)),
            minutes=int(match.group(9))
        )
        if match.group(7) == "-":
            return r - delta
        return r + delta

    @staticmethod
    def _string_from_dict_or_none(dictionary, key):
        """
        Created to make nice with the Python3 problem.
        """
        if key not in dictionary:
            return None
        return dictionary[key].decode("UTF-8")


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

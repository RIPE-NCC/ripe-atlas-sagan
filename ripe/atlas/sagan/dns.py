from __future__ import absolute_import

import base64

from .base import Result, ValidationMixin
from .helpers.abuf import AbufParser

class Header(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data    = data
        self.aa          = self.ensure("AA",         bool)
        self.qr          = self.ensure("QR",         bool)
        self.nscount     = self.ensure("NSCOUNT",    int)
        self.qdcount     = self.ensure("QDCOUNT",    int)
        self.ancount     = self.ensure("ANCOUNT",    int)
        self.tc          = self.ensure("TC",         bool)
        self.rd          = self.ensure("RD",         bool)
        self.arcount     = self.ensure("ARCOUNT",    int)
        self.return_code = self.ensure("ReturnCode", str)
        self.opcode      = self.ensure("OpCode",     str)
        self.ra          = self.ensure("RA",         bool)
        self.z           = self.ensure("Z",          int)
        self.ad          = self.ensure("AD",         bool)
        self.cd          = self.ensure("CD",         bool)
        self.id          = self.ensure("ID",         int)

    def __str__(self):
        return "Header: " + self.return_code

    @property
    def is_authoritative(self):
        return self.aa

    @property
    def is_query(self):
        if self.qr is None:
            return None
        return not self.qr

    @property
    def nameserver_count(self):
        return self.nscount

    @property
    def question_count(self):
        return self.qdcount

    @property
    def answer_count(self):
        return self.ancount

    @property
    def is_truncated(self):
        return self.tc

    @property
    def recursion_desired(self):
        return self.rd

    @property
    def additional_count(self):
        return self.arcount

    @property
    def recursion_available(self):
        return self.ra

    @property
    def zero(self):
        return self.z

    @property
    def checking_disabled(self):
        return self.cd

    @property
    def authenticated_data(self):
        return self.aa


class Option(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data = data
        self.nsid   = self.ensure("NSID",         str)
        self.code   = self.ensure("OptionCode",   int)
        self.length = self.ensure("OptionLength", int)
        self.name   = self.ensure("OptionName",   str)


class Edns0(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data = data
        self.extended_return_code = self.ensure("ExtendedReturnCode", int)
        self.name                 = self.ensure("Name",               str)
        self.type                 = self.ensure("Type",               str)
        self.udp_size             = self.ensure("UDPsize",            int)
        self.version              = self.ensure("Version",            int)
        self.z                    = self.ensure("Z",                  int)

        self.options = []
        if "Option" in self.raw_data:
            if isinstance(self.raw_data["Option"], list):
                for option in self.raw_data["Option"]:
                    self.options.append(Option(option))


class Question(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data = data
        self.klass    = self.ensure("Qclass", str)
        self.type     = self.ensure("Qtype",  str)
        self.name     = self.ensure("Qname",  str)


class Answer(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data  = data
        self.name      = self.ensure("Name",     str)
        self.ttl       = self.ensure("TTL",      int)
        self.type      = self.ensure("Type",     str)
        self.klass     = self.ensure("Class",    str)
        self.rd_length = self.ensure("RDlength", int)

    @property
    def resource_data_length(self):
        return self.rd_length


class AAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.address = self.ensure("Address", str)


class AaaaAnswer(AAnswer):
    pass


class NsAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.target = self.ensure("Target", str)


class CnameAnswer(NsAnswer):
    pass


class MxAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.preference     = self.ensure("Preference",    int)
        self.mail_exchanger = self.ensure("MailExchanger", str)


class SoaAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.mname    = self.ensure("MasterServerName", str)
        self.rname    = self.ensure("MaintainerName",   str)
        self.serial   = self.ensure("Serial",           int)
        self.refresh  = self.ensure("Refresh",          int)
        self.retry    = self.ensure("Retry",            int)
        self.expire   = self.ensure("Expire",           int)
        self.minimum  = self.ensure("NegativeTtl",      int)

    @property
    def master_server_name(self):
        return self.mname

    @property
    def maintainer_name(self):
        return self.rname

    @property
    def negative_ttl(self):
        return self.minimum

    @property
    def nxdomain(self):
        return self.minimum


class DsAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.tag            = self.ensure("Tag",           int)
        self.algorithm      = self.ensure("Algorithm",     int)
        self.digest_type    = self.ensure("DigestType",    int)
        self.delegation_key = self.ensure("DelegationKey", str)


class DnskeyAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.flags       = self.ensure("Flags",     int)
        self.algorithm   = self.ensure("Algorithm", int)
        self.protocol    = self.ensure("Protocol",  int)
        self.key         = self.ensure("Key",       str)


class TxtAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.data = self.ensure("Data", str)


class RRSigAnswer(Answer):
    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.type_covered         = self.ensure("TypeCovered",        str)
        self.algorithm            = self.ensure("Algorithm",          int)
        self.labels               = self.ensure("Labels",             int)
        self.original_ttl         = self.ensure("OriginalTTL",        int)
        self.signature_expiration = self.ensure("SignatureExpiration",int)
        self.signature_inception  = self.ensure("SignatureInception", int)
        self.key_tag              = self.ensure("KeyTag",             int)
        self.signer_name          = self.ensure("SignerName",         str)
        self.signature            = self.ensure("Signature",          str)

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {}".format(
            self.type_covered,
            self.algorithm,
            self.labels,
            self.original_ttl,
            self.signature_expiration,
            self.signature_inception,
            self.key_tag,
            self.signer_name,
            self.signature
        )


class Authority(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data  = data
        self.klass     = self.ensure("Class",    int)
        self.name      = self.ensure("Name",     str)
        self.rd_length = self.ensure("RDlength", int)
        self.ttl       = self.ensure("TTL",      int)
        self.target    = self.ensure("Target",   str)
        self.type      = self.ensure("Type",     str)

    @property
    def resource_data_length(self):
        return self.rd_length


class Additional(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data  = data
        self.address   = self.ensure("Address",  str)
        self.klass     = self.ensure("Class",    str)
        self.name      = self.ensure("Name",     str)
        self.rd_length = self.ensure("RDlength", int)
        self.ttl       = self.ensure("TTL",      int)
        self.type      = self.ensure("Type",     str)

    @property
    def resource_data_length(self):
        return self.rd_length


class Message(ValidationMixin):

    def __init__(self, message, response_data, parse_buf=True, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self._string_representation = message
        self.raw_data = {}

        if parse_buf:
            self._parse_buf(message)
        else:
            self._backfill_raw_data_from_result(response_data)

        self.header = None
        if "HEADER" in self.raw_data:
            self.header = Header(self.raw_data["HEADER"], **kwargs)

        self.edns0       = None
        self.questions   = []
        self.answers     = []
        self.authorities = []
        self.additionals = []

        answer_classes = {
            "A":      AAnswer,
            "AAAA":   AaaaAnswer,
            "NS":     NsAnswer,
            "CNAME":  CnameAnswer,
            "MX":     MxAnswer,
            "SOA":    SoaAnswer,
            "DS":     DsAnswer,
            "DNSKEY": DnskeyAnswer,
            "TXT":    TxtAnswer,
            "RRSIG":  RRSigAnswer,
        }

        if "EDNS0" in self.raw_data:
            self.edns0 = Edns0(self.raw_data["EDNS0"], **kwargs)

        for question in self.raw_data.get("QuestionSection", []):
            self.questions.append(Question(question, **kwargs))

        for answer in self.raw_data.get("AnswerSection", []):
            answer_type = answer.get("Type")
            if answer_type is None:
                self._handle_malformation(
                    "Answer has no parseable Type: {answer}".format(
                        answer=answer
                    )
                )
            answer_class = answer_classes.get(answer_type, Answer)
            self.answers.append(answer_class(answer, **kwargs))

        for authority in self.raw_data.get("AuthoritySection", []):
            self.authorities.append(Authority(authority, **kwargs))

        for additional in self.raw_data.get("AdditionalSection", []):
            self.additionals.append(Additional(additional, **kwargs))

    def __str__(self):
        return self._string_representation

    def __repr__(self):
        return str(self)

    def _parse_buf(self, message):

        try:
            self.raw_data = AbufParser.parse(base64.b64decode(message))
        except Exception as e:
            self.raw_data = {}
            self._handle_malformation(
                "{exception}: Unable to parse buffer: {buffer}".format(
                    exception=e,
                    buffer=self._string_representation
                )
            )
        else:
            if "ERROR" in self.raw_data:
                self._handle_error(self.raw_data["ERROR"])

    def _backfill_raw_data_from_result(self, response_data):

        # Header
        self.raw_data["Header"] = {}
        for key in ("NSCOUNT", "QDCOUNT", "ID", "ARCOUNT", "ANCOUNT"):
            if key in response_data:
                self.raw_data["Header"][key] = response_data[key]

        # Answers
        if "answers" in response_data and response_data["answers"]:
            self.raw_data["AnswerSection"] = []
            # The names used in the result don't align to those used in the abuf parser
            name_map = {
                "TTL":      "TTL",
                "TYPE":     "Type",
                "NAME":     "Name",
                "RDATA":    "Data",
                "MNAME":    "MasterServerName",
                "RNAME":    "MaintainerName",
                "SERIAL":   "Serial",
                "RDLENGTH": "RDlength",
            }
            for answer in response_data["answers"]:
                temporary = {}
                for k, v in name_map.items():
                    if k in answer:
                        temporary[v] = answer[k]
                if temporary:
                    self.raw_data["AnswerSection"].append(temporary)


class Response(ValidationMixin):

    def __init__(self, data, af=None, destination=None, source=None,
                 protocol=None, part_of_set=True, parse_buf=True, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data = data

        self.af                  = self.ensure("af",       int, af)
        self.destination_address = self.ensure("dst_addr", str, destination)
        self.source_address      = self.ensure("src_addr", str, source)
        self.protocol            = self.ensure("proto",    str, protocol)

        self.response_id = None

        # Preparing for lazy stuff
        self._abuf = None
        self._qbuf = None
        self._parse_buf = parse_buf

        try:
            self.response_time = round(float(self.raw_data["result"]["rt"]), 3)
        except KeyError:
            try:
                self.response_time = round(self.ensure("rt", float), 3)
            except TypeError:
                self.response_time = None

        try:
            self.response_size = self.raw_data["result"]["size"]
        except KeyError:
            self.response_size = self.ensure("size", int)

        if part_of_set:
            self.response_id = self.ensure("subid", int)

        if self.protocol and isinstance(self.protocol, str):
            self.protocol = self.clean_protocol(self.protocol)

    @property
    def abuf(self):
        return self._get_buf("a")

    @property
    def qbuf(self):
        return self._get_buf("q")

    def _get_buf(self, prefix):
        """
        Lazy read-only accessor for the (a|q)buf.
        The qbuf Message object is cached for subsequent requests.
        """
        kind = "{prefix}buf".format(prefix=prefix)
        private_name = "_" + kind
        buf = getattr(self, private_name)
        if buf:
            return buf
        try:
            buf_string = self.raw_data["result"][kind]
        except KeyError:
            buf_string = self.ensure(kind, str)
        if buf_string:
            setattr(self, private_name, Message(
                buf_string,
                self.raw_data,
                parse_buf=self._parse_buf,
                on_error=self._on_error,
                on_malformation=self._on_malformation
            ))
        return getattr(self, private_name)


class DnsResult(Result):

    def __init__(self, data, parse_buf=True, **kwargs):
        """
        Note that we're not setting `self.af` here, but rather we have it as a
        property of `Response` as it's possible that one result can contain
        multiple responses, each with either af=4 or af=6.
        """

        Result.__init__(self, data, **kwargs)

        self.responses = []
        self.responses_total = None

        af                  = self.ensure("af",       int)
        protocol            = self.ensure("proto",    str)
        source_address      = self.ensure("src_addr", str)
        destination_address = self.ensure("dst_addr", str)

        if 0 < self.firmware < 4460:
            af = self.ensure("pf", int)

        responses = []
        part_of_set = True
        try:
            responses.append(self.raw_data["result"])
            part_of_set = False
        except KeyError:
            pass  # We must be a resultset
        finally:
            try:
                self.responses_total = int(self.raw_data["result"]["submax"])
            except (KeyError, ValueError):
                pass  # The value wasn't there, not much we can do about it

        try:
            responses += self.raw_data["resultset"]
        except KeyError:
            pass  # self.responses remains the same

        for response in responses:
            self.responses.append(Response(
                response,
                af=af,
                destination=destination_address,
                source=source_address,
                protocol=protocol,
                part_of_set=part_of_set,
                parse_buf=parse_buf,
                **kwargs
            ))

        if "error" in self.raw_data:
            if isinstance(self.raw_data["error"], dict):
                if "timeout" in self.raw_data["error"]:
                    self._handle_error("Timeout: {timeout}".format(
                        timeout=self.raw_data["error"]["timeout"]
                    ))
                elif "getaddrinfo" in self.raw_data["error"]:
                    self._handle_error("Name resolution error: {msg}".format(
                        msg=self.raw_data["error"]["getaddrinfo"]
                    ))
                else:
                    self._handle_error("Unknown error: {msg}".format(
                        msg=self.raw_data["error"]
                    ))
            else:
                self._handle_error("Unknown error: {msg}".format(
                    msg=self.raw_data["error"]
                ))

__all__ = (
    "DnsResult",
)

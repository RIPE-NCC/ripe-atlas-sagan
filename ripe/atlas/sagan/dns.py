from __future__ import absolute_import

import base64
from collections import namedtuple
from datetime import datetime
from pytz import UTC

from .base import Result, ParsingDict
from .helpers import abuf
from .helpers import compatibility


class Header(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.aa = self.ensure("AA", bool)
        self.qr = self.ensure("QR", bool)
        self.nscount = self.ensure("NSCOUNT", int)
        self.qdcount = self.ensure("QDCOUNT", int)
        self.ancount = self.ensure("ANCOUNT", int)
        self.tc = self.ensure("TC", bool)
        self.rd = self.ensure("RD", bool)
        self.arcount = self.ensure("ARCOUNT", int)
        self.return_code = self.ensure("ReturnCode", str)
        self.opcode = self.ensure("OpCode", str)
        self.ra = self.ensure("RA", bool)
        self.z = self.ensure("Z", int)
        self.ad = self.ensure("AD", bool)
        self.cd = self.ensure("CD", bool)
        self.id = self.ensure("ID", int)

    def __str__(self):
        return "Header: " + self.return_code

    @property
    def flags(self):
        flags = namedtuple(
            "Flags", ("qr", "aa", "tc", "rd", "ra", "z", "ad", "cd"))
        return flags(qr=self.qr, aa=self.aa, tc=self.tc, rd=self.rd,
                     ra=self.ra, z=self.z, ad=self.ad, cd=self.cd)

    @property
    def sections(self):
        sections = namedtuple(
            "Sections", ("QDCOUNT", "ANCOUNT", "NSCOUNT", "ARCOUNT"))
        return sections(QDCOUNT=self.qdcount, ANCOUNT=self.ancount,
                        NSCOUNT=self.nscount, ARCOUNT=self.arcount)

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
        """
        Otherwise known as the NSCOUNT or the authority_count.
        """
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


class Option(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.nsid = self.ensure("NSID", str)
        self.code = self.ensure("OptionCode", int)
        self.length = self.ensure("OptionLength", int)
        self.name = self.ensure("OptionName", str)


class Edns0(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.extended_return_code = self.ensure("ExtendedReturnCode", int)
        self.name = self.ensure("Name", str)
        self.type = self.ensure("Type", str)
        self.udp_size = self.ensure("UDPsize", int)
        self.version = self.ensure("Version", int)
        self.z = self.ensure("Z", int)

        self.options = []
        if "Option" in self.raw_data:
            if isinstance(self.raw_data["Option"], list):
                for option in self.raw_data["Option"]:
                    self.options.append(Option(option))


class Question(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.klass = self.ensure("Qclass", str)
        self.type = self.ensure("Qtype", str)
        self.name = self.ensure("Qname", str)

    def __str__(self):
        return ";{:30}  {:<5}  {:5}".format(self.name, self.klass, self.type)


class Answer(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.name = self.ensure("Name", str)
        self.ttl = self.ensure("TTL", int)
        self.type = self.ensure("Type", str)
        self.klass = self.ensure("Class", str)
        self.rd_length = self.ensure("RDlength", int)

    @property
    def resource_data_length(self):
        return self.rd_length

    def __str__(self):
        return "{:22}  {:<7}  {:5}  {:5}".format(
            self.name,
            self.ttl,
            self.klass,
            self.type
        )


class AAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.address = self.ensure("Address", str)

    def __str__(self):
        return "{0}  {1}".format(Answer.__str__(self), self.address)


class AaaaAnswer(AAnswer):
    pass


class NsAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.target = self.ensure("Target", str)

    def __str__(self):
        return "{0}  {1}".format(Answer.__str__(self), self.target)


class CnameAnswer(NsAnswer):
    pass


class MxAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.preference = self.ensure("Preference", int)
        self.mail_exchanger = self.ensure("MailExchanger", str)

    def __str__(self):
        return "{0}  {1} {2}".format(
            Answer.__str__(self),
            self.preference,
            self.mail_exchanger
        )


class SoaAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.mname = self.ensure("MasterServerName", str)
        self.rname = self.ensure("MaintainerName", str)
        self.serial = self.ensure("Serial", int)
        self.refresh = self.ensure("Refresh", int)
        self.retry = self.ensure("Retry", int)
        self.expire = self.ensure("Expire", int)
        self.minimum = self.ensure("NegativeTtl", int)

    def __str__(self):
        return "{0}  {1} {2} {3} {4} {5} {6} {7}".format(
            Answer.__str__(self),
            self.mname,
            self.rname,
            self.serial,
            self.refresh,
            self.retry,
            self.expire,
            self.minimum
        )

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
        self.tag = self.ensure("Tag", int)
        self.algorithm = self.ensure("Algorithm", int)
        self.digest_type = self.ensure("DigestType", int)
        self.delegation_key = self.ensure("DelegationKey", str)

    def __str__(self):
        return "{0}  {1} {2} {3} {4}".format(
            Answer.__str__(self),
            self.tag,
            self.algorithm,
            self.digest_type,
            self.delegation_key
        )


class DnskeyAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.flags = self.ensure("Flags", int)
        self.algorithm = self.ensure("Algorithm", int)
        self.protocol = self.ensure("Protocol", int)
        self.key = self.ensure("Key", str)

    def __str__(self):
        return "{0}  {1} {2} {3} {4}".format(
            Answer.__str__(self),
            self.flags,
            self.algorithm,
            self.protocol,
            self.key
        )


class TxtAnswer(Answer):

    def __init__(self, data, **kwargs):

        Answer.__init__(self, data, **kwargs)

        self.data = []
        if "Data" in self.raw_data:
            if isinstance(self.raw_data["Data"], list):
                self.data = []
                for s in self.raw_data["Data"]:
                    if isinstance(s, compatibility.string):
                        self.data.append(s)

    def __str__(self):
        return "{0}  {1}".format(Answer.__str__(self), self.data_string)

    @property
    def data_string(self):
        return " ".join(self.data)


class RRSigAnswer(Answer):

    def __init__(self, data, **kwargs):
        Answer.__init__(self, data, **kwargs)
        self.type_covered = self.ensure("TypeCovered", str)
        self.algorithm = self.ensure("Algorithm", int)
        self.labels = self.ensure("Labels", int)
        self.original_ttl = self.ensure("OriginalTTL", int)
        self.signature_expiration = self.ensure("SignatureExpiration", int)
        self.signature_inception = self.ensure("SignatureInception", int)
        self.key_tag = self.ensure("KeyTag", int)
        self.signer_name = self.ensure("SignerName", str)
        self.signature = self.ensure("Signature", str)

    def __str__(self):

        formatter = "%Y%m%d%H%M%S"

        expiration = datetime.fromtimestamp(
            self.signature_expiration, tz=UTC).strftime(formatter)

        inception = datetime.fromtimestamp(
            self.signature_inception, tz=UTC).strftime(formatter)

        return "{0}  {1} {2} {3} {4} {5} {6} {7} {8} {9}".format(
            Answer.__str__(self),
            self.type_covered,
            self.algorithm,
            self.labels,
            self.original_ttl,
            expiration,
            inception,
            self.key_tag,
            self.signer_name,
            self.signature
        )


class NsecAnswer(Answer):
    """
    Parsing of these types of answers out of the abuf is not yet supported.
    """

    def __str__(self):
        return "{0}  ---- Not fully supported ----".format(Answer.__str__(self))


class Message(ParsingDict):

    ANSWER_CLASSES = {
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
        "NSEC":   NsecAnswer,
    }

    def __init__(self, message, response_data, parse_buf=True, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self._string_representation = message
        self.raw_data = {}

        if parse_buf:
            self._parse_buf(message)
        else:
            self._backfill_raw_data_from_result(response_data)

        self.header = None
        if "HEADER" in self.raw_data:
            self.header = Header(self.raw_data["HEADER"], **kwargs)

            # This is a tricky one, since you can't know that the response is an
            # error until *after* the abuf is parsed, and it won't be parsed
            # until you attempt to access it.
            code = self.header.return_code
            if not code or code.upper() != "NOERROR":
                self._handle_error('The response did not contain "NOERROR"')

        self.edns0 = None
        self.questions = []
        self.answers = []
        self.authorities = []
        self.additionals = []

        if "EDNS0" in self.raw_data:
            self.edns0 = Edns0(self.raw_data["EDNS0"], **kwargs)

        for question in self.raw_data.get("QuestionSection", []):
            self.questions.append(Question(question, **kwargs))

        for answer in self.raw_data.get("AnswerSection", []):
            self._append_answer(answer, "answers", **kwargs)
        for authority in self.raw_data.get("AuthoritySection", []):
            self._append_answer(authority, "authorities", **kwargs)
        for additional in self.raw_data.get("AdditionalSection", []):
            self._append_answer(additional, "additionals", **kwargs)

    def __str__(self):
        return self._string_representation

    def __repr__(self):
        return str(self)

    def _append_answer(self, answer, section, **kwargs):
        answer_type = answer.get("Type")
        if answer_type is None:
            self._handle_malformation(
                "Answer has no parseable Type: {answer}".format(
                    answer=answer
                )
            )
        answer_class = self.ANSWER_CLASSES.get(answer_type, Answer)
        getattr(self, section).append(answer_class(answer, **kwargs))

    def _parse_buf(self, message):

        try:
            self.raw_data = abuf.AbufParser.parse(base64.b64decode(message))
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

            # The names used in the result don't align to those used in the abuf
            # parser
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

            self.raw_data["AnswerSection"] = []
            for answer in response_data["answers"]:

                temporary = {}

                for k, v in name_map.items():
                    if k in answer:
                        temporary[v] = answer[k]

                # Special case where some older txt entires are strings and not
                # a list
                if temporary.get("Type") == "TXT":
                    if isinstance(temporary.get("Data"), compatibility.string):
                        temporary["Data"] = [temporary["Data"]]

                if temporary:
                    self.raw_data["AnswerSection"].append(temporary)


class Response(ParsingDict):

    def __init__(self, data, af=None, destination=None, source=None,
                 protocol=None, part_of_set=True, parse_buf=True, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data

        self.af = self.ensure("af", int, af)
        self.destination_address = self.ensure("dst_addr", str, destination)
        self.source_address = self.ensure("src_addr", str, source)
        self.protocol = self.ensure("proto", str, protocol)

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
            message = Message(
                buf_string,
                self.raw_data,
                parse_buf=self._parse_buf,
                on_error=self._on_error,
                on_malformation=self._on_malformation
            )
            if message.is_error:
                self._handle_error(message.error_message)
            setattr(self, private_name, message)
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

        af = self.ensure("af", int)
        protocol = self.ensure("proto", str)
        source_address = self.ensure("src_addr", str)
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

from __future__ import absolute_import

import base64
import logging
import struct

try:
    from dns.opcode import to_text as opcode_to_text
    from dns.rdataclass import to_text as class_to_text
    from dns.rcode import to_text as rcode_to_text
    from dns.rdatatype import to_text as type_to_text
except ImportError:
    logging.warning(
        "dnspython isn't installed, without it you cannot parse DNS "
        "measurement results"
    )

from .base import Result, ValidationMixin
from .helpers.abuf import AbufParser

class Header(ValidationMixin):

    def __init__(self, data):

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


class Option(ValidationMixin):

    def __init__(self, data):

        self.raw_data = data
        self.nsid   = self.ensure("NSID",         str)
        self.code   = self.ensure("OptionCode",   int)
        self.length = self.ensure("OptionLength", int)
        self.name   = self.ensure("OptionName",   str)


class Edns0(ValidationMixin):

    def __init__(self, data):

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

    def __init__(self, data):

        self.raw_data = data
        self.klass    = self.ensure("Qclass", str)
        self.type     = self.ensure("Qtype",  str)
        self.name     = self.ensure("Qname",  str)


class Answer(ValidationMixin):

    def __init__(self, data):

        self.raw_data  = data
        self.name      = self.ensure("Name",     str)
        self.ttl       = self.ensure("TTL",      int)
        self.address   = self.ensure("Address",  str)
        self.type      = self.ensure("Type",     str)
        self.klass     = self.ensure("Class",    str)
        self.rd_length = self.ensure("RDlength", int)

    @property
    def resource_data_length(self):
        return self.rd_length


class Authority(ValidationMixin):

    def __init__(self, data):

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

    def __init__(self, data):

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


class Response(ValidationMixin):

    def __init__(self, data, af=None, destination=None, source=None,
                 protocol=None, part_of_set=True, parse_abuf=True):

        self.raw_data    = data
        self.header      = None
        self.edns0       = None
        self.questions   = []
        self.answers     = []
        self.authorities = []
        self.additionals = []

        self.af                  = self.ensure("af",       int, af)
        self.destination_address = self.ensure("dst_addr", str, destination)
        self.source_address      = self.ensure("src_addr", str, source)
        self.protocol            = self.ensure("proto",    str, protocol)

        try:
            self.abuf = self.raw_data["result"]["abuf"]
        except KeyError:
            self.abuf = self.ensure("abuf", str)

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

        self.response_id = None

        if part_of_set:
            self.response_id = self.ensure("subid", int)

        if self.protocol and isinstance(self.protocol, str):
            self.protocol = self.clean_protocol(self.protocol)

        if self.abuf and parse_abuf:

            parsed_abuf = AbufParser.parse(base64.decodestring(self.abuf))

            self.header = Header(parsed_abuf["HEADER"])

            if "EDNS0" in parsed_abuf:
                self.edns0 = Edns0(parsed_abuf["EDNS0"])

            for question in parsed_abuf.get("QuestionSection", []):
                self.questions.append(Question(question))

            for answer in parsed_abuf.get("AnswerSection", []):
                self.answers.append(Answer(answer))

            for authority in parsed_abuf.get("AuthoritySection", []):
                self.authorities.append(Authority(authority))

            for additional in parsed_abuf.get("AdditionalSection", []):
                self.additionals.append(Additional(additional))


class DnsResult(Result):

    def __init__(self, data, parse_abuf=True, **kwargs):
        """
        Set `parse_abuf=False` if you don't want the `responses` values to
        include all of the parsed abuf data.  This is faster, but will leave a
        lot of fields empty.

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
                parse_abuf=parse_abuf
            ))


__all__ = (
    "DnsResult",
)

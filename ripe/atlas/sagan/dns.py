from __future__ import absolute_import

import base64
import logging
import struct

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


class Message(ValidationMixin):

    def __init__(self, message):

        self._string_representation = message

        self.raw_data = AbufParser.parse(base64.b64decode(message))

        self.header      = Header(self.raw_data["HEADER"])
        self.edns0       = None
        self.questions   = []
        self.answers     = []
        self.authorities = []
        self.additionals = []

        if "EDNS0" in self.raw_data:
            self.edns0 = Edns0(self.raw_data["EDNS0"])

        for question in self.raw_data.get("QuestionSection", []):
            self.questions.append(Question(question))

        for answer in self.raw_data.get("AnswerSection", []):
            self.answers.append(Answer(answer))

        for authority in self.raw_data.get("AuthoritySection", []):
            self.authorities.append(Authority(authority))

        for additional in self.raw_data.get("AdditionalSection", []):
            self.additionals.append(Additional(additional))

    def __str__(self):
        return self._string_representation

    def __repr__(self):
        return str(self)


class Response(ValidationMixin):

    def __init__(self, data, af=None, destination=None, source=None,
                 protocol=None, part_of_set=True, parse_abuf=True):

        self.raw_data    = data

        self.af                  = self.ensure("af",       int, af)
        self.destination_address = self.ensure("dst_addr", str, destination)
        self.source_address      = self.ensure("src_addr", str, source)
        self.protocol            = self.ensure("proto",    str, protocol)

        self.abuf        = None
        self.qbuf        = None
        self.response_id = None

        try:
            abuf_string = self.raw_data["result"]["abuf"]
        except KeyError:
            abuf_string = self.ensure("abuf", str)

        try:
            qbuf_string = self.raw_data["result"]["qbuf"]
        except KeyError:
            qbuf_string = self.ensure("qbuf", str)

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

        if abuf_string and parse_abuf:
            self.abuf = Message(abuf_string)

        if qbuf_string and parse_abuf:
            self.qbuf = Message(qbuf_string)

    # Deprecation shortcuts

    @property
    def header(self):
        logging.warning(
            "Response.header is deprecated and will disappear in v0.2. Use "
            "Response.parsed_abuf.header instead."
        )
        return self.abuf.header

    @property
    def edns0(self):
        logging.warning(
            "Response.edns0 is deprecated and will disappear in v0.2. Use "
            "Response.parsed_abuf.edns0 instead."
        )
        return self.abuf.edns0

    @property
    def questions(self):
        logging.warning(
            "Response.questions is deprecated and will disappear in v0.2. Use "
            "Response.parsed_abuf.questions instead."
        )
        return self.abuf.questions

    @property
    def answers(self):
        logging.warning(
            "Response.answers is deprecated and will disappear in v0.2. "
            "Use Response.parsed_abuf.answers instead."
        )
        return self.abuf.answers

    @property
    def authorities(self):
        logging.warning(
            "Response.authorities is deprecated and will disappear in v0.2. "
            "Use Response.parsed_abuf.authorities instead."
        )
        return self.abuf.authorities

    @property
    def additionals(self):
        logging.warning(
            "Response.additionals is deprecated and will disappear in v0.2. "
            "Use Response.parsed_abuf.additionals instead."
        )
        return self.abuf.additionals


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

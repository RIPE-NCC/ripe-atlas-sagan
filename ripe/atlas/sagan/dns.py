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
        "dnsython isn't installed, without it you cannot parse DNS measurement "
        "results"
    )

from .base import Result, ValidationMixin

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

            parsed_abuf = self.decode_abuf(base64.decodestring(self.abuf))

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

    @classmethod
    def decode_abuf(cls, buf, options=None):
        """
        According to Philip, an abuf is like a TARDIS: it's bigger on the inside
        """

        error         = []
        do_header     = True
        do_question   = True
        do_answer     = True
        do_authority  = True
        do_additional = True
        do_options    = True

        if options and isinstance(options, dict):
            if 'DO_Header' in options and not options['DO_Header']:
                do_header = options['DO_Header']
            if 'DO_Question' in options and not options['DO_Question']:
                do_question = options['DO_Question']
            if 'DO_Answer' in options and not options['DO_Answer']:
                do_answer = options['DO_Answer']
            if 'DO_Authority' in options and not options['DO_Authority']:
                do_authority = options['DO_Authority']
            if 'DO_Additional' in options and not options['DO_Additional']:
                do_additional = options['DO_Additional']
            if 'DO_Options' in options and not options['DO_Options']:
                do_options = options['DO_Options']

        dnsres = {}
        offset = 0
        offset, hdr = cls._parse_header(buf, offset)
        if do_header:
            dnsres['HEADER'] = hdr
        for i in range(hdr['QDCOUNT']):
            offset, qry = cls.do_query(buf, offset)
            if do_question:
                if i == 0:
                    dnsres['QuestionSection'] = [qry]
                else:
                    dnsres['QuestionSection'].append(qry)
        for i in range(hdr['ANCOUNT']):
            offset, rr = cls.do_rr(buf, offset)
            if do_answer:
                if i == 0:
                    dnsres['AnswerSection'] = [rr]
                else:
                    dnsres['AnswerSection'].append(rr)
        for i in range(hdr['NSCOUNT']):
            offset, rr = cls.do_rr(buf, offset)
            if do_authority:
                if i == 0:
                    dnsres['AuthoritySection'] = [rr]
                else:
                    dnsres['AuthoritySection'].append(rr)
        for i in range(hdr['ARCOUNT']):
            res = cls.do_rr(buf, offset)
            if res is None:
                e = ('additional', offset, ('do_rr failed, additional record %d' % i))
                error.append(e)
                dnsres['ERROR'] = error
                #result['decodedabufs_with_ERROR'] += 1
                return dnsres
            offset, rr = res
            if do_options:
                if "EDNS0" in rr:
                    dnsres['EDNS0'] = rr['EDNS0']
                    continue
            if do_additional:
                if 'AdditionalSection' in dnsres:
                    dnsres['AdditionalSection'].append(rr)
                else:
                    dnsres['AdditionalSection'] = [rr]

        if offset < len(buf):
            e = ('end', offset, 'trailing garbage, buf size = %d' % len(buf))
            error.append(e)
            #result['decodedabufs_with_ERROR'] += 1
            dnsres['ERROR'] = error

        return dnsres

    @classmethod
    def _parse_header(cls, buf, offset):

        fmt = "!HHHHHH"
        reqlen = struct.calcsize(fmt)
        strng = buf[offset:offset + reqlen]
        res = struct.unpack(fmt, strng)
        hdr = {
            "ID": res[0]
        }

        qr           = 0x8000
        opcode_mask  = 0x7800
        opcode_shift = 11
        aa           = 0x0400
        tc           = 0x0200
        rd           = 0x0100
        ra           = 0x0080
        z_mask       = 0x0070
        z_shift      = 4
        rcode_mask   = 0x000F
        rcode_shift  = 0

        hdr['QR']      = not not(res[1] & qr)
        hdr['OpCode']  = opcode_to_text((res[1] & opcode_mask) >> opcode_shift)
        hdr['AA']      = not not(res[1] & aa)
        hdr['TC']      = not not(res[1] & tc)
        hdr['RD']      = not not(res[1] & rd)
        hdr['RA']      = not not(res[1] & ra)
        hdr['Z']       = (res[1] & z_mask) >> z_shift
        hdr['ReturnCode'] = rcode_to_text((res[1] & rcode_mask) >> rcode_shift)
        hdr['QDCOUNT'] = res[2]
        hdr['ANCOUNT'] = res[3]
        hdr['NSCOUNT'] = res[4]
        hdr['ARCOUNT'] = res[5]

        return offset + reqlen, hdr

    @classmethod
    def do_query(cls, buf, offset):
        qry           = {}
        offset, name  = cls.do_name(buf, offset)
        qry['Qname']  = name

        fmt           = "!HH"
        reqlen        = struct.calcsize(fmt)
        strng         = buf[offset:offset + reqlen]
        res           = struct.unpack(fmt, strng)
        qry['Qtype']  = type_to_text(res[0])
        qry['Qclass'] = class_to_text(res[1])

        return offset + reqlen, qry

    @classmethod
    def do_rr(cls, buf, offset):
        edns0_opt_nsid = 3  # this is also hardcoded in dns.edns.py
        error          = []
        rr             = {}
        res = cls.do_name(buf, offset)
        if res is None:
            e = ("do_rr", offset, "do_name failed")
            error.append(e)
            return None
        offset, name   = res
        rr['Name']     = name
        fmt            = "!HHIH"
        reqlen         = struct.calcsize(fmt)
        dat            = buf[offset:offset + reqlen]
        res            = struct.unpack(fmt, dat)
        rr['Type']     = type_to_text(res[0])
        rr['Class']    = class_to_text(res[1])
        rr['TTL']      = res[2]
        rr['RDlength'] = res[3]

        offset         += reqlen

        rdata          = buf[offset:offset + rr['RDlength']]
        rdata_offset   = offset

        offset         = offset + rr['RDlength']

        if rr['Type'] == 'OPT':      # this is per type_to_text function
            edns0 = {
                'UDPsize':            res[1],
                'ExtendedReturnCode': res[2] >> 24,
                'Version':            (res[2] and 0x0f00) >> 16,
                'Z':                  (res[2] and 0x00ff),
                'Type':               'OPT',
                'Option':             [],
                'Name':               name,
            }

            o = 0
            while o < len(rdata):
                fmt    = "!HH"
                reqlen = struct.calcsize(fmt)
                dat    = rdata[o:o + reqlen]
                res    = struct.unpack(fmt, dat)
                opt = {
                    'OptionCode': res[0],
                    'OptionLength': res[1],
                }
                o += reqlen
                if opt['OptionCode'] == edns0_opt_nsid:
                    opt['OptionName']      = 'NSID'
                    opt[opt['OptionName']] = rdata[o:o + opt['OptionLength']]

                o = o + opt['OptionLength']
                edns0['Option'].append(opt)

            del rr['Class']
            del rr['RDlength']
            del rr['TTL']
            del rr['Name']
            del rr['Type']
            rr['EDNS0'] = edns0
            return offset, rr

        if rr['Type'] == 'A' and rr['Class'] == "IN":  # this is per type_to_text function
            fmt           = "!BBBB"
            a, b, c, d    = struct.unpack(fmt, rdata)
            rr['Address'] = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)

        if rr['Type'] == 'NS' and rr['Class'] == "IN":  # this is per type_to_text function
            doffset, name = cls.do_name(buf, rdata_offset)
            rr['Target'] = name

        return offset, rr

    @classmethod
    def do_name(cls, buf, offset):
        name  = ''
        error = []
        while True:
            fmt    = "!B"
            reqlen = struct.calcsize(fmt)
            strng    = buf[offset:offset + reqlen]
            if len(strng) != reqlen:
                e = ("do_name", offset, 'offset out of range: buf size = %d' % len(buf))
                error.append(e)
                return None
            res    = struct.unpack(fmt, strng)
            llen   = res[0]
            if llen <= 63:
                # Label
                offset += 1
                label  = buf[offset:offset + llen]
                offset = offset + llen
                if name == '' or label != '':
                    name = name + label + '.'
                if llen == 0:
                    break
            elif llen >= 0xC0:
                fmt     = "!H"
                reqlen  = struct.calcsize(fmt)
                strng   = buf[offset:offset + reqlen]
                res     = struct.unpack(fmt, strng)
                poffset = res[0] & ~0xC000
                poffset, pname = cls.do_name(buf, poffset)
                offset  += reqlen
                name    = name + pname
                break
            else:
                return None

        return offset, name


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

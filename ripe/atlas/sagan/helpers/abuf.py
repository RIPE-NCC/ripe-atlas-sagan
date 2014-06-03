from __future__ import absolute_import

import base64
import logging
import struct

class AbufParser(object):

    @classmethod
    def parse(cls, buf, options=None):
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
            offset, qry = cls._do_query(buf, offset)
            if do_question:
                if i == 0:
                    dnsres['QuestionSection'] = [qry]
                else:
                    dnsres['QuestionSection'].append(qry)
        for i in range(hdr['ANCOUNT']):
            offset, rr = cls._do_rr(buf, offset)
            if do_answer:
                if i == 0:
                    dnsres['AnswerSection'] = [rr]
                else:
                    dnsres['AnswerSection'].append(rr)
        for i in range(hdr['NSCOUNT']):
            offset, rr = cls._do_rr(buf, offset)
            if do_authority:
                if i == 0:
                    dnsres['AuthoritySection'] = [rr]
                else:
                    dnsres['AuthoritySection'].append(rr)
        for i in range(hdr['ARCOUNT']):
            res = cls._do_rr(buf, offset)
            if res is None:
                e = ('additional', offset, ('_do_rr failed, additional record %d' % i))
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

    @staticmethod
    def _opcode_to_text(opcode):
        return { 0: 'QUERY', 1: 'IQUERY', 2: 'STATUS',
                4: 'NOTIFY', 5: 'UPDATE'}.get(opcode, opcode)

    @staticmethod
    def _class_to_text(rdataclass):
        return {0: 'RESERVED0', 1: 'IN', 3: 'CH', 4: 'HS',
                254: 'NONE', 255: 'ANY'}.get(rdataclass, rdataclass)

    @staticmethod
    def _rcode_to_text(rcode):
        return {0: 'NOERROR', 1: 'FORMERR', 2: 'SERVFAIL', 3: 'NXDOMAIN',
                4: 'NOTIMP',  5: 'REFUSED', 6: 'YXDOMAIN', 7: 'YXRRSET',
                8: 'NXRRSET', 9: 'NOTAUTH', 10: 'NOTZONE',
                16: 'BADVERS'}.get(rcode, rcode)

    @staticmethod
    def _type_to_text(rdatatype):
        return {0: 'NONE', 1: 'A', 2: 'NS', 3: 'MD', 4: 'MF', 5: 'CNAME', 6: 'SOA',
                7: 'MB', 8: 'MG', 9: 'MR', 10: 'NULL', 11: 'WKS', 12: 'PTR', 13: 'HINFO',
                14: 'MINFO', 15: 'MX', 16: 'TXT', 17: 'RP', 18: 'AFSDB', 19: 'X25',
                20: 'ISDN', 21: 'RT', 22: 'NSAP', 23: 'NSAP_PTR', 24: 'SIG', 25: 'KEY',
                26: 'PX', 27: 'GPOS', 28: 'AAAA', 29: 'LOC', 30: 'NXT', 33: 'SRV',
                35: 'NAPTR', 36: 'KX', 37: 'CERT', 38: 'A6', 39: 'DNAME', 41: 'OPT',
                42: 'APL', 43: 'DS', 44: 'SSHFP', 45: 'IPSECKEY', 46: 'RRSIG', 47: 'NSEC',
                48: 'DNSKEY', 49: 'DHCID', 50: 'NSEC3', 51: 'NSEC3PARAM', 52: 'TLSA',
                55: 'HIP', 99: 'SPF', 103: 'UNSPEC', 249: 'TKEY', 250: 'TSIG', 251: 'IXFR',
                252: 'AXFR', 253: 'MAILB', 254: 'MAILA', 255: 'ANY', 32768: 'TA',
                32769: 'DLV'}.get(rdatatype,rdatatype)

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
        hdr['OpCode']  = cls._opcode_to_text((res[1] & opcode_mask) >> opcode_shift)
        hdr['AA']      = not not(res[1] & aa)
        hdr['TC']      = not not(res[1] & tc)
        hdr['RD']      = not not(res[1] & rd)
        hdr['RA']      = not not(res[1] & ra)
        hdr['Z']       = (res[1] & z_mask) >> z_shift
        hdr['ReturnCode'] = cls._rcode_to_text((res[1] & rcode_mask) >> rcode_shift)
        hdr['QDCOUNT'] = res[2]
        hdr['ANCOUNT'] = res[3]
        hdr['NSCOUNT'] = res[4]
        hdr['ARCOUNT'] = res[5]

        return offset + reqlen, hdr

    @classmethod
    def _do_query(cls, buf, offset):
        qry           = {}
        offset, name  = cls._do_name(buf, offset)
        qry['Qname']  = name

        fmt           = "!HH"
        reqlen        = struct.calcsize(fmt)
        strng         = buf[offset:offset + reqlen]
        res           = struct.unpack(fmt, strng)
        qry['Qtype']  = cls._type_to_text(res[0])
        qry['Qclass'] = cls._class_to_text(res[1])

        return offset + reqlen, qry

    @classmethod
    def _do_rr(cls, buf, offset):
        edns0_opt_nsid = 3  # this is also hardcoded in dns.edns.py
        error          = []
        rr             = {}
        res = cls._do_name(buf, offset)
        if res is None:
            e = ("_do_rr", offset, "_do_name failed")
            error.append(e)
            return None
        offset, name   = res
        rr['Name']     = name
        fmt            = "!HHIH"
        reqlen         = struct.calcsize(fmt)
        dat            = buf[offset:offset + reqlen]
        res            = struct.unpack(fmt, dat)
        rr['Type']     = cls._type_to_text(res[0])
        rr['Class']    = cls._class_to_text(res[1])
        rr['TTL']      = res[2]
        rr['RDlength'] = res[3]

        offset         += reqlen

        rdata          = buf[offset:offset + rr['RDlength']]
        rdata_offset   = offset

        offset         = offset + rr['RDlength']

        if rr['Type'] == 'OPT':      # this is per cls._type_to_text function
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

        if rr['Type'] == 'A' and rr['Class'] == "IN":  # this is per cls._type_to_text function
            fmt           = "!BBBB"
            a, b, c, d    = struct.unpack(fmt, rdata)
            rr['Address'] = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)

        if rr['Type'] == 'NS' and rr['Class'] == "IN":  # this is per cls._type_to_text function
            doffset, name = cls._do_name(buf, rdata_offset)
            rr['Target'] = name

        return offset, rr

    @classmethod
    def _do_name(cls, buf, offset):
        name  = ''
        error = []
        while True:
            fmt    = "!B"
            reqlen = struct.calcsize(fmt)
            strng    = buf[offset:offset + reqlen]
            if len(strng) != reqlen:
                e = ("_do_name", offset, 'offset out of range: buf size = %d' % len(buf))
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
                poffset, pname = cls._do_name(buf, poffset)
                offset  += reqlen
                name    = name + pname
                break
            else:
                return None

        return offset, name


__all__ = (
    "DnsResult",
)

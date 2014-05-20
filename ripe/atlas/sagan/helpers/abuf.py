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
        z_mask       = 0x0040
        ad           = 0x0020
        cd           = 0x0010
        rcode_mask   = 0x000F
        rcode_shift  = 0

        hdr['QR']      = not not(res[1] & qr)
        hdr['OpCode']  = opcode_to_text((res[1] & opcode_mask) >> opcode_shift)
        hdr['AA']      = not not(res[1] & aa)
        hdr['TC']      = not not(res[1] & tc)
        hdr['RD']      = not not(res[1] & rd)
        hdr['RA']      = not not(res[1] & ra)
        hdr['Z']       = res[1] & z_mask
        hdr['AD']      = res[1] & ad
        hdr['CD']      = res[1] & cd
        hdr['ReturnCode'] = rcode_to_text((res[1] & rcode_mask) >> rcode_shift)
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
        qry['Qtype']  = type_to_text(res[0])
        qry['Qclass'] = class_to_text(res[1])

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

        if rr['Class'] == "IN":
            # this is per type_to_text function
            if rr['Type'] == 'A':
                fmt           = "!BBBB"
                rr['Address'] = '.'.join(str(byte) for byte in struct.unpack(fmt, rdata))
                rr['Answer'] = rr['Address']
            elif rr['Type'] == 'AAAA':
                fmt           = "!BBBBBBBBBBBBBBBB"
                rr['Address'] = ':'.join(str(nibble) for nibble in struct.unpack(fmt, rdata))
                rr['Answer'] = rr['Address']
            elif rr['Type'] == 'CNAME':
                doffset, name = cls._do_name(buf, rdata_offset)
                rr['Answer'] = name
            elif rr['Type'] == 'NS': 
                doffset, name = cls._do_name(buf, rdata_offset)
            elif rr['Type'] == 'MX': 
                fmt = '!H'
                fmtsz = struct.calcsize(fmt)
                rr['Pref'] = struct.unpack(fmt, rdata[:fmtsz])[0]
                rr_offset, rr['Exchange'] = cls._do_name(buf, rdata_offset+fmtsz)
                rr['Answer'] = '{} {}'.format(rr['Pref'], rr['Exchange'])
            elif rr['Type'] == 'SOA': 
                fmt = '!IIIII'
                rr_offset, rr['Mname'] = cls._do_name(buf, rdata_offset)
                rr_offset, rr['Rname'] = cls._do_name(buf, rr_offset)
                rr['Serial'], rr['Refresh'], rr['Retry'], rr['Expire'], rr['Minimum']\
                        = struct.unpack(fmt, buf[rr_offset:rr_offset + struct.calcsize(fmt)])
                rr['Answer'] = '{} {} {} {} {} {} {}'.format(rr['Mname'], rr['Rname'],
                        rr['Serial'], rr['Refresh'], rr['Retry'], rr['Expire'], 
                        rr['Minimum'])
            elif rr['Type'] == 'DS': 
                fmt = '!HBB'
                digest_size = 0
                rr['KeyTag'], rr['Algo'], rr['DigestType'] = \
                        struct.unpack(fmt, rdata[:struct.calcsize(fmt)])
                rr['Digest'] = rdata[struct.calcsize(fmt):].encode('hex')
                rr['Answer'] = '{} {} {} {}'.format(rr['KeyTag'], rr['Algo'], 
                        rr['DigestType'], rr['Digest'])
            elif rr['Type'] == 'DNSKEY': 
                fmt = '!HBB'
                rr['Flags'], rr['Proto'], rr['Algo'] =\
                        struct.unpack(fmt, rdata[:struct.calcsize(fmt)])
                rr['Data'] = ''.join(base64.encodestring(
                    rdata[struct.calcsize(fmt):]).split())
                rr['Answer'] = '{} {} {} {}'.format(rr['Flags'], rr['Proto'], rr['Algo'], 
                        rr['Data'])

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

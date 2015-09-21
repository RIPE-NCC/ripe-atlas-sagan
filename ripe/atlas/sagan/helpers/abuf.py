from __future__ import absolute_import

import base64
import codecs
import struct


class AbufParser(object):

    DNS_CTYPE = "UTF=8"

    @classmethod
    def parse(cls, buf, options=None):
        """
        According to Philip, an abuf is like a TARDIS: it's bigger on the inside
        """

        error = []
        do_header = True
        do_question = True
        do_answer = True
        do_authority = True
        do_additional = True
        do_options = True

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
        offset, hdr = cls._parse_header(buf, offset, error)
        if do_header:
            dnsres['HEADER'] = hdr
        for i in range(hdr['QDCOUNT']):
            res = cls._do_query(buf, offset, error)
            if res is None:
                e = ('additional', offset,
                     '_do_query failed, additional record {0}'.format(i))
                error.append(e)
                dnsres['ERROR'] = error
                return dnsres
            offset, qry = res
            if do_question:
                if i == 0:
                    dnsres['QuestionSection'] = [qry]
                else:
                    dnsres['QuestionSection'].append(qry)
        for i in range(hdr['ANCOUNT']):
            res = cls._do_rr(buf, offset, error)
            if res is None:
                e = ('additional', offset,
                     '_do_rr failed, additional record {0}'.format(i))
                error.append(e)
                dnsres['ERROR'] = error
                return dnsres
            offset, rr = res
            if do_answer:
                if i == 0:
                    dnsres['AnswerSection'] = [rr]
                else:
                    dnsres['AnswerSection'].append(rr)
        for i in range(hdr['NSCOUNT']):
            res = cls._do_rr(buf, offset, error)
            if res is None:
                e = ('additional', offset,
                     '_do_rr failed, additional record %d'.format(i))
                error.append(e)
                dnsres['ERROR'] = error
                return dnsres
            offset, rr = res
            if do_authority:
                if i == 0:
                    dnsres['AuthoritySection'] = [rr]
                else:
                    dnsres['AuthoritySection'].append(rr)
        for i in range(hdr['ARCOUNT']):
            res = cls._do_rr(buf, offset, error)
            if res is None:
                e = ('additional', offset,
                     '_do_rr failed, additional record %d'.format(i))
                error.append(e)
                dnsres['ERROR'] = error
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
        return {
            0: 'QUERY',
            1: 'IQUERY',
            2: 'STATUS',
            4: 'NOTIFY',
            5: 'UPDATE'
        }.get(opcode, opcode)

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
        return {
            0: 'NONE', 1: 'A', 2: 'NS', 3: 'MD', 4: 'MF', 5: 'CNAME', 6: 'SOA',
            7: 'MB', 8: 'MG', 9: 'MR', 10: 'NULL', 11: 'WKS', 12: 'PTR', 13: 'HINFO',
            14: 'MINFO', 15: 'MX', 16: 'TXT', 17: 'RP', 18: 'AFSDB', 19: 'X25',
            20: 'ISDN', 21: 'RT', 22: 'NSAP', 23: 'NSAP_PTR', 24: 'SIG', 25: 'KEY',
            26: 'PX', 27: 'GPOS', 28: 'AAAA', 29: 'LOC', 30: 'NXT', 33: 'SRV',
            35: 'NAPTR', 36: 'KX', 37: 'CERT', 38: 'A6', 39: 'DNAME', 41: 'OPT',
            42: 'APL', 43: 'DS', 44: 'SSHFP', 45: 'IPSECKEY', 46: 'RRSIG', 47: 'NSEC',
            48: 'DNSKEY', 49: 'DHCID', 50: 'NSEC3', 51: 'NSEC3PARAM', 52: 'TLSA',
            55: 'HIP', 99: 'SPF', 103: 'UNSPEC', 249: 'TKEY', 250: 'TSIG', 251: 'IXFR',
            252: 'AXFR', 253: 'MAILB', 254: 'MAILA', 255: 'ANY', 32768: 'TA',
            32769: 'DLV'
        }.get(rdatatype, rdatatype)

    @classmethod
    def _parse_header(cls, buf, offset, error):

        fmt = "!HHHHHH"
        reqlen = struct.calcsize(fmt)
        strng = buf[offset:offset + reqlen]
        if len(strng) != reqlen:
            e = ("_parse_header", offset,
                 'offset out of range: buf size = %d'.format(len(buf)))
            error.append(e)
            return None
        res = struct.unpack(fmt, strng)
        hdr = {
            "ID": res[0]
        }

        qr = 0x8000
        opcode_mask = 0x7800
        opcode_shift = 11
        aa = 0x0400
        tc = 0x0200
        rd = 0x0100
        ra = 0x0080
        z_mask = 0x0040
        z_shift = 6
        ad = 0x0020
        cd = 0x0010
        rcode_mask = 0x000F
        rcode_shift = 0

        hdr['QR'] = bool(res[1] & qr)
        hdr['OpCode'] = cls._opcode_to_text((res[1] & opcode_mask) >> opcode_shift)
        hdr['AA'] = bool(res[1] & aa)
        hdr['TC'] = bool(res[1] & tc)
        hdr['RD'] = bool(res[1] & rd)
        hdr['RA'] = bool(res[1] & ra)
        hdr['Z'] = (res[1] & z_mask) >> z_shift
        hdr['AD'] = bool(res[1] & ad)
        hdr['CD'] = bool(res[1] & cd)
        hdr['ReturnCode'] = cls._rcode_to_text((res[1] & rcode_mask) >> rcode_shift)
        hdr['QDCOUNT'] = res[2]
        hdr['ANCOUNT'] = res[3]
        hdr['NSCOUNT'] = res[4]
        hdr['ARCOUNT'] = res[5]

        return offset + reqlen, hdr

    @classmethod
    def _do_query(cls, buf, offset, error):
        qry = {}
        offset, name = cls._do_name(buf, offset, error)
        qry['Qname'] = name

        fmt = "!HH"
        reqlen = struct.calcsize(fmt)
        strng = buf[offset:offset + reqlen]
        if len(strng) != reqlen:
            e = ("_do_query", offset,
                 'offset out of range: buf size = {0}'.format(len(buf)))
            error.append(e)
            return None
        res = struct.unpack(fmt, strng)
        qry['Qtype'] = cls._type_to_text(res[0])
        qry['Qclass'] = cls._class_to_text(res[1])

        return offset + reqlen, qry

    @classmethod
    def _clean_up_string(cls, strng):
        result = ''
        strng = bytearray(strng)
        for o in strng:
            if o < ord(' ') or o > ord('~'):
                result += ("\\%03d" % o)
            elif o == ord('"') or o == ord('\\'):
                result += "\\" + chr(o)
            else:
                result += chr(o)
        return result

    @classmethod
    def _do_rr(cls, buf, offset, error):
        edns0_opt_nsid = 3  # this is also hardcoded in dns.edns.py
        rr = {}
        res = cls._do_name(buf, offset, error)
        if res is None:
            e = ("_do_rr", offset, "_do_name failed")
            error.append(e)
            return None
        offset, name = res
        rr['Name'] = name
        fmt = "!HHIH"
        reqlen = struct.calcsize(fmt)
        dat = buf[offset:offset + reqlen]
        if len(dat) != reqlen:
            e = ("_do_rr", offset,
                 'offset out of range: buf size = %d'.format(len(buf)))
            error.append(e)
            return None
        res = struct.unpack(fmt, dat)
        rr['Type'] = cls._type_to_text(res[0])
        rr['Class'] = cls._class_to_text(res[1])
        rr['TTL'] = res[2]
        rr['RDlength'] = res[3]

        offset += reqlen

        rdata = buf[offset:offset + rr['RDlength']]
        rdata_offset = offset

        offset = offset + rr['RDlength']

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
                fmt = "!HH"
                reqlen = struct.calcsize(fmt)
                dat = rdata[o:o + reqlen]
                if len(dat) != reqlen:
                    e = (
                        "_do_rr",
                        rdata_offset,
                        'offset out of range: rdata size = {0}'.format(
                            len(rdata)
                        )
                    )
                    error.append(e)
                    return None
                res = struct.unpack(fmt, dat)
                opt = {
                    'OptionCode': res[0],
                    'OptionLength': res[1],
                }
                o += reqlen
                if opt['OptionCode'] == edns0_opt_nsid:
                    opt['OptionName'] = 'NSID'
                    nsid = rdata[o:o + opt['OptionLength']]
                    nsid_as_str = nsid.decode(cls.DNS_CTYPE)
                    opt[opt['OptionName']] = nsid_as_str

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
            # this is per cls._type_to_text function
            if rr['Type'] == 'A':
                fmt = "!BBBB"
                reqlen = struct.calcsize(fmt)
                if reqlen > len(rdata):
                    e = ("_do_rr", rdata_offset,
                         'rdata too small: size = {0}'.format(len(rdata)))
                    error.append(e)
                    return None
                rr['Address'] = '.'.join(
                    str(byte) for byte in struct.unpack(fmt, rdata)
                )
            elif rr['Type'] == 'AAAA':
                fmt = "!HHHHHHHH"
                reqlen = struct.calcsize(fmt)
                if reqlen > len(rdata):
                    e = ("_do_rr", rdata_offset,
                         'rdata too small: size = %d'.format(len(rdata)))
                    error.append(e)
                    return None
                addr = ':'.join(
                    ("%x" % quad) for quad in struct.unpack(fmt, rdata)
                )
                rr['Address'] = addr
            elif rr['Type'] == 'CNAME':
                doffset, name = cls._do_name(buf, rdata_offset, error)
                rr['Target'] = name
            elif rr['Type'] == 'NS':
                doffset, name = cls._do_name(buf, rdata_offset, error)
                rr['Target'] = name
            elif rr['Type'] == 'MX':
                fmt = '!H'
                fmtsz = struct.calcsize(fmt)
                dat = rdata[:fmtsz]
                if len(dat) != fmtsz:
                    e = (
                        "_do_rr",
                        rdata_offset,
                        'offset out of range: rdata size = {0}'.format(
                            len(rdata)
                        )
                    )
                    error.append(e)
                    return None
                rr['Preference'] = struct.unpack(fmt, dat)[0]
                rr_offset, rr['MailExchanger'] = cls._do_name(
                    buf,
                    rdata_offset + fmtsz,
                    error
                )
            elif rr['Type'] == 'SOA':
                offset_name = cls._do_name(buf, rdata_offset, error)
                if offset_name is None:
                        e = ("do_rr", rdata_offset, '_do_name failed')
                        error.append(e)
                        return None
                rr_offset, rr['MasterServerName'] = offset_name
                offset_name = cls._do_name(buf, rr_offset, error)
                if offset_name is None:
                        e = ("do_rr", rr_offset, '_do_name failed')
                        error.append(e)
                        return None
                rr_offset, rr['MaintainerName'] = offset_name
                fmt = '!IIIII'
                fmtsz = struct.calcsize(fmt)
                dat = buf[rr_offset:rr_offset + fmtsz]
                if len(dat) != fmtsz:
                    e = (
                        "_do_rr",
                        rr_offset,
                        'offset out of range: rdata size = {0}'.format(
                            len(rdata)
                        )
                    )
                    error.append(e)
                    return None
                rr['Serial'], rr['Refresh'], rr['Retry'], rr['Expire'], rr['NegativeTtl'] = struct.unpack(fmt, dat)
            elif rr['Type'] == 'DS':

                fmt = '!HBB'
                fmtsz = struct.calcsize(fmt)
                dat = rdata[:fmtsz]
                if len(dat) != fmtsz:
                    e = (
                        "_do_rr",
                        rdata_offset,
                        'offset out of range: rdata size = {0}'.format(
                            len(rdata)
                        )
                    )
                    error.append(e)
                    return None
                rr['Tag'], rr['Algorithm'], rr['DigestType'] = struct.unpack(
                    fmt, dat)
                key = rdata[struct.calcsize(fmt):]
                key_as_hex = codecs.getencoder('hex_codec')(key)[0]
                key_as_hex_str = key_as_hex.decode(cls.DNS_CTYPE)
                rr['DelegationKey'] = key_as_hex_str
            elif rr['Type'] == 'DNSKEY':
                fmt = '!HBB'
                fmtsz = struct.calcsize(fmt)
                dat = rdata[:fmtsz]
                if len(dat) != fmtsz:
                    e = (
                        "_do_rr",
                        rdata_offset,
                        'offset out of range: rdata size = {0}'.format(
                            len(rdata)
                        )
                    )
                    error.append(e)
                    return None
                rr['Flags'], rr['Protocol'], rr['Algorithm'] = struct.unpack(
                    fmt, dat)
                key = rdata[struct.calcsize(fmt):]
                key_as_base64 = cls._encodebytes(key)
                key_as_base64_str = key_as_base64.decode(cls.DNS_CTYPE)
                rr['Key'] = ''.join(key_as_base64_str.split())
            elif rr['Type'] == 'RRSIG':
                # https://tools.ietf.org/html/rfc4034#section-3.1

                """ The RDATA for an RRSIG RR consists of a 2 octet Type
                Covered field, a 1 octet Algorithm field, a 1 octet Labels
                field, a 4 octet Original  TTL field, a 4 octet Signature
                Expiration field, a 4 octet Signature Inception field, a 2
                octet Key tag, the Signer's Name field, and the Signature
                field. """

                fmt = "!HBBIIIH"
                fmtsz = struct.calcsize(fmt)
                dat = rdata[:fmtsz]
                if len(dat) != fmtsz:
                    e = (
                        "_do_rr",
                        rdata_offset,
                        'offset out of range: rdata size = {0}'.format(
                            len(rdata)
                        )
                    )
                    error.append(e)
                    return None
                rr['TypeCovered'], rr['Algorithm'], rr['Labels'], rr['OriginalTTL'], rr['SignatureExpiration'], rr['SignatureInception'], rr['KeyTag'] = struct.unpack(fmt, dat)
                rr['TypeCovered'] = cls._type_to_text(rr['TypeCovered'])

                res = cls._do_name(rdata, fmtsz, error)
                if res is None:
                    e = ("_do_rr", offset, "_do_name failed")
                    error.append(e)
                    return None
                signature_offset, rr['SignerName'] = res

                sig = rdata[signature_offset:]
                sig_as_base64 = cls._encodebytes(sig)
                sig_as_base64_str = sig_as_base64.decode(cls.DNS_CTYPE)
                rr['Signature'] = ''.join(sig_as_base64_str.split())

        if rr['Type'] == 'TXT':
            if rr['Class'] == "IN" or rr['Class'] == "CH":
                fmt = "!B"
                reqlen = struct.calcsize(fmt)
                o = 0
                rr['Data'] = []
                while o < len(rdata):
                        strng = rdata[o:o+reqlen]
                        if len(strng) != reqlen:
                            e = (
                                "_do_rr",
                                rdata_offset,
                                'offset out of range: rdata size = {0}'.format(
                                    len(rdata)
                                )
                            )
                            error.append(e)
                            return None
                        res = struct.unpack(fmt, strng)
                        llen = res[0]
                        o += reqlen
                        strng = rdata[o:o+llen]
                        if len(strng) < llen:
                            e = (
                                "_do_rr",
                                rdata_offset,
                                'offset out of range: rdata size = %d'.format(
                                    len(rdata)
                                )
                            )
                            error.append(e)
                            return None
                        strng = cls._clean_up_string(strng)
                        rr['Data'].append(strng)
                        o += llen

        return offset, rr

    @classmethod
    def _do_name(cls, buf, offset, error):
        name = ''
        while True:
            fmt = "!B"
            reqlen = struct.calcsize(fmt)
            strng = buf[offset:offset + reqlen]
            if len(strng) != reqlen:
                e = ("_do_name", offset, 'offset out of range: buf size = %d' % len(buf))
                error.append(e)
                return None
            res = struct.unpack(fmt, strng)
            llen = res[0]
            if llen <= 63:
                # Label
                offset += 1
                label = buf[offset:offset + llen]
                offset = offset + llen
                label_as_str = label.decode(cls.DNS_CTYPE)
                if name == '' or label_as_str != '':
                    name = name + label_as_str + '.'
                if llen == 0:
                    break
            elif llen >= 0xC0:
                fmt = "!H"
                reqlen = struct.calcsize(fmt)
                strng = buf[offset:offset + reqlen]
                if len(strng) != reqlen:
                    e = ("_do_name", offset, 'offset out of range: buf size = %d' % len(buf))
                    error.append(e)
                    return None
                res = struct.unpack(fmt, strng)
                poffset = res[0] & ~0xC000
                n = cls._do_name(buf, poffset, error)
                if n is None:
                    e = (
                        "_do_name",
                        poffset,
                        'offset out of range: buf size = {0}'.format(len(buf))
                    )
                    error.append(e)
                    return None
                poffset, pname = n
                offset += reqlen
                name = name + pname
                break
            else:
                return None

        return offset, name

    @staticmethod
    def _encodebytes(s):
        """
        A wrapper to take care of the deprecation of base64.encodestring() in
        Python 3.
        """
        try:
            return base64.encodebytes(s)  # 3
        except AttributeError:
            return base64.encodestring(s)  # 2


__all__ = (
    "AbufParser",
)

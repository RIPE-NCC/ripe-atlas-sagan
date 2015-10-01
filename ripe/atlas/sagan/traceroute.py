import logging

from calendar import timegm
from IPy import IP

from .base import Result, ParsingDict


class IcmpHeader(ParsingDict):
    """
    But why did we stop here?  Why not go all the way and define subclasses for
    each object and for `mpls`?  it comes down to a question of complexity vs.
    usefulness.  This is such a fringe case that it's probably fine to just
    dump the data in to `self.objects` and let people work from there.  If
    however you feel that this needs expansion, pull requests are welcome :-)

    Further information regarding the structure and meaning of the data in
    this class can be found here: http://localhost:8000/docs/data_struct/
    """

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data

        self.version = self.ensure("version", int)
        self.rfc4884 = self.ensure("rfc4884", bool)
        self.objects = self.ensure("obj",     list)


class Packet(ParsingDict):

    ERROR_CONDITIONS = {
        "N": "Network unreachable",
        "H": "Destination unreachable",
        "A": "Administratively prohibited",
        "P": "Protocol unreachable",
        "p": "Port unreachable",
    }

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data

        self.origin = self.ensure("from", str)
        self.rtt = self.ensure("rtt", float)
        self.size = self.ensure("size", int)
        self.ttl = self.ensure("ttl", int)
        self.mtu = self.ensure("mtu", int)
        self.destination_option_size = self.ensure("dstoptsize", int)
        self.hop_by_hop_option_size = self.ensure("hbhoptsize", int)
        self.arrived_late_by = self.ensure("late", int, 0)
        self.internal_ttl = self.ensure("ittl", int, 1)

        if self.rtt:
            self.rtt = round(self.rtt, 3)

        error = self.ensure("err", str)
        if error:
            self._handle_error(self.ERROR_CONDITIONS.get(error, error))

        icmp_header = self.ensure("icmpext", dict)

        self.icmp_header = None
        if icmp_header:
            self.icmp_header = IcmpHeader(icmp_header, **kwargs)

    def __str__(self):
        return self.origin


class Hop(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data

        self.index = self.ensure("hop", int)

        error = self.ensure("error", str)
        if error:
            self._handle_error(error)

        self.packets = []
        if "result" in self.raw_data:
            for packet in self.raw_data["result"]:
                self.packets.append(Packet(packet, **kwargs))

        self.median_rtt = None
        if self.packets:
            rtts = sorted([p.rtt for p in self.packets if p and p.rtt])
            if rtts:
                self.median_rtt = Result.calculate_median(rtts)

    def __str__(self):
        return self.index


class TracerouteResult(Result):

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.af = self.ensure("af", int)
        self.destination_address = self.ensure("dst_addr", str)
        self.destination_name = self.ensure("dst_name", str)
        self.source_address = self.ensure("src_addr", str)
        self.end_time = self.ensure("endtime", "datetime")
        self.paris_id = self.ensure("paris_id", int)
        self.size = self.ensure("size", int)

        if 0 < self.firmware < 4460:
            self.af = self.ensure("pf", int)

        self.protocol = self.clean_protocol(self.ensure("proto", str))

        self.hops = []
        self.total_hops = 0
        self.last_median_rtt = None
        self._parse_hops(**kwargs)  # Sets hops, last_rtt, and total_hops

        # Used by a few response tests below
        self._destination_ip_responded = None
        self._last_hop_responded = None

    @property
    def last_rtt(self):
        logging.warning(
            '"last_rtt" is deprecated and will be removed in future versions. '
            'Instead, use "last_median_rtt".')
        return self.last_median_rtt

    @property
    def target_responded(self):
        logging.warning(
            'The "target_responded" property is deprecated and will be removed '
            'in future versions.  Instead, use "destination_ip_responded".'
        )
        return self.destination_ip_responded

    @property
    def destination_ip_responded(self):

        if self._destination_ip_responded is not None:
            return self._destination_ip_responded

        self._destination_ip_responded = False
        if self.hops and self.hops[-1].packets:
            destination_address = IP(self.destination_address)
            for packet in self.hops[-1].packets:
                if packet.origin and destination_address == IP(packet.origin):
                    self._destination_ip_responded = True
                    break

        return self.destination_ip_responded

    @property
    def last_hop_responded(self):

        if self._last_hop_responded is not None:
            return self._last_hop_responded

        self._last_hop_responded = False
        if self.hops and self.hops[-1].packets:
            for packet in self.hops[-1].packets:
                if packet.origin:
                    self._last_hop_responded = True
                    break

        return self.last_hop_responded

    @property
    def end_time_timestamp(self):
        return timegm(self.end_time.timetuple())

    @property
    def ip_path(self):
        """
        Returns just the IPs from the traceroute.
        """
        r = []
        for hop in self.hops:
            r.append([packet.origin for packet in hop.packets])
        return r

    def _parse_hops(self, **kwargs):

        try:
            hops = self.raw_data["result"]
            assert(isinstance(hops, list))
        except (KeyError, AssertionError):
            self._handle_malformation("Legacy formats not supported")
            return

        for hop in hops:

            hop = Hop(hop, **kwargs)

            if hop.median_rtt:
                self.last_median_rtt = hop.median_rtt

            self.hops.append(hop)
            self.total_hops += 1


__all__ = (
    "TracerouteResult",
)

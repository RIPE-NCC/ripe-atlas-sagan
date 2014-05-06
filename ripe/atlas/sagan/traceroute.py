import logging

from .base import Result, ValidationMixin

class Packet(ValidationMixin):
    """
    origin: The `from` value, if any
    rtt:    Return trip time
    size:   The packet size
    ttl:    Time to live
    """

    ERROR_CONDITIONS = {
        "N": "Network unreachable",
        "H": "Destination unreachable",
        "A": "Administratively prohibited",
        "P": "Protocol unreachable",
        "p": "Port unreachable",
    }

    def __init__(self, data):

        self.raw_data = data

        self.origin = self.ensure("from", str)
        self.rtt    = self.ensure("rtt",  float)
        self.size   = self.ensure("size", int)
        self.ttl    = self.ensure("ttl",  int)
        self.error  = self.ensure("err",  str)

        if self.rtt:
            self.rtt = round(self.rtt, 3)

        if self.error in self.ERROR_CONDITIONS.keys():
            self.error = self.ERROR_CONDITIONS[self.error]

    def __str__(self):
        return self.origin


class Hop(ValidationMixin):
    """
    index:   The hop number
    packets: A list of packet objects
    """

    def __init__(self, data):

        self.raw_data = data

        self.index = self.ensure("hop", int)
        self.error = self.ensure("error", str)

        self.packets = []
        if "result" in self.raw_data:
            for packet in self.raw_data["result"]:
                self.packets.append(Packet(packet))

    def __str__(self):
        return self.index


class TracerouteResult(Result):

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.af                  = self.ensure("af", int)
        self.destination_address = self.ensure("dst_addr", str)
        self.destination_name    = self.ensure("dst_name", str)
        self.source_address      = self.ensure("src_addr", str)
        self.end_time            = self.ensure("endtime",  "datetime")
        self.paris_id            = self.ensure("paris_id", int)
        self.size                = self.ensure("size",     int)

        if 0 < self.firmware < 4460:
            self.af = self.ensure("pf", int)

        self.protocol = self.clean_protocol(self.ensure("proto", str))

        self.hops       = []
        self.total_hops = 0
        self.last_rtt   = None
        self._parse_hops()  # Sets hops, last_rtt, and total_hops

        self.target_responded = False
        if self.hops and self.hops[-1].index == self.total_hops:
            self.target_responded = True

    @property
    def end_time_timestamp(self):
        return self.end_time.timestamp

    def _parse_hops(self):

        try:
            hops = self.raw_data["result"]
            assert(isinstance(hops, list))
        except (KeyError, AssertionError):
            logging.warning("Legacy formats not supported")
            return

        for hop in hops:

            hop = Hop(hop)

            rtts = []
            for packet in hop.packets:
                if packet.rtt is not None:
                    rtts.append(packet.rtt)
                    self.last_rtt = packet.rtt
            rtts.sort()

            self.hops.append(hop)
            self.total_hops += 1


__all__ = (
    "TracerouteResult",
)

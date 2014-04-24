import logging

from .base import Result, ValidationMixin

class Packet(ValidationMixin):
    """
    origin: The `from` value, if any
    rtt:    Return trip time
    size:   The packet size
    ttl:    Time to live
    """

    def __init__(self, data):

        self.origin = None
        self.rtt    = None
        self.size   = None
        self.ttl    = None

        try:
            self.origin = data["from"]
        except KeyError:
            pass

        try:
            self.rtt = round(float(data["rtt"]), 3)
        except (KeyError, ValueError):
            pass

        try:
            self.size = int(data["size"])
        except KeyError:
            pass

        try:
            self.ttl = int(data["ttl"])
        except KeyError:
            pass

    def __str__(self):
        return self.origin


class Hop(ValidationMixin):
    """
    index:   The hop number
    packets: A list of packet objects
    """

    def __init__(self, data):

        self.index = None
        try:
            self.index = data["hop"]
        except KeyError:
            pass

        self.packets = []
        for packet in data["result"]:
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
        self.origin              = self.ensure("from",     str)
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

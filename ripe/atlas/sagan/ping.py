from .base import Result, ResultParseError, ParsingDict

class Packet(ParsingDict):

    def __init__(self, data, default_ttl, default_source_address, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.rtt = None
        self.dup = False
        self.ttl = None

        self.source_address = data.get(
            "src_addr",
            data.get(
                "srcaddr", default_source_address
            )
        )

        if "rtt" in data:
            try:
                self.rtt = round(float(data["rtt"]), 3)
            except (ValueError, TypeError):
                raise ResultParseError(
                    'RTT "{rtt}" does not appear to be a float'.format(
                        rtt=data["rtt"]
                    )
                )

        if self.rtt:
            self.ttl = default_ttl
            if "ttl" in data:
                try:
                    self.ttl = int(data["ttl"])
                except (ValueError, TypeError):
                    raise ResultParseError(
                        'TTL "{ttl}" does not appear to be an integer'.format(
                            ttl=data["ttl"]
                        )
                    )

        if "dup" in data:
            self.dup = True

    def __str__(self):
        return str(self.rtt)


class PingResult(Result):
    """
    Ping measurement result class
    """

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.af = self.ensure("af", int)
        self.duplicates = self.ensure("dup", int)
        self.rtt_average = self.ensure("avg", float)
        self.rtt_max = self.ensure("max", float)
        self.rtt_min = self.ensure("min", float)
        self.packets_sent = self.ensure("sent", int)
        self.packets_received = self.ensure("rcvd", int)
        self.packet_size = self.ensure("size", int)
        self.destination_name = self.ensure("dst_name", str)
        self.destination_address = self.ensure("dst_addr", str)
        self.step = self.ensure("step", int)
        self.rtt_median = None  # Redefined in self._set_rtt_median()
        self.packets = []

        if self.rtt_average < 0:
            self.rtt_average = self.rtt_min = self.rtt_max = None

        if 0 < self.firmware < 4460:
            self.af = self.ensure("pf", int)

        self.protocol = self.clean_protocol(self.ensure("proto", str))

        if 0 < self.firmware < 4460:
            self.destination_address = self.ensure("addr", str)
            self.destination_name = self.ensure("name", str)
            self.packet_size = None
        elif 0 < self.firmware < 4570 and self.protocol == self.PROTOCOL_ICMP:
            self.packet_size -= 8

        if self.af is None and self.destination_address:
            self.af = 4
            if ":" in self.destination_address:
                self.af = 6

        if self.rtt_average:
            self.rtt_average = round(self.rtt_average, 3)

        self._parse_packets(**kwargs)
        self._set_rtt_median()

    def _parse_packets(self, **kwargs):

        source_address = self.raw_data.get(
            "src_addr", self.raw_data.get("srcaddr")
        )
        for packet in self.ensure("result", list, []):
            self.packets.append(
                Packet(
                    packet,
                    self.ensure("ttl", int),
                    source_address,
                    **kwargs
                )
            )

    def _set_rtt_median(self):
        packets = sorted([
            p.rtt for p in self.packets if p.rtt is not None and p.dup is False
        ])
        self.rtt_median = self.calculate_median(packets)

__all__ = (
    "PingResult",
)

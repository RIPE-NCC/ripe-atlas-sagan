from .base import Result, ResultParseError, ValidationMixin


class Packet(ValidationMixin):
    """Model for data structure of each packet for a NTP result."""

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.raw_data = data
        self.rtt = None
        self.offset = None

        if "rtt" not in data:
            return

        try:
            self.rtt = round(float(data["rtt"]), 3)
        except (ValueError, TypeError):
            raise ResultParseError(
                'RTT "{rtt}" does not appear to be a float'.format(rtt=data["rtt"])
            )

        self.final_timestamp = self.ensure("final-ts", float)
        self.offset = self.ensure("offset", float)
        self.origin_timestamp = self.ensure("origin-ts", float)
        self.receive_timestamp = self.ensure("receive-ts", float)
        self.transmit_timestamp = self.ensure("transmit-ts", float)

    def __str__(self):
        return "{rtt}|{offset}".format(rtt=self.rtt, offset=self.offset)


class NtpResult(Result):
    """
    Subclass to cover ntp type measurement results.
    """

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.rtt_median = None
        self.offset_median = None
        self.af = self.ensure("af", int)
        self.protocol = self.ensure("proto", str)
        self.destination_address = self.ensure("dst_addr", str)
        self.destination_name = self.ensure("dst_name", str)
        self.source_address = self.ensure("src_addr", str)
        self.end_time = self.ensure("endtime",  "datetime")
        self.leap_second_indicator = self.ensure("li", str)
        self.mode = self.ensure("mode", str)
        self.poll = self.ensure("poll", int)
        self.precision = self.ensure("precision", float)
        self.reference_id = self.ensure("ref-id", str)
        self.reference_time = self.ensure("ref-ts", float)
        self.root_delay = self.ensure("root-delay", int)
        self.root_dispersion = self.ensure("root-dispersion", float)
        self.stratum = self.ensure("stratum", int)
        self.version = self.ensure("version", int)

        self.packets = []

        if "result" not in self.raw_data:
            self._handle_malformation("No result value found")
            return

        for response in self.raw_data["result"]:
            self.packets.append(Packet(response, **kwargs))

        self._set_medians()

    def _set_medians(self):
        """Sets median values for rtt and offset of the result packets."""
        rtts = sorted([p.rtt for p in self.packets if p.rtt is not None])
        self.rtt_median = self.calculate_median(rtts)
        offsets = sorted(
            [p.offset for p in self.packets if p.offset is not None]
        )
        self.offset_median = self.calculate_median(offsets)


__all__ = (
    "NtpResult"
)

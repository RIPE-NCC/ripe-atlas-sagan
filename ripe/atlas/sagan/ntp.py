# Copyright (c) 2016 RIPE NCC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import UTC

from .base import Result, ResultParseError, ParsingDict


class Packet(ParsingDict):
    """
    Model for data structure of each packet for a NTP result.
    """

    NTP_EPOCH = datetime(1900, 1, 1, tzinfo=UTC)

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.raw_data = data
        self.rtt = None
        self.offset = None

        if "rtt" not in data:
            return

        try:
            self.rtt = round(float(data["rtt"]), 3)
        except (ValueError, TypeError):
            raise ResultParseError(
                'RTT "{rtt}" does not appear to be a float'.format(
                    rtt=data["rtt"])
            )

        self.offset = self.ensure("offset", float)
        self.final_timestamp = self.ensure("final-ts", float)
        self.origin_timestamp = self.ensure("origin-ts", float)
        self.received_timestamp = self.ensure("receive-ts", float)
        self.transmitted_timestamp = self.ensure("transmit-ts", float)

        # Caching

        self._final_time = None
        self._origin_time = None
        self._received_time = None
        self._transmitted_time = None

    def __str__(self):
        return "{rtt}|{offset}".format(rtt=self.rtt, offset=self.offset)

    @property
    def final_time(self):
        if not self._final_time and self.final_timestamp:
            self._final_time = self.NTP_EPOCH + relativedelta(
                seconds=self.final_timestamp)
        return self._final_time

    @property
    def origin_time(self):
        if not self._origin_time and self.origin_timestamp:
            self._origin_time = self.NTP_EPOCH + relativedelta(
                seconds=self.origin_timestamp)
        return self._origin_time

    @property
    def received_time(self):
        if not self._received_time and self.received_timestamp:
            self._received_time = self.NTP_EPOCH + relativedelta(
                seconds=self.received_timestamp)
        return self._received_time

    @property
    def transmitted_time(self):
        if not self._transmitted_time and self.transmitted_timestamp:
            self._transmitted_time = self.NTP_EPOCH + relativedelta(
                    seconds=self.transmitted_timestamp)
        return self._transmitted_time


class NtpResult(Result):
    """
    Subclass to cover ntp type measurement results.
    """

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.rtt_median = None
        self.rtt_min = None
        self.rtt_max = None
        self.offset_median = None
        self.offset_min = None
        self.offset_max = None

        self.af = self.ensure("af", int)
        self.protocol = self.ensure("proto", str)
        self.destination_address = self.ensure("dst_addr", str)
        self.destination_name = self.ensure("dst_name", str)
        self.source_address = self.ensure("src_addr", str)
        self.end_time = self.ensure("endtime", "datetime")
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

        self._set_medians_and_extremes()

    def _set_medians_and_extremes(self):
        """
        Sets median values for rtt and the offset of result packets.
        """

        rtts = sorted([p.rtt for p in self.packets if p.rtt is not None])
        if rtts:
            self.rtt_min = rtts[0]
            self.rtt_max = rtts[-1]
            self.rtt_median = self.calculate_median(rtts)

        offsets = sorted(
            [p.offset for p in self.packets if p.offset is not None]
        )
        if offsets:
            self.offset_min = offsets[0]
            self.offset_max = offsets[-1]
            self.offset_median = self.calculate_median(offsets)


__all__ = (
    "NtpResult"
)

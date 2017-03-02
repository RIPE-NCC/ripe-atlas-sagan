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

import logging

from calendar import timegm

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
        self.objects = self.ensure("obj", list)


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
        packet_rtts = []
        if "result" in self.raw_data:
            for raw_packet in self.raw_data["result"]:
                if "late" not in raw_packet:
                    packet = Packet(raw_packet, **kwargs)
                    if packet.rtt:
                        packet_rtts.append(packet.rtt)
                    self.packets.append(packet)
        self.median_rtt = Result.calculate_median(packet_rtts)

    def __str__(self):
        return str(self.index)


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

        # Used by a few response tests below
        self.destination_ip_responded = False
        self.last_hop_responded = False
        self.is_success = False
        self.last_hop_errors = []

        self._parse_hops(**kwargs)  # Sets hops, last_median_rtt, and total_hops

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

    def set_destination_ip_responded(self, last_hop):
        """Sets the flag if destination IP responded."""
        if not self.destination_address:
            return

        for packet in last_hop.packets:
            if packet.origin and \
                    self.destination_address == packet.origin:
                self.destination_ip_responded = True
                break

    def set_last_hop_responded(self, last_hop):
        """Sets the flag if last hop responded."""
        for packet in last_hop.packets:
            if packet.rtt:
                self.last_hop_responded = True
                break

    def set_is_success(self, last_hop):
        """Sets the flag if traceroute result is successfull or not."""
        for packet in last_hop.packets:
            if packet.rtt and not packet.is_error:
                self.is_success = True
                break
        else:
            self.set_last_hop_errors(last_hop)

    def set_last_hop_errors(self, last_hop):
        """Sets the last hop's errors."""
        if last_hop.is_error:
            self.last_hop_errors.append(last_hop.error_message)
            return

        for packet in last_hop.packets:
            if packet.is_error:
                self.last_hop_errors.append(packet.error_message)

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

    def _parse_hops(self, parse_all_hops=True, **kwargs):

        try:
            hops = self.raw_data["result"]
            assert(isinstance(hops, list))
        except (KeyError, AssertionError):
            self._handle_malformation("Legacy formats not supported")
            return

        num_hops = len(hops)
        # Go through the hops in reverse so that if
        # parse_all_hops is False we can stop processing as
        # soon as possible.
        for index, raw_hop in reversed(list(enumerate(hops))):

            hop = Hop(raw_hop, **kwargs)

            # If last hop set several useful attributes
            if index + 1 == num_hops:
                self.set_destination_ip_responded(hop)
                self.set_last_hop_responded(hop)
                self.set_is_success(hop)
                # We always store the last hop
                self.hops.insert(0, hop)
            elif parse_all_hops:
                self.hops.insert(0, hop)

            if hop.median_rtt and not self.last_median_rtt:
                self.last_median_rtt = hop.median_rtt
                if not parse_all_hops:
                    # Now that we have the last RTT we can stop
                    break
        self.total_hops = num_hops


__all__ = (
    "TracerouteResult",
)

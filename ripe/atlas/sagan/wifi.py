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

from .base import Result, ParsingDict


class WPASupplicant(ParsingDict):

    def __init__(self, data, **kwargs):

        ParsingDict.__init__(self, **kwargs)

        self.address = data.get("address")
        self.bssid = data.get("bssid")
        self.connect_time = data.get("connect-time")
        self.group_cipher = data.get("group_cipher")
        self.wpa_supplicant_id = data.get("id")
        self.ip_address = data.get("ip_address")
        self.key_management = data.get("key_mgmt")
        self.mode = data.get("mode")
        self.pairwise_cipher = data.get("pairwise_cipher")
        self.ssid = data.get("ssid")
        self.wpa_state = data.get("wpa_state")


class WiFiResult(Result):
    """
    WiFi measurement result class
    """

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.wpa_supplicant = WPASupplicant(
            data["wpa_supplicant"], **kwargs
        )

__all__ = (
    "WiFiResult",
)

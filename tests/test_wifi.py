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

from ripe.atlas.sagan import Result
from ripe.atlas.sagan.wifi import WiFiResult


def test_wifi():
    raw_data = {
        "bundle": 1463495978,
        "from": "2001:67c:2e8:ffe1:eade:27ff:fe69:e6f0",
        "fw": "4733",
        "group_id": 1021275,
        "msm_id": 1021275,
        "msm_name": "WiFi",
        "prb_id": 105,
        "timestamp": 1463495978,
        "type": "wifi",
        "wpa_supplicant": {
            "address": "ea:de:27:69:e6:f0",
            "bssid": "08:ea:44:3b:6d:14",
            "connect-time": "2",
            "group_cipher": "CCMP",
            "id": "0",
            "ip_address": "193.0.10.126",
            "key_mgmt": "WPA2-PSK",
            "mode": "station",
            "pairwise_cipher": "CCMP",
            "ssid": "guestnet",
            "wpa_state": "COMPLETED"
        }
    }

    result = Result.get(raw_data)
    assert(isinstance(result, WiFiResult))
    assert(result.bundle == 1463495978)
    assert(result.origin == "2001:67c:2e8:ffe1:eade:27ff:fe69:e6f0")
    assert(result.firmware == 4733)
    assert(result.group_id == 1021275)
    assert(result.wpa_supplicant.address == "ea:de:27:69:e6:f0")
    assert(result.wpa_supplicant.bssid == "08:ea:44:3b:6d:14")
    assert(result.wpa_supplicant.connect_time == "2")
    assert(result.wpa_supplicant.group_cipher == "CCMP")
    assert(result.wpa_supplicant.wpa_supplicant_id == "0")
    assert(result.wpa_supplicant.ip_address == "193.0.10.126")
    assert(result.wpa_supplicant.key_management == "WPA2-PSK")
    assert(result.wpa_supplicant.mode == "station")
    assert(result.wpa_supplicant.pairwise_cipher == "CCMP")
    assert(result.wpa_supplicant.ssid == "guestnet")
    assert(result.wpa_supplicant.wpa_state == "COMPLETED")


def test_wifi_error():
    raw_data = {
        "bundle": 1463493022,
        "error": "wpa timeout",
        "from": "2001:67c:2e8:ffe1:eade:27ff:fe69:e6f0",
        "fw": "4733",
        "group_id": 1021275,
        "msm_id": 1021275,
        "msm_name": "WiFi",
        "prb_id": 105,
        "timestamp": 1463493023,
        "type": "wifi",
        "wpa_supplicant": {"connect-time": "11"}
    }

    result = Result.get(raw_data)
    assert(isinstance(result, WiFiResult))
    assert(result.bundle == 1463493022)
    assert(result.origin == "2001:67c:2e8:ffe1:eade:27ff:fe69:e6f0")
    assert(result.firmware == 4733)
    assert(result.group_id == 1021275)
    assert(result.created_timestamp == 1463493023)
    assert(result.wpa_supplicant.address is None)
    assert(result.wpa_supplicant.bssid is None)
    assert(result.wpa_supplicant.connect_time == "11")
    assert(result.wpa_supplicant.group_cipher is None)
    assert(result.wpa_supplicant.wpa_supplicant_id is None)
    assert(result.wpa_supplicant.ip_address is None)
    assert(result.wpa_supplicant.key_management is None)
    assert(result.wpa_supplicant.mode is None)
    assert(result.wpa_supplicant.pairwise_cipher is None)
    assert(result.wpa_supplicant.ssid is None)
    assert(result.wpa_supplicant.wpa_state is None)

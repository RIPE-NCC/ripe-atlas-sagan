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
from ripe.atlas.sagan.ntp import NtpResult

def test_ntp_valid():
    result = (
        '{"af":4,"dst_addr":"193.0.0.229","dst_name":"atlas","from":"193.0.0.78","fw":4670,'
        '"group_id":1020237,"li":"no","lts":-1,"mode":"server","msm_id":1020237,"msm_name":"Ntp",'
        '"poll":1,"prb_id":71,"precision":0.0000019074,"proto":"UDP","ref-id":"GPS",'
        '"ref-ts":3627199357.7446351051,"result":['
            '{"final-ts":3627199379.8182010651,"offset":-8.363271,"origin-ts":3627199379.7962741852,'
            '"receive-ts":3627199388.1704945564,"rtt":0.021899,"transmit-ts":3627199388.170522213},'
            '{"final-ts":3627199379.831638813,"offset":-8.36871,"origin-ts":3627199379.8214530945,'
            '"receive-ts":3627199388.1952428818,"rtt":0.01016,"transmit-ts":3627199388.195268631},'
            '{"final-ts":3627199379.8474769592,"offset":-8.372775,"origin-ts":3627199379.8454480171,'
            '"receive-ts":3627199388.2192249298,"rtt":0.002004,"transmit-ts":3627199388.2192502022}'
        '],'
        '"root-delay":0,"root-dispersion":0.00140381,"src_addr":"10.0.2.12","stratum":1,'
        '"timestamp":1418210579,"type":"ntp","version":4}'
    )
    result = Result.get(result)
    assert(isinstance(result, NtpResult))
    assert(result.af == 4)
    assert(result.firmware == 4670)
    assert(result.destination_address == "193.0.0.229")
    assert(result.destination_name == "atlas")
    assert(result.source_address == "10.0.2.12")
    assert(result.origin == "193.0.0.78")
    assert(result.leap_second_indicator == "no")
    assert(result.mode == "server")
    assert(result.poll == 1)
    assert(result.precision == 1.9074e-06)
    assert(result.protocol == "UDP")
    assert(result.reference_id == "GPS")
    assert(result.reference_time == 3627199357.7446351051)
    assert(result.root_delay == 0)
    assert(round(result.root_dispersion, 8) == 0.00140381)
    assert(result.stratum == 1)
    assert(result.version == 4)
    assert(result.packets[0].final_timestamp == 3627199379.8182010651)
    assert(result.packets[0].final_time.isoformat() == "2014-12-10T11:22:59.818201+00:00")
    assert(result.packets[0].offset == -8.363271)
    assert(result.packets[0].rtt == 0.022)
    assert(result.packets[0].origin_timestamp == 3627199379.7962741852)
    assert(result.packets[0].origin_time.isoformat() == "2014-12-10T11:22:59.796274+00:00")
    assert(result.packets[0].received_timestamp == 3627199388.1704945564)
    assert(result.packets[0].received_time.isoformat() == "2014-12-10T11:23:08.170495+00:00")
    assert(result.packets[0].transmitted_timestamp == 3627199388.170522213)
    assert(result.packets[0].transmitted_time.isoformat() == "2014-12-10T11:23:08.170522+00:00")
    assert(result.rtt_min == 0.002)
    assert(result.rtt_max == 0.022)
    assert(result.rtt_median == 0.01)
    assert(result.offset_min == -8.372775)
    assert(result.offset_max == -8.363271)
    assert(result.offset_median == -8.36871)


def test_ntp_timeout():
    result = (
        '{ "msm_id":"1020235", "fw":4661, "lts":76, "timestamp":1418196642, "dst_name":"atlas", '
        '"prb_id":71, "dst_addr":"193.0.6.139", "src_addr":"193.0.10.127", "proto":"UDP", "af": 4,'
        '"from": "193.0.0.78", "type": "ntp", "result": '
        '[ { "x":"*" }, { "x":"*" }, { "x":"*" } ] '
        '}'
    )
    result = Result.get(result)
    assert(isinstance(result, NtpResult))
    assert(result.af == 4)
    assert(result.firmware == 4661)
    assert(result.destination_address == "193.0.6.139")
    assert(result.destination_name == "atlas")
    assert(result.source_address == "193.0.10.127")
    assert(result.origin == "193.0.0.78")
    assert(result.leap_second_indicator is None)
    assert(result.stratum is None)
    assert(result.rtt_median is None)
    assert(result.offset_median is None)
    assert(getattr(result.packets[0], "final_timestamp", None) is None)
    assert(getattr(result.packets[0], "final_times", None) is None)
    assert(getattr(result.packets[0], "origin_timestamp", None) is None)
    assert(getattr(result.packets[0], "origin_time", None) is None)
    assert(getattr(result.packets[0], "transmitted_timestamp", None) is None)
    assert(getattr(result.packets[0], "transmitted_time", None) is None)
    assert(getattr(result.packets[0], "received_timestamp", None) is None)
    assert(getattr(result.packets[0], "received_time", None) is None)
    assert(result.packets[0].offset is None)
    assert(result.packets[0].rtt is None)


def test_ntp_error():
    result = (
        '{ "msm_id":"1020235", "fw":4661, "lts":76, "timestamp":1418196642, "dst_name":"atlas", '
        '"prb_id":71, "dst_addr":"193.0.6.139", "src_addr":"193.0.10.127", "proto":"UDP", "af": 4,'
        '"from": "193.0.0.78", "type": "ntp", "result": '
        '[ { "error":"error-example" }, { "error":"error-example" }, { "x":"*" } ] '
        '}'
    )
    result = Result.get(result)
    assert(isinstance(result, NtpResult))
    assert(result.af == 4)
    assert(result.firmware == 4661)
    assert(result.destination_address == "193.0.6.139")
    assert(result.destination_name == "atlas")
    assert(result.source_address == "193.0.10.127")
    assert(result.origin == "193.0.0.78")
    assert(result.leap_second_indicator is None)
    assert(result.stratum is None)
    assert(result.rtt_median is None)
    assert(result.offset_median is None)
    assert(getattr(result.packets[0], "final_timestamp", None) is None)
    assert(getattr(result.packets[0], "final_time", None) is None)
    assert(getattr(result.packets[0], "origin_timestamp", None) is None)
    assert(getattr(result.packets[0], "origin_time", None) is None)
    assert(getattr(result.packets[0], "transmitted_timestamp", None) is None)
    assert(getattr(result.packets[0], "transmitted_time", None) is None)
    assert(getattr(result.packets[0], "received_timestamp", None) is None)
    assert(getattr(result.packets[0], "received_time", None) is None)
    assert(result.packets[0].offset is None)
    assert(result.packets[0].rtt is None)

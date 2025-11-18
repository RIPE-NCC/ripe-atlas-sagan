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
from ripe.atlas.sagan.traceroute import TracerouteResult, Hop, Packet


def test_traceroute_4460():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1340329208,"from":"107.3.81.49","fw":4460,"msm_id":1000157,"paris_id":2,"prb_id":190,"proto":"UDP","result":[{"hop":1,"result":[{"from":"192.168.1.1","rtt":2.7829999999999999,"size":96,"ttl":64},{"from":"192.168.1.1","rtt":2.4500000000000002,"size":96,"ttl":64},{"from":"192.168.1.1","rtt":2.3210000000000002,"size":96,"ttl":64}]},{"hop":2,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":3,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":4,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":5,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":6,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"192.168.1.107","timestamp":1340329190,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2012-06-22T01:40:08+00:00")
    assert(result.origin == "107.3.81.49")
    assert(result.firmware == 4460)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 190)
    assert(result.paris_id == 2)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 7)
    assert(result.last_median_rtt == 2.45)
    assert(result.ip_path[3][1] is None)
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin is None)
    assert(result.hops[3].packets[1].rtt is None)
    assert(result.hops[3].packets[1].size is None)
    assert(result.hops[3].packets[2].ttl is None)
    assert(result.hops[-1].index == 255)


def test_traceroute_4470():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1344429608,"from":"216.66.30.82","fw":4470,"msm_id":1000157,"paris_id":1,"prb_id":426,"proto":"UDP","result":[{"hop":1,"result":[{"from":"216.66.30.81","rtt":1.9650000000000001,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":2.004,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":1.855,"size":56,"ttl":255}]},{"hop":2,"result":[{"from":"64.71.128.50","rtt":1.843,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":2.004,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":1.8580000000000001,"size":56,"ttl":63}]},{"hop":3,"result":[{"from":"213.248.79.129","rtt":2.4220000000000002,"size":56,"ttl":253},{"from":"213.248.79.129","rtt":1.8700000000000001,"size":56,"ttl":253},{"from":"213.248.79.129","rtt":1.8740000000000001,"size":56,"ttl":253}]},{"hop":4,"result":[{"from":"80.91.250.102","rtt":2.327,"size":56,"ttl":251},{"from":"80.91.250.102","rtt":2.0760000000000001,"size":56,"ttl":251},{"from":"80.91.250.102","rtt":2.3210000000000002,"size":56,"ttl":251}]},{"hop":5,"result":[{"from":"213.155.135.79","rtt":2.7010000000000001,"size":56,"ttl":251},{"from":"213.155.135.79","rtt":2.5030000000000001,"size":56,"ttl":251},{"from":"213.155.135.79","rtt":9.9969999999999999,"size":56,"ttl":251}]},{"hop":6,"result":[{"from":"209.58.26.89","rtt":2.5760000000000001,"size":56,"ttl":250},{"from":"209.58.26.89","rtt":2.6640000000000001,"size":56,"ttl":250},{"from":"209.58.26.89","rtt":14.355,"size":56,"ttl":250}]},{"hop":7,"result":[{"from":"195.219.243.21","rtt":71.448999999999998,"size":56,"ttl":249},{"from":"195.219.243.21","rtt":71.435000000000002,"size":56,"ttl":249},{"from":"195.219.243.21","rtt":71.311000000000007,"size":56,"ttl":249}]},{"hop":8,"result":[{"from":"80.231.131.10","rtt":71.504000000000005,"size":56,"ttl":249},{"from":"80.231.131.10","rtt":71.540000000000006,"size":56,"ttl":249},{"from":"80.231.131.10","rtt":71.484999999999999,"size":56,"ttl":249}]},{"hop":9,"result":[{"from":"195.219.144.118","rtt":197.21299999999999,"size":56,"ttl":246},{"from":"195.219.144.118","rtt":222.99100000000001,"size":56,"ttl":246},{"from":"195.219.144.118","rtt":196.874,"size":56,"ttl":246}]},{"hop":10,"result":[{"from":"59.163.16.13","ittl":0,"rtt":197.03399999999999,"size":56,"ttl":245},{"from":"59.163.16.13","ittl":0,"rtt":200.82900000000001,"size":56,"ttl":245},{"from":"59.163.16.13","ittl":0,"rtt":196.88900000000001,"size":56,"ttl":245}]},{"hop":11,"result":[{"from":"59.163.16.13","rtt":197.04599999999999,"size":56,"ttl":245},{"from":"59.163.16.13","rtt":196.92699999999999,"size":56,"ttl":245},{"from":"59.163.16.13","rtt":196.96199999999999,"size":56,"ttl":245}]},{"hop":12,"result":[{"from":"203.197.33.148","rtt":197.33099999999999,"size":56,"ttl":245},{"from":"203.197.33.148","rtt":197.398,"size":56,"ttl":245},{"from":"203.197.33.148","rtt":197.34800000000001,"size":56,"ttl":245}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":17,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"216.66.30.82","timestamp":1344429586,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2012-08-08T12:40:08+00:00")
    assert(result.origin == "216.66.30.82")
    assert(result.firmware == 4470)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 426)
    assert(result.paris_id == 1)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 18)
    assert(result.last_median_rtt == 197.348)
    assert(result.last_rtt == 197.348)  # Deprecation test
    assert(result.ip_path[3][1] == "80.91.250.102")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "80.91.250.102")
    assert(result.hops[3].packets[1].rtt == 2.076)
    assert(result.hops[3].packets[1].size == 56)
    assert(result.hops[3].packets[2].ttl == 251)
    assert(result.hops[-1].index == 255)


def test_traceroute_4480():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1349840414,"from":"216.66.30.82","fw":4480,"msm_id":1000157,"paris_id":1,"prb_id":426,"proto":"UDP","result":[{"hop":1,"result":[{"from":"216.66.30.81","rtt":2.133,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":1.8360000000000001,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":1.8400000000000001,"size":56,"ttl":255}]},{"hop":2,"result":[{"from":"64.71.128.50","rtt":3.5990000000000002,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":8.4779999999999998,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":3.6499999999999999,"size":56,"ttl":63}]},{"hop":3,"result":[{"from":"72.52.92.102","rtt":7.5289999999999999,"size":56,"ttl":62},{"from":"72.52.92.102","rtt":1.847,"size":56,"ttl":62},{"from":"72.52.92.102","rtt":1.8380000000000001,"size":56,"ttl":62}]},{"hop":4,"result":[{"from":"213.248.101.145","rtt":1.8340000000000001,"size":56,"ttl":252},{"from":"213.248.101.145","rtt":1.9830000000000001,"size":56,"ttl":252},{"from":"213.248.101.145","rtt":1.9279999999999999,"size":56,"ttl":252}]},{"hop":5,"result":[{"from":"80.91.248.177","rtt":2.3290000000000002,"size":56,"ttl":250},{"from":"80.91.248.177","rtt":2.2400000000000002,"size":56,"ttl":250},{"from":"80.91.248.177","rtt":2.2370000000000001,"size":56,"ttl":250}]},{"hop":6,"result":[{"from":"213.155.135.79","rtt":22.812999999999999,"size":56,"ttl":251},{"from":"213.155.135.79","rtt":22.091000000000001,"size":56,"ttl":251},{"from":"213.155.135.79","rtt":2.3100000000000001,"size":56,"ttl":251}]},{"hop":7,"result":[{"from":"213.248.100.178","rtt":2.5710000000000002,"size":56,"ttl":250},{"from":"213.248.100.178","rtt":2.5049999999999999,"size":56,"ttl":250},{"x":"*"}]},{"hop":8,"result":[{"from":"195.219.243.21","rtt":71.701999999999998,"size":56,"ttl":249},{"from":"195.219.243.21","rtt":71.295000000000002,"size":56,"ttl":249},{"from":"195.219.243.21","rtt":71.734999999999999,"size":56,"ttl":249}]},{"hop":9,"result":[{"from":"80.231.131.10","rtt":71.626000000000005,"size":56,"ttl":249},{"from":"80.231.131.10","rtt":71.313000000000002,"size":56,"ttl":249},{"from":"80.231.131.10","rtt":71.253,"size":56,"ttl":249}]},{"hop":10,"result":[{"from":"195.219.144.62","rtt":205.416,"size":56,"ttl":245},{"from":"195.219.144.62","rtt":200.53,"size":56,"ttl":245},{"from":"195.219.144.62","rtt":200.39500000000001,"size":56,"ttl":245}]},{"hop":11,"result":[{"from":"59.163.55.149","ittl":0,"rtt":200.755,"size":56,"ttl":244},{"from":"59.163.55.149","ittl":0,"rtt":200.41,"size":56,"ttl":244},{"from":"59.163.55.149","ittl":0,"rtt":200.40799999999999,"size":56,"ttl":244}]},{"hop":12,"result":[{"from":"59.163.55.149","rtt":200.572,"size":56,"ttl":244},{"from":"59.163.55.149","rtt":200.584,"size":56,"ttl":244},{"from":"59.163.55.149","rtt":200.673,"size":56,"ttl":244}]},{"hop":13,"result":[{"from":"203.197.33.148","rtt":198.666,"size":56,"ttl":244},{"from":"203.197.33.148","rtt":198.83699999999999,"size":56,"ttl":244},{"from":"203.197.33.148","rtt":198.55099999999999,"size":56,"ttl":244}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":17,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":18,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"216.66.30.82","timestamp":1349840391,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2012-10-10T03:40:14+00:00")
    assert(result.origin == "216.66.30.82")
    assert(result.firmware == 4480)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 426)
    assert(result.paris_id == 1)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 19)
    assert(result.last_median_rtt == 198.666)
    assert(result.ip_path[3][1] == "213.248.101.145")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "213.248.101.145")
    assert(result.hops[3].packets[1].rtt == 1.983)
    assert(result.hops[3].packets[1].size == 56)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_4500():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1361436009,"from":"192.172.226.243","fw":4500,"msm_id":1000157,"paris_id":1,"prb_id":319,"proto":"UDP","result":[{"hop":1,"result":[{"from":"192.172.226.252","rtt":2.0209999999999999,"size":56,"ttl":254},{"from":"192.172.226.252","rtt":1.7589999999999999,"size":56,"ttl":254},{"from":"192.172.226.252","rtt":1.7589999999999999,"size":56,"ttl":254}]},{"hop":2,"result":[{"from":"192.12.207.61","rtt":1.8999999999999999,"size":56,"ttl":253},{"from":"192.12.207.61","rtt":1.7549999999999999,"size":56,"ttl":253},{"from":"192.12.207.61","rtt":1.9079999999999999,"size":56,"ttl":253}]},{"hop":3,"result":[{"from":"137.164.23.129","rtt":1.859,"size":56,"ttl":253},{"from":"137.164.23.129","rtt":1.7669999999999999,"size":56,"ttl":253},{"from":"137.164.23.129","rtt":1.9099999999999999,"size":56,"ttl":253}]},{"hop":4,"result":[{"from":"137.164.47.110","rtt":10.246,"size":56,"ttl":252},{"from":"137.164.47.110","rtt":9.8439999999999994,"size":56,"ttl":252},{"from":"137.164.47.110","rtt":10.106999999999999,"size":56,"ttl":252}]},{"hop":5,"result":[{"from":"137.164.46.57","rtt":11.597,"size":56,"ttl":251},{"from":"137.164.46.57","rtt":11.255000000000001,"size":56,"ttl":251},{"from":"137.164.46.57","rtt":11.279999999999999,"size":56,"ttl":251}]},{"hop":6,"result":[{"from":"137.164.47.136","rtt":11.24,"size":56,"ttl":250},{"from":"137.164.47.136","rtt":11.099,"size":56,"ttl":250},{"from":"137.164.47.136","rtt":11.096,"size":56,"ttl":250}]},{"hop":7,"result":[{"from":"4.59.48.177","rtt":11.287000000000001,"size":56,"ttl":248},{"from":"4.59.48.177","rtt":11.201000000000001,"size":56,"ttl":248},{"from":"4.59.48.177","rtt":11.204000000000001,"size":56,"ttl":248}]},{"hop":8,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":9,"result":[{"from":"4.68.62.118","rtt":11.532999999999999,"size":56,"ttl":247},{"from":"4.68.62.118","rtt":11.298999999999999,"size":56,"ttl":247},{"from":"4.68.62.118","rtt":11.474,"size":56,"ttl":247}]},{"hop":10,"result":[{"from":"66.110.59.1","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":407904,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":23.974,"size":168,"ttl":241},{"from":"66.110.59.1","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":407904,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":27.079000000000001,"size":168,"ttl":241},{"from":"66.110.59.1","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":407904,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":23.843,"size":168,"ttl":241}]},{"hop":11,"result":[{"from":"66.198.127.9","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":371728,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":23.997,"size":168,"ttl":242},{"from":"66.198.127.9","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":371728,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":46.223999999999997,"size":168,"ttl":242},{"from":"66.198.127.9","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":371728,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":24.052,"size":168,"ttl":242}]},{"hop":12,"result":[{"from":"66.198.127.2","rtt":23.966999999999999,"size":56,"ttl":244},{"from":"66.198.127.2","rtt":24.617000000000001,"size":56,"ttl":244},{"from":"66.198.127.2","rtt":24.991,"size":56,"ttl":244}]},{"hop":13,"result":[{"from":"66.198.144.2","rtt":268.68200000000002,"size":56,"ttl":233},{"from":"66.198.144.2","rtt":268.93299999999999,"size":56,"ttl":233},{"from":"66.198.144.2","rtt":268.45999999999998,"size":56,"ttl":233}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":17,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":18,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"192.172.226.243","timestamp":1361435986,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2013-02-21T08:40:09+00:00")
    assert(result.origin == "192.172.226.243")
    assert(result.firmware == 4500)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 319)
    assert(result.paris_id == 1)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 19)
    assert(result.last_median_rtt == 268.682)
    assert(result.ip_path[3][1] == "137.164.47.110")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "137.164.47.110")
    assert(result.hops[3].packets[1].rtt == 9.844)
    assert(result.hops[3].packets[1].size == 56)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_4520():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1365381605,"from":"216.66.30.82","fw":4520,"msm_id":1000157,"paris_id":12,"prb_id":426,"proto":"UDP","result":[{"hop":1,"result":[{"from":"216.66.30.81","rtt":2.0720000000000001,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":1.7829999999999999,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":1.9399999999999999,"size":56,"ttl":255}]},{"hop":2,"result":[{"from":"64.71.128.50","rtt":8.0690000000000008,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":3.3690000000000002,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":7.891,"size":56,"ttl":63}]},{"hop":3,"result":[{"from":"72.52.92.49","rtt":27.738,"size":56,"ttl":62},{"from":"72.52.92.49","rtt":58.445,"size":56,"ttl":62},{"from":"72.52.92.49","rtt":79.837000000000003,"size":56,"ttl":62}]},{"hop":4,"result":[{"from":"213.248.67.125","rtt":101.46899999999999,"size":56,"ttl":252},{"from":"213.248.67.125","rtt":83.983999999999995,"size":56,"ttl":252},{"from":"213.248.67.125","rtt":1.869,"size":56,"ttl":252}]},{"hop":5,"result":[{"from":"213.155.131.254","rtt":1.8879999999999999,"size":56,"ttl":251},{"from":"213.155.131.254","rtt":1.7869999999999999,"size":56,"ttl":251},{"from":"213.155.131.254","rtt":1.9339999999999999,"size":56,"ttl":251}]},{"hop":6,"result":[{"from":"213.248.100.178","rtt":3.8559999999999999,"size":56,"ttl":249},{"from":"213.248.100.178","rtt":1.7989999999999999,"size":56,"ttl":249},{"from":"213.248.100.178","rtt":1.897,"size":56,"ttl":249}]},{"hop":7,"result":[{"from":"63.243.128.38","rtt":71.748000000000005,"size":56,"ttl":249},{"from":"63.243.128.38","rtt":80.543999999999997,"size":56,"ttl":249},{"from":"63.243.128.38","rtt":71.480000000000004,"size":56,"ttl":249}]},{"hop":8,"result":[{"from":"80.231.131.114","rtt":203.08600000000001,"size":56,"ttl":249},{"from":"80.231.131.114","rtt":202.63,"size":56,"ttl":249},{"from":"80.231.131.114","rtt":202.63999999999999,"size":56,"ttl":249}]},{"hop":9,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":10,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":11,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":12,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"216.66.30.82","timestamp":1365381585,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2013-04-08T00:40:05+00:00")
    assert(result.origin == "216.66.30.82")
    assert(result.firmware == 4520)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 426)
    assert(result.paris_id == 12)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 14)
    assert(result.last_median_rtt == 202.64)
    assert(result.ip_path[3][1] == "213.248.67.125")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "213.248.67.125")
    assert(result.hops[3].packets[1].rtt == 83.984)
    assert(result.hops[3].packets[1].size == 56)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_4550():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1378186817,"from":"24.61.47.146","fw":4550,"msm_id":1000157,"msm_name":"Traceroute","paris_id":1,"prb_id":190,"proto":"UDP","result":[{"hop":1,"result":[{"from":"192.168.11.1","rtt":1.8919999999999999,"size":96,"ttl":64},{"from":"192.168.11.1","rtt":1.75,"size":96,"ttl":64},{"from":"192.168.11.1","rtt":1.744,"size":96,"ttl":64}]},{"hop":2,"result":[{"from":"96.120.64.225","rtt":12.012,"size":56,"ttl":254},{"from":"96.120.64.225","rtt":25.962,"size":56,"ttl":254},{"from":"96.120.64.225","rtt":11.657999999999999,"size":56,"ttl":254}]},{"hop":3,"result":[{"from":"68.85.140.197","rtt":10.077999999999999,"size":56,"ttl":253},{"from":"68.85.140.197","rtt":12.561999999999999,"size":56,"ttl":253},{"from":"68.85.140.197","rtt":14.548999999999999,"size":56,"ttl":253}]},{"hop":4,"result":[{"from":"68.87.144.69","rtt":10.404,"size":56,"ttl":253},{"from":"68.87.144.69","rtt":10.539999999999999,"size":56,"ttl":253},{"from":"68.87.144.69","rtt":10.07,"size":56,"ttl":253}]},{"hop":5,"result":[{"from":"68.85.162.157","rtt":28.190999999999999,"size":96,"ttl":252},{"from":"68.85.162.157","rtt":15.026,"size":96,"ttl":252},{"from":"68.85.162.157","rtt":13.1,"size":96,"ttl":252}]},{"hop":6,"result":[{"from":"68.86.93.185","rtt":40.353000000000002,"size":96,"ttl":250},{"from":"68.86.93.185","rtt":44.490000000000002,"size":96,"ttl":250},{"from":"68.86.93.185","rtt":40.649000000000001,"size":96,"ttl":250}]},{"hop":7,"result":[{"from":"68.86.86.74","rtt":42.399000000000001,"size":96,"ttl":249},{"from":"68.86.86.74","rtt":42.179000000000002,"size":96,"ttl":249},{"from":"68.86.86.74","rtt":46.326000000000001,"size":96,"ttl":249}]},{"hop":8,"result":[{"from":"209.58.26.81","rtt":40.264000000000003,"size":56,"ttl":248},{"from":"209.58.26.81","rtt":37.850999999999999,"size":56,"ttl":248},{"from":"209.58.26.81","rtt":44.194000000000003,"size":56,"ttl":248}]},{"hop":9,"result":[{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":674080,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":273.74099999999999,"size":168,"ttl":239},{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":674080,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":272.11099999999999,"size":168,"ttl":239},{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":674080,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":271.76499999999999,"size":168,"ttl":239}]},{"hop":10,"result":[{"from":"80.231.200.13","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":371312,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":271.88,"size":168,"ttl":240},{"from":"80.231.200.13","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":371312,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":278.21100000000001,"size":168,"ttl":240},{"from":"80.231.200.13","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":371312,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":274.62799999999999,"size":168,"ttl":240}]},{"hop":11,"result":[{"from":"80.231.217.1","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":545488,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":275.60899999999998,"size":168,"ttl":241},{"from":"80.231.217.1","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":545488,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":278.06900000000002,"size":168,"ttl":241},{"from":"80.231.217.1","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":545488,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":276.13799999999998,"size":168,"ttl":241}]},{"hop":12,"result":[{"from":"80.231.217.18","rtt":295.97000000000003,"size":56,"ttl":243},{"from":"80.231.217.18","rtt":284.20299999999997,"size":56,"ttl":243},{"from":"80.231.217.18","rtt":283.91300000000001,"size":56,"ttl":243}]},{"hop":13,"result":[{"from":"180.87.38.6","rtt":268.40899999999999,"size":56,"ttl":237},{"from":"180.87.38.6","rtt":277.73099999999999,"size":56,"ttl":237},{"from":"180.87.38.6","rtt":268.12,"size":56,"ttl":237}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":17,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":18,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"192.168.11.151","timestamp":1378186793,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2013-09-03T05:40:17+00:00")
    assert(result.origin == "24.61.47.146")
    assert(result.firmware == 4550)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 190)
    assert(result.paris_id == 1)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 19)
    assert(result.last_median_rtt == 268.409)
    assert(result.ip_path[3][1] == "68.87.144.69")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "68.87.144.69")
    assert(result.hops[3].packets[1].rtt == 10.54)
    assert(result.hops[3].packets[1].size == 56)
    assert(result.hops[3].packets[2].ttl == 253)
    assert(result.hops[-1].index == 255)


def test_traceroute_4560():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1380595207,"from":"216.66.30.82","fw":4560,"msm_id":1000157,"msm_name":"Traceroute","paris_id":1,"prb_id":426,"proto":"UDP","result":[{"hop":1,"result":[{"from":"216.66.30.81","rtt":137.40299999999999,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":103.331,"size":56,"ttl":255},{"from":"216.66.30.81","rtt":7.6379999999999999,"size":56,"ttl":255}]},{"hop":2,"result":[{"from":"64.71.128.50","rtt":1.756,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":3.1059999999999999,"size":56,"ttl":63},{"from":"64.71.128.50","rtt":1.905,"size":56,"ttl":63}]},{"hop":3,"result":[{"from":"184.105.222.81","rtt":2.0470000000000002,"size":56,"ttl":62},{"from":"184.105.222.81","rtt":2.0569999999999999,"size":56,"ttl":62},{"from":"184.105.222.81","rtt":1.768,"size":56,"ttl":62}]},{"hop":4,"result":[{"from":"213.248.67.125","rtt":1.762,"size":56,"ttl":252},{"from":"213.248.67.125","rtt":1.764,"size":56,"ttl":252},{"from":"213.248.67.125","rtt":62.124000000000002,"size":56,"ttl":252}]},{"hop":5,"result":[{"from":"213.155.130.34","rtt":1.8620000000000001,"size":56,"ttl":251},{"from":"213.155.130.34","rtt":3.028,"size":56,"ttl":251},{"from":"213.155.130.34","rtt":2.9990000000000001,"size":56,"ttl":251}]},{"hop":6,"result":[{"from":"213.248.100.178","rtt":4.25,"size":56,"ttl":250},{"from":"213.248.100.178","rtt":2.512,"size":56,"ttl":250},{"from":"213.248.100.178","rtt":1.869,"size":56,"ttl":250}]},{"hop":7,"result":[{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":310273,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":97.242999999999995,"size":168,"ttl":240},{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":310273,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":111.867,"size":168,"ttl":240},{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":310273,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":96.531999999999996,"size":168,"ttl":240}]},{"hop":8,"result":[{"from":"80.231.130.121","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":798112,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":102.61,"size":168,"ttl":241},{"from":"80.231.130.121","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":798112,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":132.82499999999999,"size":168,"ttl":241},{"from":"80.231.130.121","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":798112,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":103.658,"size":168,"ttl":241}]},{"hop":9,"result":[{"from":"80.231.130.2","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":301041,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":102.482,"size":168,"ttl":242},{"from":"80.231.130.2","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":301041,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":102.691,"size":168,"ttl":242},{"from":"80.231.130.2","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":301041,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":102.435,"size":168,"ttl":242}]},{"hop":10,"result":[{"from":"80.231.217.5","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":302880,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":97.114999999999995,"size":168,"ttl":243},{"from":"80.231.217.5","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":302880,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":96.379000000000005,"size":168,"ttl":243},{"from":"80.231.217.5","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":302880,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":96.712999999999994,"size":168,"ttl":243}]},{"hop":11,"result":[{"from":"80.231.217.2","rtt":168.09700000000001,"size":56,"ttl":245},{"from":"80.231.217.2","rtt":96.829999999999998,"size":56,"ttl":245},{"from":"80.231.217.2","rtt":103.726,"size":56,"ttl":245}]},{"hop":12,"result":[{"from":"80.231.200.26","rtt":198.64599999999999,"size":56,"ttl":244},{"from":"80.231.200.26","rtt":198.21000000000001,"size":56,"ttl":244},{"from":"80.231.200.26","rtt":206.268,"size":56,"ttl":244}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":17,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"216.66.30.82","timestamp":1380595186,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2013-10-01T02:40:07+00:00")
    assert(result.origin == "216.66.30.82")
    assert(result.firmware == 4560)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 426)
    assert(result.paris_id == 1)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 18)
    assert(result.last_median_rtt == 198.646)
    assert(result.ip_path[3][1] == "213.248.67.125")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "213.248.67.125")
    assert(result.hops[3].packets[1].rtt == 1.764)
    assert(result.hops[3].packets[1].size == 56)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_4570():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1392240133,"from":"216.66.30.82","fw":4570,"msm_id":1000157,"msm_name":"Traceroute","paris_id":2,"prb_id":426,"proto":"UDP","result":[{"hop":1,"result":[{"from":"216.66.30.81","rtt":62.367,"size":28,"ttl":255},{"from":"216.66.30.81","rtt":3.038,"size":28,"ttl":255},{"from":"216.66.30.81","rtt":2.895,"size":28,"ttl":255}]},{"hop":2,"result":[{"from":"64.71.128.50","rtt":12.539,"size":28,"ttl":63},{"from":"64.71.128.50","rtt":7.634,"size":28,"ttl":63},{"from":"64.71.128.50","rtt":12.681,"size":28,"ttl":63}]},{"hop":3,"result":[{"from":"184.105.222.81","rtt":12.469,"size":28,"ttl":62},{"from":"184.105.222.81","rtt":6.039,"size":28,"ttl":62},{"from":"184.105.222.81","rtt":13.747,"size":28,"ttl":62}]},{"hop":4,"result":[{"from":"213.248.67.125","rtt":3.466,"size":28,"ttl":252},{"from":"213.248.67.125","rtt":6.483,"size":28,"ttl":252},{"from":"213.248.67.125","rtt":2.901,"size":28,"ttl":252}]},{"hop":5,"result":[{"from":"213.155.130.32","rtt":2.9,"size":28,"ttl":251},{"from":"213.155.130.32","rtt":2.911,"size":28,"ttl":251},{"from":"213.155.130.32","rtt":2.906,"size":28,"ttl":251}]},{"hop":6,"result":[{"from":"213.248.100.178","rtt":2.888,"size":28,"ttl":250},{"from":"213.248.100.178","rtt":2.905,"size":28,"ttl":250},{"from":"213.248.100.178","rtt":2.907,"size":28,"ttl":250}]},{"hop":7,"result":[{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":539153,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":102.323,"size":140,"ttl":243},{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":539153,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":101.937,"size":140,"ttl":243},{"from":"63.243.128.38","icmpext":{"obj":[{"class":1,"mpls":[{"exp":1,"label":539153,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":101.985,"size":140,"ttl":243}]},{"hop":8,"result":[{"from":"80.231.200.13","rtt":118.695,"size":28,"ttl":245},{"from":"80.231.200.13","rtt":167.614,"size":28,"ttl":245},{"from":"80.231.200.13","rtt":104.848,"size":28,"ttl":245}]},{"hop":9,"result":[{"from":"80.231.200.26","rtt":198.423,"size":28,"ttl":242},{"from":"80.231.200.26","rtt":198.483,"size":28,"ttl":242},{"from":"80.231.200.26","rtt":275.198,"size":28,"ttl":242}]},{"hop":10,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":11,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":12,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"216.66.30.82","timestamp":1392240112,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2014-02-12T21:22:13+00:00")
    assert(result.origin == "216.66.30.82")
    assert(result.firmware == 4570)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 426)
    assert(result.paris_id == 2)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 15)
    assert(result.last_median_rtt == 198.483)
    assert(result.ip_path[3][1] == "213.248.67.125")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "213.248.67.125")
    assert(result.hops[3].packets[1].rtt == 6.483)
    assert(result.hops[3].packets[1].size == 28)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_4600():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1392240144,"from":"192.172.226.243","fw":4600,"msm_id":1000157,"msm_name":"Traceroute","paris_id":1,"prb_id":319,"proto":"UDP","result":[{"hop":1,"result":[{"from":"192.172.226.252","rtt":1.905,"size":28,"ttl":254},{"from":"192.172.226.252","rtt":1.753,"size":28,"ttl":254},{"from":"192.172.226.252","rtt":1.9,"size":28,"ttl":254}]},{"hop":2,"result":[{"from":"192.12.207.61","rtt":1.895,"size":28,"ttl":253},{"from":"192.12.207.61","rtt":1.894,"size":28,"ttl":253},{"from":"192.12.207.61","rtt":1.91,"size":28,"ttl":253}]},{"hop":3,"result":[{"from":"137.164.23.129","rtt":1.902,"size":28,"ttl":253},{"from":"137.164.23.129","rtt":1.903,"size":28,"ttl":253},{"from":"137.164.23.129","rtt":1.892,"size":28,"ttl":253}]},{"hop":4,"result":[{"from":"137.164.47.14","rtt":13.516,"size":68,"ttl":252},{"from":"137.164.47.14","rtt":11.383,"size":68,"ttl":252},{"from":"137.164.47.14","rtt":13.716,"size":68,"ttl":252}]},{"hop":5,"result":[{"from":"137.164.46.57","rtt":14.907,"size":68,"ttl":251},{"from":"137.164.46.57","rtt":12.637,"size":68,"ttl":251},{"from":"137.164.46.57","rtt":14.947,"size":68,"ttl":251}]},{"hop":6,"result":[{"from":"137.164.47.136","rtt":11.321,"size":28,"ttl":250},{"from":"137.164.47.136","rtt":11.148,"size":28,"ttl":250},{"from":"137.164.47.136","rtt":11.209,"size":28,"ttl":250}]},{"hop":7,"result":[{"from":"4.59.48.177","rtt":11.24,"size":28,"ttl":248},{"from":"4.59.48.177","rtt":11.284,"size":28,"ttl":248},{"from":"4.59.48.177","rtt":11.364,"size":28,"ttl":248}]},{"hop":8,"result":[{"from":"4.69.144.208","rtt":48.435,"size":28,"ttl":248},{"from":"4.69.144.208","rtt":11.359,"size":28,"ttl":248},{"from":"4.69.144.208","rtt":11.29,"size":28,"ttl":248}]},{"hop":9,"result":[{"from":"4.68.62.118","rtt":11.387,"size":28,"ttl":247},{"from":"4.68.62.118","rtt":11.322,"size":28,"ttl":247},{"from":"4.68.62.118","rtt":11.568,"size":28,"ttl":247}]},{"hop":10,"result":[{"from":"66.198.144.73","rtt":23.979,"size":28,"ttl":245},{"from":"66.198.144.73","rtt":23.784,"size":28,"ttl":245},{"from":"66.198.144.73","rtt":23.924,"size":28,"ttl":245}]},{"hop":11,"result":[{"from":"66.198.144.2","rtt":278.829,"size":28,"ttl":229},{"from":"66.198.144.2","rtt":272.012,"size":28,"ttl":229},{"from":"66.198.144.2","rtt":271.775,"size":28,"ttl":229}]},{"hop":12,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"192.172.226.243","timestamp":1392240124,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2014-02-12T21:22:24+00:00")
    assert(result.origin == "192.172.226.243")
    assert(result.firmware == 4600)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 319)
    assert(result.paris_id == 1)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 17)
    assert(result.last_median_rtt == 272.012)
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.ip_path[3][1] == "137.164.47.14")
    assert(result.hops[3].packets[0].origin == "137.164.47.14")
    assert(result.hops[3].packets[1].rtt == 11.383)
    assert(result.hops[3].packets[1].size == 68)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_4610():
    result = Result.get('{"af":4,"dst_addr":"121.244.76.25","dst_name":"121.244.76.25","endtime":1395833056,"from":"192.172.226.243","fw":4610,"group_id":1000157,"msm_id":1000157,"msm_name":"Traceroute","paris_id":13,"prb_id":319,"proto":"UDP","result":[{"hop":1,"result":[{"from":"192.172.226.252","rtt":5.6970000000000001,"size":28,"ttl":254},{"from":"192.172.226.252","rtt":2.931,"size":28,"ttl":254},{"from":"192.172.226.252","rtt":2.919,"size":28,"ttl":254}]},{"hop":2,"result":[{"from":"192.12.207.61","rtt":3.052,"size":28,"ttl":253},{"from":"192.12.207.61","rtt":2.923,"size":28,"ttl":253},{"from":"192.12.207.61","rtt":2.919,"size":28,"ttl":253}]},{"hop":3,"result":[{"from":"137.164.23.129","rtt":2.9140000000000001,"size":28,"ttl":253},{"from":"137.164.23.129","rtt":3.0579999999999998,"size":28,"ttl":253},{"from":"137.164.23.129","rtt":3.0630000000000002,"size":28,"ttl":253}]},{"hop":4,"result":[{"from":"137.164.47.14","rtt":14.433999999999999,"size":68,"ttl":252},{"from":"137.164.47.14","rtt":17.170999999999999,"size":68,"ttl":252},{"from":"137.164.47.14","rtt":14.332000000000001,"size":68,"ttl":252}]},{"hop":5,"result":[{"from":"137.164.46.57","rtt":14.737,"size":68,"ttl":251},{"from":"137.164.46.57","rtt":16.905000000000001,"size":68,"ttl":251},{"from":"137.164.46.57","rtt":14.532,"size":68,"ttl":251}]},{"hop":6,"result":[{"from":"137.164.47.136","rtt":12.420999999999999,"size":28,"ttl":250},{"from":"137.164.47.136","rtt":12.192,"size":28,"ttl":250},{"from":"137.164.47.136","rtt":12.204000000000001,"size":28,"ttl":250}]},{"hop":7,"result":[{"from":"4.59.48.177","rtt":12.343999999999999,"size":28,"ttl":248},{"from":"4.59.48.177","rtt":12.404,"size":28,"ttl":248},{"from":"4.59.48.177","rtt":12.257999999999999,"size":28,"ttl":248}]},{"hop":8,"result":[{"from":"4.69.144.80","rtt":12.476000000000001,"size":28,"ttl":248},{"from":"4.69.144.80","rtt":12.329000000000001,"size":28,"ttl":248},{"from":"4.69.144.80","rtt":12.473000000000001,"size":28,"ttl":248}]},{"hop":9,"result":[{"from":"4.68.62.118","rtt":12.506,"size":28,"ttl":247},{"from":"4.68.62.118","rtt":12.324,"size":28,"ttl":247},{"from":"4.68.62.118","rtt":12.56,"size":28,"ttl":247}]},{"hop":10,"result":[{"from":"64.86.252.38","rtt":24.934000000000001,"size":28,"ttl":245},{"from":"64.86.252.38","rtt":24.690000000000001,"size":28,"ttl":245},{"from":"64.86.252.38","rtt":24.913,"size":28,"ttl":245}]},{"hop":11,"result":[{"from":"66.198.144.2","rtt":297.88499999999999,"size":28,"ttl":232},{"from":"66.198.144.2","rtt":273.28500000000003,"size":28,"ttl":232},{"from":"66.198.144.2","rtt":273.49400000000003,"size":28,"ttl":232}]},{"hop":12,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":14,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":15,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":16,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"192.172.226.243","timestamp":1395833036,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(isinstance(result.hops[0], Hop))
    assert(isinstance(result.hops[0].packets[0], Packet))
    assert(result.af == 4)
    assert(result.destination_address == "121.244.76.25")
    assert(result.destination_name == "121.244.76.25")
    assert(result.end_time.isoformat() == "2014-03-26T11:24:16+00:00")
    assert(result.origin == "192.172.226.243")
    assert(result.firmware == 4610)
    assert(result.measurement_id == 1000157)
    assert(result.probe_id == 319)
    assert(result.paris_id == 13)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 17)
    assert(result.last_median_rtt == 273.494)
    assert(result.destination_ip_responded is False)
    assert(result.last_hop_responded is False)
    assert(result.is_success is False)
    assert(result.ip_path[3][1] == "137.164.47.14")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[3].index == 4)
    assert(result.hops[3].packets[0].origin == "137.164.47.14")
    assert(result.hops[3].packets[1].rtt == 17.171)
    assert(result.hops[3].packets[1].size == 68)
    assert(result.hops[3].packets[2].ttl == 252)
    assert(result.hops[-1].index == 255)


def test_traceroute_responding_target():
    result = Result.get('{"af":4,"dst_addr":"220.226.205.30","dst_name":"220.226.205.30","endtime":1398334554,"from":"75.75.127.227","fw":4610,"msm_id":1000158,"msm_name":"Traceroute","paris_id":15,"prb_id":394,"proto":"UDP","result":[{"hop":1,"result":[{"from":"10.0.0.1","rtt":3.0310000000000001,"size":68,"ttl":64},{"from":"10.0.0.1","rtt":3.1930000000000001,"size":68,"ttl":64},{"from":"10.0.0.1","rtt":3.1869999999999998,"size":68,"ttl":64}]},{"hop":2,"result":[{"from":"96.120.80.5","rtt":10.606999999999999,"size":28,"ttl":254},{"from":"96.120.80.5","rtt":10.815,"size":28,"ttl":254},{"from":"96.120.80.5","rtt":10.208,"size":28,"ttl":254}]},{"hop":3,"result":[{"from":"68.86.175.213","rtt":9.7599999999999998,"size":28,"ttl":252},{"from":"68.86.175.213","rtt":15.592000000000001,"size":28,"ttl":252},{"from":"68.86.175.213","rtt":17.454000000000001,"size":28,"ttl":252}]},{"hop":4,"result":[{"from":"68.85.214.113","rtt":11.877000000000001,"size":28,"ttl":251},{"from":"68.85.214.113","rtt":11.071,"size":28,"ttl":251},{"from":"68.85.214.113","rtt":11.417999999999999,"size":28,"ttl":251}]},{"hop":5,"result":[{"from":"68.86.95.21","rtt":14.359,"size":68,"ttl":251},{"from":"68.86.95.21","rtt":24.558,"size":68,"ttl":251},{"from":"68.86.95.21","rtt":16.370000000000001,"size":68,"ttl":251}]},{"hop":6,"result":[{"from":"23.30.207.94","rtt":14.358000000000001,"size":28,"ttl":249},{"from":"23.30.207.94","rtt":14.403,"size":28,"ttl":249},{"from":"23.30.207.94","rtt":14.685,"size":28,"ttl":249}]},{"hop":7,"result":[{"from":"4.69.146.222","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1394,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"rtt":19.100000000000001,"size":140,"ttl":52},{"from":"4.69.146.222","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1394,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"rtt":19.216000000000001,"size":140,"ttl":52},{"from":"4.69.146.222","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1394,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"rtt":20.004999999999999,"size":140,"ttl":52}]},{"hop":8,"result":[{"from":"4.69.201.69","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1692,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"ittl":2,"rtt":20.114999999999998,"size":140,"ttl":52},{"from":"4.69.201.69","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1692,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"ittl":2,"rtt":20.407,"size":140,"ttl":52},{"from":"4.69.201.69","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1692,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"ittl":2,"rtt":19.105,"size":140,"ttl":52}]},{"hop":9,"result":[{"from":"4.69.134.78","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1512,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"ittl":3,"rtt":27.760000000000002,"size":140,"ttl":53},{"from":"4.69.134.78","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1512,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"ittl":3,"rtt":20.033999999999999,"size":140,"ttl":53},{"from":"4.69.134.78","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":1512,"s":1,"ttl":1}],"type":1}],"rfc4884":1,"version":2},"ittl":3,"rtt":20.065999999999999,"size":140,"ttl":53}]},{"hop":10,"result":[{"from":"4.69.155.206","rtt":18.975999999999999,"size":28,"ttl":244},{"from":"4.69.155.206","rtt":74.272999999999996,"size":28,"ttl":244},{"from":"4.69.155.206","rtt":20.582000000000001,"size":28,"ttl":244}]},{"hop":11,"result":[{"from":"4.78.132.122","rtt":22.222000000000001,"size":28,"ttl":243},{"from":"4.78.132.122","rtt":23.568000000000001,"size":28,"ttl":243},{"from":"4.78.132.122","rtt":20.062000000000001,"size":28,"ttl":243}]},{"hop":12,"result":[{"from":"85.95.25.110","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":310352,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":215.90000000000001,"size":140,"ttl":239},{"from":"85.95.25.110","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":310352,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":217.31399999999999,"size":140,"ttl":239},{"from":"85.95.25.110","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":310352,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":235.255,"size":140,"ttl":239}]},{"hop":13,"result":[{"from":"85.95.25.158","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":301856,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":93.918000000000006,"size":140,"ttl":246},{"from":"85.95.25.158","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":301856,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":93.653000000000006,"size":140,"ttl":246},{"from":"85.95.25.158","icmpext":{"obj":[{"class":1,"mpls":[{"exp":0,"label":301856,"s":1,"ttl":1}],"type":1}],"rfc4884":0,"version":2},"rtt":94.137,"size":140,"ttl":246}]},{"hop":14,"result":[{"from":"85.95.26.153","rtt":221.02600000000001,"size":28,"ttl":242},{"from":"85.95.26.153","rtt":220.42500000000001,"size":28,"ttl":242},{"from":"85.95.26.153","rtt":220.12799999999999,"size":28,"ttl":242}]},{"hop":15,"result":[{"from":"62.216.147.98","rtt":217.67699999999999,"size":68,"ttl":50},{"from":"62.216.147.98","rtt":221.37200000000001,"size":68,"ttl":50},{"from":"62.216.147.98","rtt":220.02199999999999,"size":68,"ttl":50}]},{"hop":16,"result":[{"from":"202.138.117.210","rtt":215.69499999999999,"size":28,"ttl":240},{"from":"202.138.117.210","rtt":215.68700000000001,"size":28,"ttl":240},{"from":"202.138.117.210","rtt":219.387,"size":28,"ttl":240}]},{"hop":17,"result":[{"from":"202.138.113.1","rtt":225.48099999999999,"size":28,"ttl":239},{"from":"202.138.113.1","rtt":221.18299999999999,"size":28,"ttl":239},{"from":"202.138.113.1","rtt":227.797,"size":28,"ttl":239}]},{"hop":18,"result":[{"from":"202.138.113.37","rtt":229.71799999999999,"size":28,"ttl":47},{"from":"202.138.113.37","rtt":216.155,"size":28,"ttl":47},{"from":"202.138.113.37","rtt":216.096,"size":28,"ttl":47}]},{"hop":19,"result":[{"from":"202.138.113.150","rtt":224.357,"size":28,"ttl":237},{"from":"202.138.113.150","rtt":223.726,"size":28,"ttl":237},{"from":"202.138.113.150","rtt":221.374,"size":28,"ttl":237}]},{"hop":20,"result":[{"from":"220.226.205.30","rtt":221.541,"size":68,"ttl":45},{"from":"220.226.205.30","rtt":217.10300000000001,"size":68,"ttl":45},{"from":"220.226.205.30","rtt":216.44300000000001,"size":68,"ttl":45}]}],"size":40,"src_addr":"10.0.0.7","timestamp":1398334547,"type":"traceroute"}')
    assert(isinstance(result, TracerouteResult))
    assert(isinstance(result.hops[0], Hop))
    assert(isinstance(result.hops[0].packets[0], Packet))
    assert(result.af == 4)
    assert(result.destination_address == "220.226.205.30")
    assert(result.destination_name == "220.226.205.30")
    assert(result.end_time.isoformat() == "2014-04-24T10:15:54+00:00")
    print(result.end_time_timestamp, 1398334554)
    assert(result.end_time_timestamp == 1398334554)
    assert(result.origin == "75.75.127.227")
    assert(result.firmware == 4610)
    assert(result.measurement_id == 1000158)
    assert(result.probe_id == 394)
    assert(result.paris_id == 15)
    assert(result.protocol == TracerouteResult.PROTOCOL_UDP)
    assert(result.total_hops == 20)
    assert(result.last_median_rtt == 217.103)
    assert(result.destination_ip_responded is True)
    assert(result.last_hop_responded is True)
    assert(result.is_success is True)
    assert(result.ip_path[3][1] == "68.85.214.113")
    assert(result.hops[0].packets[0].destination_option_size is None)
    assert(result.hops[0].packets[0].hop_by_hop_option_size is None)
    assert(result.hops[0].packets[0].mtu is None)
    assert(result.hops[19].index == 20)
    assert(result.hops[19].packets[0].origin == "220.226.205.30")
    assert(result.hops[19].packets[1].rtt == 217.103)
    assert(result.hops[19].packets[1].size == 68)
    assert(result.hops[19].packets[2].ttl == 45)
    assert(result.hops[7].packets[0].internal_ttl == 2)
    assert(result.hops[7].packets[0].icmp_header.rfc4884 == 1)
    assert(result.hops[7].packets[0].icmp_header.version == 2)
    assert(result.hops[7].packets[0].icmp_header.objects == [{u"class": 1, u"mpls": [{u"exp": 0, u"label": 1692, u"s": 1, u"ttl": 1}], u"type": 1}])
    assert(result.hops[1].packets[0].icmp_header is None)
    assert(result.hops[-1].index == 20)


def test_traceroute_error():
    result = Result.get('{"af":6,"dst_addr":"2001:6b0:e:3::1","dst_name":"2001:6b0:e:3:0:0:0:1","endtime":1399388948,"from":"","fw":4610,"group_id":1018508,"lts":107,"msm_id":1019825,"msm_name":"Traceroute","paris_id":5,"prb_id":82,"proto":"ICMP","result":[{"hop":1,"result":[{"err":"H","from":"2001:67c:2e8:13:fad1:11ff:fea9:dd68","rtt":2014.845,"size":88,"ttl":64},{"err":"H","from":"2001:67c:2e8:13:fad1:11ff:fea9:dd68","rtt":2995.839,"size":88,"ttl":64},{"err":"H","from":"2001:67c:2e8:13:fad1:11ff:fea9:dd68","rtt":2998.491,"size":88,"ttl":64}]}],"size":40,"src_addr":"2001:67c:2e8:13:fad1:11ff:fea9:dd68","timestamp":1399388940,"type":"traceroute"}')
    assert(result.total_hops == 1)
    assert(result.hops[0].index == 1)
    assert(result.hops[0].packets[0].is_error is True)
    assert(result.hops[0].packets[0].error_message == Packet.ERROR_CONDITIONS["H"])
    assert(result.hops[0].packets[1].is_error is True)
    assert(result.hops[0].packets[1].error_message == Packet.ERROR_CONDITIONS["H"])
    assert(result.hops[0].packets[2].is_error is True)
    assert(result.hops[0].packets[2].error_message == Packet.ERROR_CONDITIONS["H"])


def test_traceroute_error_unreachable():
    result = Result.get('{"af":6,"dst_addr":"2001:6b0:e:3::1","dst_name":"2001:6b0:e:3:0:0:0:1","endtime":1398180530,"from":"","fw":4610,"group_id":1018508,"lts":10065,"msm_id":1019825,"msm_name":"Traceroute","paris_id":14,"prb_id":82,"proto":"ICMP","result":[{"error":"connect failed: Network is unreachable","hop":1}],"size":40,"src_addr":"2001:67c:2e8:13:fad1:11ff:fea9:dd68","timestamp":1398180530,"type":"traceroute"}')
    assert(result.total_hops == 1)
    assert(result.hops[0].index == 1)
    assert(result.hops[0].is_error is True)
    assert(result.hops[0].error_message == "connect failed: Network is unreachable")
    assert(len(result.hops[0].packets) == 0)


def test_traceroute_v6_mtu():
    result = Result.get('{"af":6,"dst_addr":"2a03:8180:1001:b2:45::3","dst_name":"2a03:8180:1001:b2:45:0:0:3","endtime":1400582566,"from":"","fw":4610,"group_id":1666033,"msm_id":1666033,"msm_name":"Traceroute","paris_id":1,"prb_id":2463,"proto":"ICMP","result":[{"hop":1,"result":[{"from":"2001:470:d04f:12::18","mtu":1500,"rtt":5.1260000000000003,"size":1232,"ttl":64},{"x":"*"},{"err":"H","from":"2001:470:d04f:12::18","rtt":3011.8739999999998,"size":1232,"ttl":64},{"err":"H","from":"2001:470:d04f:12::18","rtt":3011.8110000000001,"size":1232,"ttl":64},{"err":"H","from":"2001:470:d04f:12::18","rtt":3011.8690000000001,"size":1232,"ttl":64}]},{"hop":2,"result":[{"err":"H","from":"2001:470:d04f:12::18","ittl":2,"rtt":3011.6619999999998,"size":1232,"ttl":64},{"err":"H","from":"2001:470:d04f:12::18","ittl":2,"rtt":3011.877,"size":1232,"ttl":64},{"err":"H","from":"2001:470:d04f:12::18","ittl":2,"rtt":3011.866,"size":1232,"ttl":64},{"err":"H","from":"2001:470:d04f:12::18","ittl":2,"rtt":3012.1300000000001,"size":1232,"ttl":64},{"err":"H","from":"2001:470:d04f:12::18","ittl":2,"rtt":3012.1700000000001,"size":1232,"ttl":64}]}],"size":2000,"src_addr":"2001:470:d04f:12::18","timestamp":1400582538,"type":"traceroute"}')
    assert(result.hops[0].packets[0].mtu == 1500)


def test_traceroute_v6_options():
    result = Result.get('{"af":6,"dst_addr":"2a00:1450:4013:c01::5e","dst_name":"2a00:1450:4013:c01:0:0:0:5e","endtime":1400087957,"from":"2601:6:7980:584:6666:b3ff:feb0:f3b8","fw":4610,"group_id":1665356,"msm_id":1665357,"msm_name":"Traceroute","paris_id":1,"prb_id":14748,"proto":"ICMP","result":[{"hop":1,"result":[{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":5.0170000000000003,"size":608,"ttl":64},{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":4.4960000000000004,"size":608,"ttl":64},{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":4.9770000000000003,"size":608,"ttl":64},{"x":"*"},{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":4.8120000000000003,"size":608,"ttl":64},{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":4.556,"size":608,"ttl":64},{"x":"*"},{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":4.9500000000000002,"size":608,"ttl":64},{"x":"*"},{"dstoptsize":512,"from":"2601:6:7980:584::1","rtt":4.5,"size":608,"ttl":64}]},{"hop":2,"result":[{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":17.681999999999999,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":13.93,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":12.875,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":11.496,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":11.692,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":13.476000000000001,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":11.685,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":15.076000000000001,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":14.548999999999999,"size":608,"ttl":63},{"dstoptsize":512,"from":"2001:558:4023:f6::1","rtt":11.723000000000001,"size":608,"ttl":63}]},{"hop":3,"result":[{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":13.426,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":13.311999999999999,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":14.772,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":12.185,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":13.241,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":15.148999999999999,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":12.010999999999999,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":11.635,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":13.837999999999999,"size":608,"ttl":62},{"dstoptsize":512,"from":"2001:558:202:82::1","rtt":13.212,"size":608,"ttl":62}]},{"hop":4,"result":[{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.193,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.891,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.178000000000001,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.457000000000001,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.097,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":12.823,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.66,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.865,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":13.714,"size":608,"ttl":61},{"dstoptsize":512,"from":"2001:558:200:8f::1","rtt":15.621,"size":608,"ttl":61}]},{"hop":5,"result":[{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":19.004000000000001,"size":608,"ttl":60},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":21.626000000000001,"size":608,"ttl":60},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":21.167999999999999,"size":608,"ttl":60},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":17.995999999999999,"size":608,"ttl":60},{"x":"*"},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":19.061,"size":608,"ttl":60},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":17.544,"size":608,"ttl":60},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":18.108000000000001,"size":608,"ttl":60},{"dstoptsize":512,"from":"2001:558:200:175::1","rtt":17.172000000000001,"size":608,"ttl":60},{"x":"*"}]},{"hop":6,"result":[{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":23.879999999999999,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":25.186,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":21.422999999999998,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":25.553000000000001,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":25.783000000000001,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":26.172999999999998,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":25.032,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":26.071999999999999,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":25.173999999999999,"size":608,"ttl":59},{"dstoptsize":512,"from":"2001:558:200:11d::1","rtt":25.318999999999999,"size":608,"ttl":59}]},{"hop":7,"result":[{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":31.378,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":29.427,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":29.52,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":30.445,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":28.565000000000001,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":29.602,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":30.321999999999999,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":28.719999999999999,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":29.369,"size":608,"ttl":58},{"dstoptsize":512,"from":"2001:558:0:f76e::1","rtt":29.747,"size":608,"ttl":58}]},{"hop":8,"result":[{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":30.334,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":27.571999999999999,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":31.545999999999999,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":27.419,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":29.584,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":27.41,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":31.577999999999999,"size":608,"ttl":57},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":28.866,"size":608,"ttl":57},{"x":"*"},{"dstoptsize":512,"from":"2001:558:0:f8d7::2","rtt":30.077999999999999,"size":608,"ttl":57}]},{"hop":9,"result":[{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":10,"result":[{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":11,"result":[{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":12,"result":[{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":13,"result":[{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"}]},{"hop":255,"result":[{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"},{"x":"*"}]}],"size":40,"src_addr":"2601:6:7980:584:6666:b3ff:feb0:f3b8","timestamp":1400087690,"type":"traceroute"}')
    assert(result.hops[0].packets[0].destination_option_size == 512)
    assert(result.hops[0].packets[1].destination_option_size == 512)
    assert(result.hops[0].packets[2].destination_option_size == 512)
    assert(result.hops[0].packets[3].destination_option_size is None)
    result = Result.get('{"af":6,"dst_addr":"2a02:d28:667::2","dst_name":"2a02:d28:667:0:0:0:0:2","endtime":1400589952,"from":"2a02:d28:667:1::2","fw":4620,"group_id":1666051,"msm_id":1666051,"msm_name":"Traceroute","paris_id":1,"prb_id":6021,"proto":"UDP","result":[{"hop":1,"result":[{"from":"2a02:d28:667:1::1","hbhoptsize":256,"rtt":2.669,"size":352,"ttl":64},{"from":"2a02:d28:667:1::1","hbhoptsize":256,"rtt":0.27200000000000002,"size":352,"ttl":64},{"from":"2a02:d28:667:1::1","hbhoptsize":256,"rtt":2.2309999999999999,"size":352,"ttl":64}]},{"hop":2,"result":[{"from":"2a02:d28:5580:1::d1","hbhoptsize":256,"rtt":64.810000000000002,"size":352,"ttl":61},{"from":"2a02:d28:5580:1::d1","hbhoptsize":256,"rtt":76.120000000000005,"size":352,"ttl":63},{"from":"2a02:d28:5580:1::d1","hbhoptsize":256,"rtt":83.963999999999999,"size":352,"ttl":61}]},{"hop":3,"result":[{"from":"2a02:d28:5580::1:b9","hbhoptsize":256,"rtt":100.01000000000001,"size":352,"ttl":62},{"from":"2a02:d28:5580::1:b9","hbhoptsize":256,"rtt":88.451999999999998,"size":352,"ttl":62},{"from":"2a02:d28:5580::1:b9","hbhoptsize":256,"rtt":88.390000000000001,"size":352,"ttl":62}]},{"hop":4,"result":[{"from":"2a02:d28:5580:1::c1","hbhoptsize":256,"rtt":88.792000000000002,"size":352,"ttl":61},{"from":"2a02:d28:5580:1::c1","hbhoptsize":256,"rtt":88.882000000000005,"size":352,"ttl":61},{"from":"2a02:d28:5580:1::c1","hbhoptsize":256,"rtt":87.719999999999999,"size":352,"ttl":61}]},{"hop":5,"result":[{"from":"2a02:d28:667::2","hbhoptsize":256,"rtt":90.457999999999998,"size":352,"ttl":60},{"from":"2a02:d28:667::2","hbhoptsize":256,"rtt":91.408000000000001,"size":352,"ttl":60},{"from":"2a02:d28:667::2","hbhoptsize":256,"rtt":85.784999999999997,"size":352,"ttl":60}]}],"size":40,"src_addr":"2a02:d28:667:1::2","timestamp":1400589951,"type":"traceroute"}')
    assert(result.hops[0].packets[0].hop_by_hop_option_size is 256)
    assert(result.hops[0].packets[1].hop_by_hop_option_size is 256)
    assert(result.hops[0].packets[2].hop_by_hop_option_size is 256)


def test_traceroute_lts():
    result = Result.get('{"lts":2029,"size":40,"group_id":1000157,"from":"192.172.226.243","dst_name":"121.244.76.25","fw":4650,"proto":"UDP","af":4,"msm_name":"Traceroute","prb_id":319,"result":[{"result":[{"rtt":1.891,"ttl":254,"from":"192.172.226.252","size":28},{"rtt":34.727,"ttl":254,"from":"192.172.226.252","size":28},{"rtt":1.731,"ttl":254,"from":"192.172.226.252","size":28}],"hop":1},{"result":[{"rtt":1.726,"ttl":253,"from":"192.12.207.61","size":28},{"rtt":1.724,"ttl":253,"from":"192.12.207.61","size":28},{"rtt":1.72,"ttl":253,"from":"192.12.207.61","size":28}],"hop":2},{"result":[{"rtt":1.72,"ttl":253,"from":"137.164.23.129","size":28},{"rtt":1.735,"ttl":253,"from":"137.164.23.129","size":28},{"rtt":1.724,"ttl":253,"from":"137.164.23.129","size":28}],"hop":3},{"result":[{"rtt":13.136,"ttl":252,"from":"137.164.47.110","size":68},{"rtt":10.883,"ttl":252,"from":"137.164.47.110","size":68},{"rtt":13.087,"ttl":252,"from":"137.164.47.110","size":68}],"hop":4},{"result":[{"rtt":15.208,"ttl":251,"from":"137.164.46.57","size":68},{"rtt":12.571,"ttl":251,"from":"137.164.46.57","size":68},{"rtt":14.545,"ttl":251,"from":"137.164.46.57","size":68}],"hop":5},{"result":[{"rtt":11.037,"ttl":250,"from":"137.164.47.136","size":28},{"rtt":10.957,"ttl":250,"from":"137.164.47.136","size":28},{"rtt":11.011,"ttl":250,"from":"137.164.47.136","size":28}],"hop":6},{"result":[{"rtt":11.075,"ttl":249,"from":"4.59.48.177","size":28},{"rtt":11.032,"ttl":249,"from":"4.59.48.177","size":28},{"rtt":69.194,"ttl":249,"from":"4.59.48.177","size":28}],"hop":7},{"result":[{"rtt":11.25,"ttl":248,"from":"4.69.144.80","size":28},{"rtt":11.141,"ttl":248,"from":"4.69.144.80","size":28},{"rtt":11.177,"ttl":248,"from":"4.69.144.80","size":28}],"hop":8},{"result":[{"rtt":11.316,"ttl":247,"from":"4.68.62.118","size":28},{"rtt":11.243,"ttl":247,"from":"4.68.62.118","size":28},{"rtt":11.238,"ttl":247,"from":"4.68.62.118","size":28}],"hop":9},{"result":[{"rtt":37.808,"ttl":245,"from":"64.86.252.38","size":28},{"rtt":37.811,"ttl":245,"from":"64.86.252.38","size":28},{"rtt":37.768,"ttl":245,"from":"64.86.252.38","size":28}],"hop":10},{"result":[{"rtt":277.064,"ttl":232,"from":"66.198.144.2","size":28},{"rtt":276.963,"ttl":232,"from":"66.198.144.2","size":28},{"rtt":276.92,"ttl":232,"from":"66.198.144.2","size":28}],"hop":11},{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":12},{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":13},{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":14},{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":15},{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":16},{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":255}],"timestamp":1406561027,"src_addr":"192.172.226.243","paris_id":5,"endtime":1406561047,"type":"traceroute","dst_addr":"121.244.76.25","msm_id":1000157}')
    assert(result.seconds_since_sync == 2029)


def test_traceroute_last_hop_responded_vs_destination_ip_responded():
    result = Result.get('{"af":6,"dst_addr":"2a00:1450:4001:808::1010","dst_name":"2a00:1450:4001:808::1010","endtime":1414685936,"from":"2001:6c8:3f00:abe:280:a3ff:fe91:4252","fw":4660,"group_id":1772418,"lts":110,"msm_id":1772418,"msm_name":"Traceroute","paris_id":1,"prb_id":4978,"proto":"UDP","result":[{"hop":1,"result":[{"from":"2001:6c8:3f00:abe::1","rtt":2.399,"size":96,"ttl":63},{"from":"2001:6c8:3f00:abe::1","rtt":2.199,"size":96,"ttl":63},{"from":"2001:6c8:3f00:abe::1","rtt":2.136,"size":96,"ttl":63}]},{"hop":2,"result":[{"from":"2001:6c8:41:100:0:10:3:1","rtt":22.533,"size":96,"ttl":62},{"from":"2001:6c8:41:100:0:10:3:1","rtt":22.131,"size":96,"ttl":62},{"from":"2001:6c8:41:100:0:10:3:1","rtt":22.54,"size":96,"ttl":62}]},{"hop":3,"result":[{"from":"2001:6f0:40::3a","rtt":33.808,"size":96,"ttl":61},{"from":"2001:6f0:40::3a","rtt":33.815,"size":96,"ttl":61},{"from":"2001:6f0:40::3a","rtt":34.074,"size":96,"ttl":61}]},{"hop":4,"result":[{"from":"2001:6f0:81:100::6:2","rtt":34.335,"size":96,"ttl":60},{"from":"2001:6f0:81:100::6:2","rtt":34.33,"size":96,"ttl":60},{"from":"2001:6f0:81:100::6:2","rtt":34.135,"size":96,"ttl":60}]},{"hop":5,"result":[{"from":"2001:4860::1:0:26eb","rtt":34.559,"size":96,"ttl":59},{"from":"2001:4860::1:0:26eb","rtt":34.638,"size":96,"ttl":59},{"from":"2001:4860::1:0:26eb","rtt":49.453,"size":96,"ttl":59}]},{"hop":6,"result":[{"from":"2001:4860::8:0:4fc8","rtt":35.123,"size":96,"ttl":57},{"from":"2001:4860::8:0:4fc8","rtt":34.621,"size":96,"ttl":57},{"from":"2001:4860::8:0:4fc8","rtt":34.896,"size":96,"ttl":57}]},{"hop":7,"result":[{"from":"2001:4860::8:0:672e","rtt":49.557,"size":96,"ttl":56},{"from":"2001:4860::8:0:672e","rtt":50.057,"size":96,"ttl":56},{"from":"2001:4860::8:0:672e","rtt":50.39,"size":96,"ttl":56}]},{"hop":8,"result":[{"from":"2001:4860::8:0:5039","rtt":50.039,"size":96,"ttl":57},{"from":"2001:4860::8:0:5039","rtt":50.078,"size":96,"ttl":57},{"from":"2001:4860::8:0:5039","rtt":50.061,"size":96,"ttl":57}]},{"hop":9,"result":[{"from":"2001:4860::1:0:4ca2","rtt":52.175,"size":96,"ttl":59},{"from":"2001:4860::1:0:4ca2","rtt":58.49,"size":96,"ttl":59},{"from":"2001:4860::1:0:4ca2","rtt":55.845,"size":96,"ttl":59}]},{"hop":10,"result":[{"from":"2001:4860:0:1::6ef","rtt":50.311,"size":96,"ttl":58},{"x":"*"},{"x":"*"}]},{"hop":11,"result":[{"from":"2a00:1450:8000:3d::3","rtt":52.233,"size":96,"ttl":57},{"from":"2a00:1450:8000:3d::3","rtt":50.576,"size":96,"ttl":57},{"from":"2a00:1450:8000:3d::3","rtt":50.277,"size":96,"ttl":57}]}],"size":48,"src_addr":"2001:6c8:3f00:abe:280:a3ff:fe91:4252","timestamp":1414685926,"type":"traceroute"}')
    assert(result.destination_ip_responded is False)
    assert(result.last_hop_responded is True)


def test_traceroute_with_late_packets():

    # Older firmwares
    result = Result.get('{"lts":-1,"size":40,"from":"185.60.176.3","dst_name":"78.46.48.134","fw":4720,"proto":"UDP","af":4,"msm_name":"Traceroute","prb_id":10834,"result":[{"result":[{"x":"*"},{"x":"*"},{"x":"*"}],"hop":1},{"result":[{"late":4,"ttl":63,"from":"192.168.14.253","size":68},{"x":"*"},{"late":5,"ttl":63,"from":"192.168.14.253","size":68},{"x":"*"},{"late":6,"ttl":63,"from":"192.168.14.253","size":68},{"x":"*"}],"hop":2},{"result":[{"late":7,"ttl":253,"from":"141.105.161.184","size":28},{"x":"*"},{"late":8,"ttl":253,"from":"141.105.161.184","size":28},{"x":"*"},{"late":9,"ttl":253,"from":"141.105.161.184","size":28},{"x":"*"}],"hop":3},{"result":[{"late":10,"ttl":252,"from":"141.105.161.176","size":28},{"x":"*"},{"late":11,"ttl":252,"from":"141.105.161.176","size":28},{"x":"*"},{"late":12,"ttl":252,"from":"141.105.161.176","size":28},{"x":"*"}],"hop":4},{"result":[{"late":13,"ttl":251,"from":"94.201.50.45","size":68},{"x":"*"},{"late":14,"ttl":251,"from":"94.201.50.45","size":68},{"x":"*"},{"late":15,"ttl":251,"from":"94.201.50.45","size":68},{"x":"*"}],"hop":5},{"result":[{"late":16,"ittl":244,"from":"78.46.48.134","ttl":53,"size":68},{"x":"*"},{"late":17,"ittl":244,"from":"78.46.48.134","ttl":53,"size":68},{"x":"*"},{"late":18,"ittl":244,"from":"78.46.48.134","ttl":53,"size":68},{"x":"*"}],"hop":255}],"timestamp":1447330668,"src_addr":"185.60.176.3","paris_id":10,"endtime":1447330686,"type":"traceroute","dst_addr":"78.46.48.134","msm_id":5017}')

    assert(len(result.hops[0].packets) == 3)
    assert(result.hops[0].packets[0].origin is None)
    assert(result.hops[0].packets[0].rtt is None)
    for packet in result.hops[1].packets:
        print(packet.raw_data)
    assert(len(result.hops[1].packets) == 3)
    assert(result.hops[1].packets[0].origin is None)
    assert(result.hops[1].packets[0].rtt is None)
    assert(result.is_success is False)

    # Newer firmwares
    # No sample available yet


def test_last_responded_hop_with_error_packets():
    """"
    Case where traceroute has a single hop and all of its packets have error
    in them.
    """

    result = Result.get({'lts': 117, 'msm_id': 3059023, 'endtime': 1449152831, 'from': '2001:470:1883:1:6666:b3ff:feb0:dcda', 'dst_name': '2001:980:1284:10:beee:7bff:fe87:9eda', 'fw': 4720, 'timestamp': 1449152831, 'proto': 'ICMP', 'paris_id': 1, 'prb_id': 14468, 'af': 6, 'result': [{'result': [{'rtt': 0.714, 'size': 96, 'from': '2001:470:1883:1::1', 'err': 'N', 'ttl': 64}, {'rtt': 0.495, 'size': 96, 'from': '2001:470:1883:1::1', 'err': 'N', 'ttl': 64}, {'rtt': 0.48, 'size': 96, 'from': '2001:470:1883:1::1', 'err': 'N', 'ttl': 64}], 'hop': 1}], 'dst_addr': '2001:980:1284:10:beee:7bff:fe87:9eda', 'src_addr': '2001:470:1883:1:6666:b3ff:feb0:dcda', 'group_id': 3059023, 'type': 'traceroute', 'msm_name': 'Traceroute', 'size': 48})

    assert(len(result.hops[0].packets) == 3)
    assert(result.last_hop_responded is True)
    assert(result.is_success is False)


def test_is_success_with_error_packets():
    """"
    Case where traceroute has a single hop and all of its packets have error
    in them.
    """

    result = Result.get({'lts': 117, 'msm_id': 3059023, 'endtime': 1449152831, 'from': '2001:470:1883:1:6666:b3ff:feb0:dcda', 'dst_name': '2001:980:1284:10:beee:7bff:fe87:9eda', 'fw': 4720, 'timestamp': 1449152831, 'proto': 'ICMP', 'paris_id': 1, 'prb_id': 14468, 'af': 6, 'result': [{'result': [{'rtt': 0.714, 'size': 96, 'from': '2001:470:1883:1::1', 'err': 'N', 'ttl': 64}, {'rtt': 0.495, 'size': 96, 'from': '2001:470:1883:1::1', 'err': 'N', 'ttl': 64}, {'rtt': 0.48, 'size': 96, 'from': '2001:470:1883:1::1', 'err': 'N', 'ttl': 64}], 'hop': 1}], 'dst_addr': '2001:980:1284:10:beee:7bff:fe87:9eda', 'src_addr': '2001:470:1883:1:6666:b3ff:feb0:dcda', 'group_id': 3059023, 'type': 'traceroute', 'msm_name': 'Traceroute', 'size': 48})

    assert(len(result.hops[0].packets) == 3)
    assert(result.is_success is False)
    assert(result.last_hop_errors == ['Network unreachable', 'Network unreachable', 'Network unreachable'])


def test_missing_dst_addr():
    """"Case where traceroute misses dst_addr key."""

    result = Result.get({"af": 4, "dst_name": "syndication.exoclick.com", "endtime": 1446563590, "from": "89.216.30.6", "fw": 4720, "group_id": 2906346, "lts": 80, "msm_id": 2906346, "msm_name": "Traceroute", "paris_id": 0, "prb_id": 22586, "proto": "ICMP", "result": [{"error": "name resolution failed: non-recoverable failure in name resolution (1)"}], "size": 48, "timestamp": 1446563590, "type": "traceroute"})
    assert(result.destination_address is None)
    assert(result.is_success is False)

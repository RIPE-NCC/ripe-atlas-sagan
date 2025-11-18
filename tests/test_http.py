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

from ripe.atlas.sagan import Result, ResultError, ResultParseError
from ripe.atlas.sagan.http import HttpResult

def test_http_0():
    data = '{"fw":0,"msm_id":12023,"prb_id":1,"src_addr":"GET4 193.0.6.139 0.042268 200 263 1406","timestamp":1319704299,"type":"http"}'
    result = Result.get(data)
    assert(result.is_malformed is True)
    try:
        Result.get(data, on_malformation=Result.ACTION_FAIL)
        assert False
    except ResultParseError:
        pass

def test_http_1_error():
    data = '{"fw":1,"msm_id":12023,"prb_id":1,"src_addr":"connect error 4","timestamp":1323118908,"type":"http"}'
    result = Result.get(data)
    assert(result.is_malformed is True)
    try:
        Result.get(data, on_malformation=Result.ACTION_FAIL)
        assert False
    except ResultParseError:
        pass

def test_http_1():
    result = Result.get('{"from":"62.194.83.50","fw":1,"msm_id":12023,"prb_id":1,"result":"GET4 193.0.6.139 0.030229 200 263 1406","timestamp":1333387900,"type":"http"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "62.194.83.50")
    assert(result.firmware == 1)
    assert(result.measurement_id == 12023)
    assert(result.probe_id == 1)
    assert(result.created.isoformat() == "2012-04-02T17:31:40+00:00")
    assert(result.uri is None)
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af is None)
    assert(result.responses[0].body_size == 1406)
    assert(result.responses[0].head_size == 263)
    assert(result.responses[0].destination_address == "193.0.6.139")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 30.229)
    assert(result.responses[0].source_address is None)
    assert(result.responses[0].version is None)

def test_http_4430():
    result = Result.get('{"from":"62.194.83.50","fw":4430,"msm_id":12023,"prb_id":1,"result":[{"addr":"193.0.6.139","bsize":1406,"hsize":263,"mode":"GET4","res":200,"rt":27.276,"srcaddr":"192.168.99.183","ver":"1.1"}],"timestamp":1336418202,"type":"http"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "62.194.83.50")
    assert(result.firmware == 4430)
    assert(result.measurement_id == 12023)
    assert(result.probe_id == 1)
    assert(result.created.isoformat() == "2012-05-07T19:16:42+00:00")
    assert(result.uri is None)
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af is None)
    assert(result.responses[0].body_size == 1406)
    assert(result.responses[0].head_size == 263)
    assert(result.responses[0].destination_address == "193.0.6.139")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 27.276)
    assert(result.responses[0].source_address == "192.168.99.183")
    assert(result.responses[0].version == "1.1")

def test_http_4460():
    result = Result.get('{"from":"2001:780:100:6:220:4aff:fee0:2479","fw":4460,"msm_id":1003930,"prb_id":2707,"result":[{"af":6,"bsize":22383,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":71.146000000000001,"src_addr":"2001:780:100:6:220:4aff:fee0:2479","ver":"1.1"}],"timestamp":1350471605,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2001:780:100:6:220:4aff:fee0:2479")
    assert(result.firmware == 4460)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 2707)
    assert(result.created.isoformat() == "2012-10-17T11:00:05+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 22383)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 71.146)
    assert(result.responses[0].source_address == result.origin)
    assert(result.responses[0].version == "1.1")


def test_http_4470():
    result = Result.get('{"from":"2001:4538:100:0:220:4aff:fec8:232b","fw":4470,"msm_id":1003930,"prb_id":303,"result":[{"af":6,"bsize":22243,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":765.25400000000002,"src_addr":"2001:4538:100:0:220:4aff:fec8:232b","ver":"1.1"}],"timestamp":1352869218,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2001:4538:100:0:220:4aff:fec8:232b")
    assert(result.firmware == 4470)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 303)
    assert(result.created.isoformat() == "2012-11-14T05:00:18+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 22243)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 765.254)
    assert(result.responses[0].source_address == result.origin)
    assert(result.responses[0].version == "1.1")


def test_http_4480():
    result = Result.get('{"fw":4480,"msm_id":1003930,"prb_id":2184,"result":[{"af":6,"bsize":39777,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":660.40999999999997,"src_addr":"2a02:6c80:5:0:220:4aff:fee0:2774","ver":"1.1"}],"src_addr":"2a02:6c80:5:0:220:4aff:fee0:2774","timestamp":1372582858,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin is None)
    assert(result.firmware == 4480)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 2184)
    assert(result.created.isoformat() == "2013-06-30T09:00:58+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 39777)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 660.41)
    assert(result.responses[0].source_address == "2a02:6c80:5:0:220:4aff:fee0:2774")
    assert(result.responses[0].version == "1.1")


def test_http_4500():
    result = Result.get('{"from":"2a02:8304:1:4:220:4aff:fee0:228d","fw":4500,"msm_id":1003930,"prb_id":2954,"result":[{"af":6,"bsize":40103,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":234.048,"src_addr":"2a02:8304:1:4:220:4aff:fee0:228d","ver":"1.1"}],"timestamp":1367233244,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2a02:8304:1:4:220:4aff:fee0:228d")
    assert(result.firmware == 4500)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 2954)
    assert(result.created.isoformat() == "2013-04-29T11:00:44+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 40103)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 234.048)
    assert(result.responses[0].source_address == result.origin)
    assert(result.responses[0].version == "1.1")


def test_http_4520():
    result = Result.get('{"from":"2a02:27d0:100:115:6000::250","fw":4520,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":2802,"result":[{"af":6,"bsize":40567,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":102.825,"src_addr":"2a02:27d0:100:115:6000::250","ver":"1.1"}],"timestamp":1379594363,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2a02:27d0:100:115:6000::250")
    assert(result.firmware == 4520)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 2802)
    assert(result.created.isoformat() == "2013-09-19T12:39:23+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 40567)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 102.825)
    assert(result.responses[0].source_address == result.origin)
    assert(result.responses[0].version == "1.1")


def test_http_4540():
    result = Result.get('{"from":"2001:980:36af:1:220:4aff:fec8:226d","fw":4540,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":26,"result":[{"af":6,"bsize":40485,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":158.994,"src_addr":"2001:980:36af:1:220:4aff:fec8:226d","ver":"1.1"}],"timestamp":1377695803,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2001:980:36af:1:220:4aff:fec8:226d")
    assert(result.firmware == 4540)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 26)
    assert(result.created.isoformat() == "2013-08-28T13:16:43+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 40485)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 158.994)
    assert(result.responses[0].source_address == "2001:980:36af:1:220:4aff:fec8:226d")
    assert(result.responses[0].version == "1.1")


def test_http_4550():
    result = Result.get('{"from":"2001:4538:100:0:220:4aff:fec8:232b","fw":4550,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":303,"result":[{"af":6,"bsize":40118,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":2092.447,"src_addr":"2001:4538:100:0:220:4aff:fec8:232b","ver":"1.1"}],"timestamp":1380901810,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2001:4538:100:0:220:4aff:fec8:232b")
    assert(result.firmware == 4550)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 303)
    assert(result.created.isoformat() == "2013-10-04T15:50:10+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 40118)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 2092.447)
    assert(result.responses[0].source_address == "2001:4538:100:0:220:4aff:fec8:232b")
    assert(result.responses[0].version == "1.1")


def test_http_4560():
    result = Result.get('{"from":"2620:0:2ed0:aaaa::210","fw":4560,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":1164,"result":[{"af":6,"bsize":39340,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":739.26999999999998,"src_addr":"2620:0:2ed0:aaaa::210","ver":"1.1"}],"timestamp":1385895661,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2620:0:2ed0:aaaa::210")
    assert(result.firmware == 4560)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 1164)
    assert(result.created.isoformat() == "2013-12-01T11:01:01+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 39340)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 739.27)
    assert(result.responses[0].source_address == "2620:0:2ed0:aaaa::210")
    assert(result.responses[0].version == "1.1")


def test_http_4570():
    result = Result.get('{"from":"2001:8b0:34f:5b8:220:4aff:fee0:21fc","fw":4570,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":2030,"result":[{"af":6,"bsize":41021,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":187.02199999999999,"src_addr":"2001:8b0:34f:5b8:220:4aff:fee0:21fc","ver":"1.1"}],"timestamp":1395324614,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2001:8b0:34f:5b8:220:4aff:fee0:21fc")
    assert(result.firmware == 4570)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 2030)
    assert(result.created.isoformat() == "2014-03-20T14:10:14+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 41021)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 187.022)
    assert(result.responses[0].source_address == "2001:8b0:34f:5b8:220:4aff:fee0:21fc")
    assert(result.responses[0].version == "1.1")


def test_http_4600():
    result = Result.get('{"from":"2a01:6a8:0:f:220:4aff:fec5:5b5a","fw":4600,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":720,"result":[{"af":6,"bsize":41020,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":195.84399999999999,"src_addr":"2a01:6a8:0:f:220:4aff:fec5:5b5a","ver":"1.1"}],"timestamp":1396163194,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2a01:6a8:0:f:220:4aff:fec5:5b5a")
    assert(result.firmware == 4600)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 720)
    assert(result.created.isoformat() == "2014-03-30T07:06:34+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 41020)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 195.844)
    assert(result.responses[0].source_address == "2a01:6a8:0:f:220:4aff:fec5:5b5a")
    assert(result.responses[0].version == "1.1")


def test_http_4610():
    result = Result.get('{"from":"2a01:9e00:a217:d00:220:4aff:fec6:cb5b","fw":4610,"group_id":1003930,"msm_id":1003930,"msm_name":"HTTPGet","prb_id":780,"result":[{"af":6,"bsize":41020,"dst_addr":"2001:67c:2e8:22::c100:68b","hsize":279,"method":"GET","res":200,"rt":154.755,"src_addr":"2a01:9e00:a217:d00:220:4aff:fec6:cb5b","ver":"1.1"}],"timestamp":1396359320,"type":"http","uri":"http://www.ripe.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2a01:9e00:a217:d00:220:4aff:fec6:cb5b")
    assert(result.firmware == 4610)
    assert(result.measurement_id == 1003930)
    assert(result.probe_id == 780)
    assert(result.created.isoformat() == "2014-04-01T13:35:20+00:00")
    assert(result.uri == "http://www.ripe.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size == 41020)
    assert(result.responses[0].head_size == 279)
    assert(result.responses[0].destination_address == "2001:67c:2e8:22::c100:68b")
    assert(result.responses[0].code == 200)
    assert(result.responses[0].response_time == 154.755)
    assert(result.responses[0].source_address == "2a01:9e00:a217:d00:220:4aff:fec6:cb5b")
    assert(result.responses[0].version == "1.1")


def test_http_4610_fail():
    result = Result.get('{"from":"2001:630:301:1080:220:4aff:fee0:20a0","fw":4610,"msm_id":1003932,"msm_name":"HTTPGet","prb_id":2493,"result":[{"af":6,"dst_addr":"2001:42d0:0:200::6","err":"timeout reading chunk","method":"GET","src_addr":"2001:630:301:1080:220:4aff:fee0:20a0"}],"timestamp":1398184661,"type":"http","uri":"http://www.afrinic.net/"}')
    assert(isinstance(result, HttpResult))
    assert(result.origin == "2001:630:301:1080:220:4aff:fee0:20a0")
    assert(result.firmware == 4610)
    assert(result.measurement_id == 1003932)
    assert(result.probe_id == 2493)
    assert(result.created.isoformat() == "2014-04-22T16:37:41+00:00")
    assert(result.uri == "http://www.afrinic.net/")
    assert(result.method == HttpResult.METHOD_GET)
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 6)
    assert(result.responses[0].body_size is None)
    assert(result.responses[0].head_size is None)
    assert(result.responses[0].destination_address == "2001:42d0:0:200::6")
    assert(result.responses[0].code is None)
    assert(result.responses[0].response_time is None)
    assert(result.responses[0].source_address == "2001:630:301:1080:220:4aff:fee0:20a0")
    assert(result.responses[0].version is None)
    assert(result.responses[0].is_error is True)
    assert(result.responses[0].error_message == "timeout reading chunk")

def test_http_lts():
    result = Result.get('{"lts":275,"from":"","msm_id":1003932,"fw":4650,"timestamp":1406558081,"uri":"http:\/\/www.afrinic.net\/","prb_id":902,"result":[{"method":"GET","dst_addr":"2001:42d0:0:200::6","err":"connect: Network is unreachable","af":6}],"type":"http","msm_name":"HTTPGet"}')
    assert(result.seconds_since_sync == 275)

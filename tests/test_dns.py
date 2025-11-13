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

from collections import namedtuple

from ripe.atlas.sagan import Result, ResultError
from ripe.atlas.sagan.dns import (
    DnsResult, Edns0, Answer,
    AAnswer, AaaaAnswer, NsAnswer, CnameAnswer, MxAnswer, SoaAnswer, DsAnswer,
    DnskeyAnswer, RRSigAnswer, NsecAnswer, Nsec3Answer, Nsec3ParamAnswer,
    PtrAnswer, SrvAnswer, SshfpAnswer, TxtAnswer, HinfoAnswer, TlsaAnswer
)


def test_dns_4460():
    result = Result.get('{"af":4,"dst_addr":"193.227.234.53","from":"217.172.81.146","fw":4460,"msm_id":1004041,"prb_id":184,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":39825,"NSCOUNT":0,"QDCOUNT":1,"abuf":"m5GEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==","answers":[{"RDLENGTH":4,"TYPE":1}],"rt":45.305,"size":43},"timestamp":1347765990,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin == "217.172.81.146")
    assert(result.firmware == 4460)
    assert(result.measurement_id == 1004041)
    assert(result.probe_id == 184)
    assert(result.created.isoformat() == "2012-09-16T03:26:30+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "193.227.234.53")
    assert(result.responses[0].source_address is None)
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "m5GEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==")
    assert(result.responses[0].response_time == 45.305)
    assert(result.responses[0].response_size == 43)
    assert(result.responses[0].abuf.header.aa is True)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 0)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is False)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 0)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is False)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 39825)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "as250.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "as250.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].address == "194.150.168.100")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)


def test_dns_4470():
    result = Result.get('{"af":4,"dst_addr":"193.227.234.53","from":"195.47.235.67","fw":4470,"msm_id":1004041,"prb_id":148,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":63020,"NSCOUNT":0,"QDCOUNT":1,"abuf":"9iyEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==","rt":30.733000000000001,"size":43},"src_addr":"195.47.235.67","timestamp":1352273196,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin == "195.47.235.67")
    assert(result.firmware == 4470)
    assert(result.measurement_id == 1004041)
    assert(result.probe_id == 148)
    assert(result.created.isoformat() == "2012-11-07T07:26:36+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "193.227.234.53")
    assert(result.responses[0].source_address == "195.47.235.67")
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "9iyEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==")
    assert(result.responses[0].response_time == 30.733)
    assert(result.responses[0].response_size == 43)
    assert(result.responses[0].abuf.header.aa is True)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 0)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is False)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 0)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is False)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 63020)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "as250.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "as250.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].address == "194.150.168.100")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)


def test_dns_4480():
    result = Result.get('{"af":4,"dst_addr":"193.227.234.53","from":"46.17.16.18","fw":4480,"msm_id":1004041,"prb_id":778,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":12288,"NSCOUNT":0,"QDCOUNT":1,"abuf":"MACEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==","rt":38.576999999999998,"size":43},"src_addr":"192.168.1.12","timestamp":1363332374,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin == "46.17.16.18")
    assert(result.firmware == 4480)
    assert(result.measurement_id == 1004041)
    assert(result.probe_id == 778)
    assert(result.created.isoformat() == "2013-03-15T07:26:14+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "193.227.234.53")
    assert(result.responses[0].source_address == "192.168.1.12")
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "MACEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==")
    assert(result.responses[0].response_time == 38.577)
    assert(result.responses[0].response_size == 43)
    assert(result.responses[0].abuf.header.aa is True)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 0)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is False)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 0)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is False)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 12288)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "as250.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "as250.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].address == "194.150.168.100")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)


def test_dns_4500():
    result = Result.get('{"af":4,"dst_addr":"193.227.234.53","from":"176.28.80.97","fw":4500,"msm_id":1004041,"prb_id":2918,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":57235,"NSCOUNT":0,"QDCOUNT":1,"abuf":"35OEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==","rt":69.736999999999995,"size":43},"src_addr":"10.220.3.215","timestamp":1366255550,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin == "176.28.80.97")
    assert(result.firmware == 4500)
    assert(result.measurement_id == 1004041)
    assert(result.probe_id == 2918)
    assert(result.created.isoformat() == "2013-04-18T03:25:50+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "193.227.234.53")
    assert(result.responses[0].source_address == "10.220.3.215")
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "35OEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaoZA==")
    assert(result.responses[0].response_time == 69.737)
    assert(result.responses[0].response_size == 43)
    assert(result.responses[0].abuf.header.aa is True)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 0)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is False)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 0)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is False)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 57235)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "as250.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "as250.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].address == "194.150.168.100")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)


def test_dns_4520():
    result = Result.get('{"af":4,"dst_addr":"193.227.234.53","fw":4520,"msm_id":1004041,"prb_id":203,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":1472,"NSCOUNT":0,"QDCOUNT":1,"abuf":"BcCEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaooA==","rt":362.416,"size":43},"src_addr":"118.208.45.191","timestamp":1373241512,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin is None)
    assert(result.firmware == 4520)
    assert(result.measurement_id == 1004041)
    assert(result.probe_id == 203)
    assert(result.created.isoformat() == "2013-07-07T23:58:32+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "193.227.234.53")
    assert(result.responses[0].source_address == "118.208.45.191")
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "BcCEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaooA==")
    assert(result.responses[0].response_time == 362.416)
    assert(result.responses[0].response_size == 43)
    assert(result.responses[0].abuf.header.aa is True)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 0)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is False)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 0)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is False)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 1472)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "as250.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "as250.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].address == "194.150.168.160")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)


def test_dns_4610():
    result = Result.get('{"af":4,"dst_addr":"193.227.234.53","from":"79.134.181.58","fw":4610,"msm_id":1004041,"msm_name":"Tdig","prb_id":714,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":15824,"NSCOUNT":0,"QDCOUNT":1,"abuf":"PdCEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaooA==","rt":81.718000000000004,"size":43},"result-rt":81.718000000000004,"src_addr":"192.168.0.100","timestamp":1395856407,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin == "79.134.181.58")
    assert(result.firmware == 4610)
    assert(result.measurement_id == 1004041)
    assert(result.probe_id == 714)
    assert(result.created.isoformat() == "2014-03-26T17:53:27+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 1)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "193.227.234.53")
    assert(result.responses[0].source_address == "192.168.0.100")
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "PdCEAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaooA==")
    assert(result.responses[0].response_time == 81.718)
    assert(result.responses[0].response_size == 43)
    assert(result.responses[0].abuf.header.aa is True)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 0)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is False)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 0)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is False)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 15824)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "as250.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "as250.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].address == "194.150.168.160")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)


def test_resultset():
    result = Result.get('{"from":"87.218.115.95","fw":4610,"msm_id":1004049,"msm_name":"Tdig","prb_id":13337,"resultset":[{"af":4,"dst_addr":"192.168.1.1","proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":6,"ID":19506,"NSCOUNT":6,"QDCOUNT":1,"abuf":"TDKBgAABAAEABgAGA3d3dwRyaXBlA25ldAAAAQABwAwAAQABAAAnsgAEwQAGi8AQAAIAAQAACTsADANuczMDbmljAmZyAMAQAAIAAQAACTsAEAZzbnMtcGIDaXNjA29yZwDAEAACAAEAAAk7AA0Ec2VjMQVhcG5pY8AVwBAAAgABAAAJOwAOA3ByaQdhdXRoZG5zwBDAEAACAAEAAAk7AA4GdGlubmllBGFyaW7AFcAQAAIAAQAACTsABwRzZWMzwHPAOgABAAEAASqyAATAhgAxwFIAAQABAAAZUgAEwAUEAcBuAAEAAQAAAW0ABMoMHTvAhwABAAEAAAk7AATBAAkFwKEAAQABAAAWlAAEx9QANcC7AAEAAQAACjcABMoMHIw=","rt":2.9939999999999998,"size":290},"src_addr":"192.168.1.2","subid":1,"submax":3,"time":1395792203},{"af":4,"dst_addr":"109.69.8.34","proto":"UDP","result":{"ANCOUNT":2,"ARCOUNT":15,"ID":25432,"NSCOUNT":7,"QDCOUNT":1,"abuf":"Y1iBgAABAAIABwAPA3d3dwRyaXBlA25ldAAAAQABwAwAAQABAAAnsAAEwQAGi8AMAC4AAQAAJ7AAnAABBQMAAFRgU1kk1VMxicVypgRyaXBlA25ldAAO4dloUjFkGWQKhb7ovCvAUn0NxHnxhCG/8PxtVf2+gUCxU1DAwP6mhazefe/B7Ecz5EVaF0WpbNUwhYOlEApMVgxd26DzrH7n99Yx8XN+mp/jts7MhoXrybZyh4NJ4Lwd/eAxCwp81ZAj7YDUX+EVtM+8c5h72C1XVfYb3Q/k98BMAAIAAQAACToADQRzZWMxBWFwbmljwFHATAACAAEAAAk6ABAGc25zLXBiA2lzYwNvcmcAwEwAAgABAAAJOgAOA3ByaQdhdXRoZG5zwEzATAACAAEAAAk6AAwDbnMzA25pYwJmcgDATAACAAEAAAk6AAcEc2VjM8DnwEwAAgABAAAJOgAOBnRpbm5pZQRhcmluwFHATAAuAAEAAA3RAJwAAgUCAAAOEFNZJNVTMYnFcqYEcmlwZQNuZXQAPVTDPwe6Z82fnZBvGzBGjFgX/CLRCE0Z6atTKBxqGAMbQzoqFMv+pfqjwe/wTEcIJnWqvPRGxnERAFYRpEi/Fjws7ELstYPOGUaY/GU8J0j0wJ6xJzr0gF8RYHKzvSwV2b2v2pJqCWYx0v03Mzv9UOXxE3Yj0WgSqKLsRckUDvDBMQABAAEAASqxAATAhgAxwTEAHAABAAEqsQAQIAEGYDAGAAEAAAAAAAEAAcEXAAEAAQAACToABMEACQXBFwAcAAEAAAk6ABAgAQZ8AOAAAAAAAAAAAAAFwOIAAQABAAABbAAEygwdO8DiABwAAQAAAWwAECABDcAgAQAKRggAAAAAAFnBSQABAAEAAAo2AATKDByMwUkAHAABAAAKNgAQIAENwAABAABHdwAAAAABQMD7AAEAAQAAGVEABMAFBAHA+wAcAAEAABlRABAgAQUAAC4AAAAAAAAAAAABwVwAAQABAAAWkgAEx9QANcFcABwAAQAAFpIAECABBQAAEwAAAAAAAMfUADXBMQAuAAEAASqxAJoAAQgDAAKjAFM4bf9TLyzfq04DbmljAmZyAAoIofy0bTrtF6fosXpt3PoQAQK2NStYRCEn/n6x+AqYbqeqh26q7gP94d2PeMAPV+sVRcY9ZgoRu2a7GmE4bxwzr3MlcAyv/MHiOU2f7eW0xDegtoL5GXnLgLx0+CvoG8lbiquEQNRxVNqQ2G4FdwvjYPnirfxmFKsW6YhTradrwTEALgABAAEqsQCaABwIAwACowBTObYgUzA3a6tOA25pYwJmcgBSd6DmR9159Y1jhnViTvqjnB0Tq0EjZVL2O5G8EiAgq4sYY2BtOL/zrM6/wohJ7hVBtPRWJ1xEf9WQsm/oZeJUThPp52GjB2fEboxJct/4k7i3wNZ6gN2krl1vNb5CrOiaVpDcdJMmZTkrua4LV4uB+buS0hvZ15D5KtODmgke8wAAKRAAAACAAAAA","rt":76.292000000000002,"size":1137},"src_addr":"192.168.1.2","subid":2,"submax":3,"time":1395792204},{"af":4,"dst_addr":"8.8.8.8","proto":"UDP","result":{"ANCOUNT":2,"ARCOUNT":1,"ID":34160,"NSCOUNT":0,"QDCOUNT":1,"abuf":"hXCBoAABAAIAAAABA3d3dwRyaXBlA25ldAAAAQABwAwAAQABAAAs2AAEwQAGi8AMAC4AAQAALNgAnAABBQMAAFRgU1kk1VMxicVypgRyaXBlA25ldAAO4dloUjFkGWQKhb7ovCvAUn0NxHnxhCG/8PxtVf2+gUCxU1DAwP6mhazefe/B7Ecz5EVaF0WpbNUwhYOlEApMVgxd26DzrH7n99Yx8XN+mp/jts7MhoXrybZyh4NJ4Lwd/eAxCwp81ZAj7YDUX+EVtM+8c5h72C1XVfYb3Q/k9wAAKQIAAACAAAAA","rt":79.971000000000004,"size":225},"src_addr":"192.168.1.2","subid":3,"submax":3,"time":1395792205}],"timestamp":1395792203,"type":"dns"}')
    assert(isinstance(result, DnsResult))
    assert(result.origin == "87.218.115.95")
    assert(result.firmware == 4610)
    assert(result.measurement_id == 1004049)
    assert(result.probe_id == 13337)
    assert(result.created.isoformat() == "2014-03-26T00:03:23+00:00")
    assert(isinstance(result.responses, list))
    assert(len(result.responses) == 3)
    assert(result.responses[0].af == 4)
    assert(result.responses[0].destination_address == "192.168.1.1")
    assert(result.responses[0].source_address == "192.168.1.2")
    assert(result.responses[0].protocol == DnsResult.PROTOCOL_UDP)
    assert(str(result.responses[0].abuf) == "TDKBgAABAAEABgAGA3d3dwRyaXBlA25ldAAAAQABwAwAAQABAAAnsgAEwQAGi8AQAAIAAQAACTsADANuczMDbmljAmZyAMAQAAIAAQAACTsAEAZzbnMtcGIDaXNjA29yZwDAEAACAAEAAAk7AA0Ec2VjMQVhcG5pY8AVwBAAAgABAAAJOwAOA3ByaQdhdXRoZG5zwBDAEAACAAEAAAk7AA4GdGlubmllBGFyaW7AFcAQAAIAAQAACTsABwRzZWMzwHPAOgABAAEAASqyAATAhgAxwFIAAQABAAAZUgAEwAUEAcBuAAEAAQAAAW0ABMoMHTvAhwABAAEAAAk7AATBAAkFwKEAAQABAAAWlAAEx9QANcC7AAEAAQAACjcABMoMHIw=")
    assert(result.responses[0].response_time == 2.994)
    assert(result.responses[0].response_size == 290)
    assert(result.responses[0].abuf.header.aa is False)
    assert(result.responses[0].abuf.header.qr is True)
    assert(result.responses[0].abuf.header.nscount == 6)
    assert(result.responses[0].abuf.header.qdcount == 1)
    assert(result.responses[0].abuf.header.ancount == 1)
    assert(result.responses[0].abuf.header.tc is False)
    assert(result.responses[0].abuf.header.rd is True)
    assert(result.responses[0].abuf.header.cd is False)
    assert(result.responses[0].abuf.header.ad is False)
    assert(result.responses[0].abuf.header.arcount == 6)
    assert(result.responses[0].abuf.header.return_code == "NOERROR")
    assert(result.responses[0].abuf.header.opcode == "QUERY")
    assert(result.responses[0].abuf.header.ra is True)
    assert(result.responses[0].abuf.header.z == 0)
    assert(result.responses[0].abuf.header.id == 19506)
    assert(result.responses[1].abuf.header.id == 25432)
    assert(result.responses[2].abuf.header.id == 34160)
    assert(isinstance(result.responses[0].abuf.questions, list))
    assert(result.responses[0].abuf.questions[0].klass == "IN")
    assert(result.responses[0].abuf.questions[0].type == "A")
    assert(result.responses[0].abuf.questions[0].name == "www.ripe.net.")
    assert(result.responses[1].abuf.questions[0].type == "A")
    assert(result.responses[2].abuf.questions[0].name == "www.ripe.net.")
    assert(isinstance(result.responses[0].abuf.answers, list))
    assert(isinstance(result.responses[0].abuf.answers[0], AAnswer))
    assert(result.responses[0].abuf.answers[0].name == "www.ripe.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 10162)
    assert(result.responses[0].abuf.answers[0].address == "193.0.6.139")
    assert(result.responses[0].abuf.answers[0].type == "A")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 4)
    assert(result.responses[1].abuf.answers[1].rd_length == 156)
    assert(isinstance(result.responses[0].abuf.authorities, list))
    assert(len(result.responses[0].abuf.authorities) == 6)
    assert(result.responses[0].abuf.authorities[0].target == "ns3.nic.fr.")
    assert(result.responses[0].abuf.authorities[1].target == "sns-pb.isc.org.")
    assert(result.responses[0].abuf.authorities[2].target == "sec1.apnic.net.")
    assert(result.responses[0].abuf.authorities[3].target == "pri.authdns.ripe.net.")
    assert(result.responses[0].abuf.authorities[4].rd_length == 14)
    assert(result.responses[0].abuf.authorities[5].ttl == 2363)
    assert(result.responses[0].abuf.authorities[5].type == "NS")
    assert(result.responses[0].abuf.authorities[1].rd_length == 16)
    assert(result.responses[0].abuf.authorities[2].ttl == 2363)
    assert(result.responses[0].abuf.authorities[3].target == "pri.authdns.ripe.net.")
    assert(isinstance(result.responses[0].abuf.additionals, list))
    assert(len(result.responses[0].abuf.additionals) == 6)
    assert(result.responses[0].abuf.additionals[0].address == "192.134.0.49")
    assert(result.responses[0].abuf.additionals[1].klass == "IN")
    assert(result.responses[0].abuf.additionals[2].name == "sec1.apnic.net.")
    assert(result.responses[0].abuf.additionals[3].rd_length == 4)
    assert(result.responses[0].abuf.additionals[4].ttl == 5780)
    assert(result.responses[0].abuf.additionals[3].type == "A")


def test_edns0():
    result = Result.get('{"from":"2001:d98:6004:1:6666:b3ff:feb0:ec1e","msm_id":1004048,"timestamp":1398939936,"fw":4610,"proto":"UDP","af":6,"result-rdata":null,"dst_addr":"2001:7fd::1","prb_id":14184,"result":{"abuf":"ACuEAAABAAEADQAYAAAGAAEAAAYAAQABUYAAQAFhDHJvb3Qtc2VydmVycwNuZXQABW5zdGxkDHZlcmlzaWduLWdycwNjb20AeAv3NAAABwgAAAOEAAk6gAABUYAAAAIAAQAH6QAAAsAcAAACAAEAB+kAAAQBYsAeAAACAAEAB+kAAAQBY8AeAAACAAEAB+kAAAQBZMAeAAACAAEAB+kAAAQBZcAeAAACAAEAB+kAAAQBZsAeAAACAAEAB+kAAAQBZ8AeAAACAAEAB+kAAAQBaMAeAAACAAEAB+kAAAQBacAeAAACAAEAB+kAAAQBasAeAAACAAEAB+kAAAQBa8AeAAACAAEAB+kAAAQBbMAeAAACAAEAB+kAAAQBbcAewBwAAQABAAfpAAAExikABMB0AAEAAQAH6QAABMDkT8nAgwABAAEAB+kAAATAIQQMwJIAAQABAAfpAAAExwdbDcChAAEAAQAH6QAABMDL5grAsAABAAEAB+kAAATABQXxwL8AAQABAAfpAAAEwHAkBMDOAAEAAQAH6QAABIA\/AjXA3QABAAEAB+kAAATAJJQRwOwAAQABAAfpAAAEwDqAHsD7AAEAAQAH6QAABMEADoHBCgABAAEAB+kAAATHB1MqwRkAAQABAAfpAAAEygwbIcAcABwAAQAH6QAAECABBQO6PgAAAAAAAAACADDAgwAcAAEAB+kAABAgAQUAAAIAAAAAAAAAAAAMwJIAHAABAAfpAAAQIAEFAAAtAAAAAAAAAAAADcCwABwAAQAH6QAAECABBQAALwAAAAAAAAAAAA\/AzgAcAAEAB+kAABAgAQUAAAEAAAAAAACAPwI1wN0AHAABAAfpAAAQIAEH\/gAAAAAAAAAAAAAAU8DsABwAAQAH6QAAECABBQMMJwAAAAAAAAACADDA+wAcAAEAB+kAABAgAQf9AAAAAAAAAAAAAAABwQoAHAABAAfpAAAQIAEFAAADAAAAAAAAAAAAQsEZABwAAQAH6QAAECABDcMAAAAAAAAAAAAAADUAACkQAAAAAAAAGAADABRrMy5hbXMtaXguay5yaXBlLm5ldA==","rt":219.205,"NSCOUNT":13,"QDCOUNT":1,"answers":[{"RNAME":"nstld.verisign-grs.com.","NAME":".","MNAME":"a.root-servers.net.","TTL":86400,"SERIAL":2014050100,"TYPE":"SOA"}],"ID":43,"ARCOUNT":24,"ANCOUNT":1,"size":808},"type":"dns","result-rname":"nstld.verisign-grs.com.","src_addr":"2001:d98:6004:1:6666:b3ff:feb0:ec1e","result-rt":219.205,"result-serial":2014050100,"msm_name":"Tdig"}')
    assert(isinstance(result, DnsResult))
    assert(isinstance(result.responses, list))
    assert(isinstance(result.responses[0].abuf.edns0, Edns0))
    assert(result.responses[0].abuf.edns0.extended_return_code == 0)
    assert(result.responses[0].abuf.edns0.name == ".")
    assert(result.responses[0].abuf.edns0.type == "OPT")
    assert(result.responses[0].abuf.edns0.udp_size == 4096)
    assert(result.responses[0].abuf.edns0.version == 0)
    assert(result.responses[0].abuf.edns0.z == 0)
    assert(isinstance(result.responses[0].abuf.edns0.options, list))
    assert(len(result.responses[0].abuf.edns0.options) == 1)
    assert(result.responses[0].abuf.edns0.options[0].nsid == "k3.ams-ix.k.ripe.net")
    assert(result.responses[0].abuf.edns0.options[0].code == 3)
    assert(result.responses[0].abuf.edns0.options[0].length == 20)
    assert(result.responses[0].abuf.edns0.options[0].name == "NSID")


def test_error_timeout():
    broken_result = {u'from': u'84.132.219.105', u'msm_id': 1666006, u'timestamp':1400570732, u'fw': 4610, u'proto': u'UDP', u'af': 4, u'msm_name':u'Tdig', u'prb_id': 2960, u'error': {u'timeout': 5000}, u'src_addr':u'192.168.179.20', u'group_id': 1666005, u'type': u'dns', u'dst_addr':u'194.0.25.16'}
    result = Result.get(broken_result)
    assert(result.is_error is True)
    try:
        Result.get(broken_result, on_error=Result.ACTION_FAIL)
        assert False
    except ResultError as e:
        assert(str(e) == "Timeout: 5000")


def test_qbuf_single_result():

    result = Result.get('{"af":6,"dst_addr":"2001:67c:e0::5","from":"2a02:2860:3:1::a","fw":4720,"group_id":2927179,"lts":30,"msm_id":2927179,"msm_name":"Tdig","prb_id":18279,"proto":"UDP","qbuf":"CcsAAAABAAAAAAABBHJpcGUDbmV0AAAcAAEAACkCAAAAgAAAAAAAAAA=","result":{"ANCOUNT":2,"ARCOUNT":1,"ID":2507,"NSCOUNT":0,"QDCOUNT":1,"abuf":"CcuEAAABAAIAAAABBHJpcGUDbmV0AAAcAAHADAAcAAEAAAEsABAgAQZ8AugAIgAAAADBAAaLwAwALgABAAABLACcABwFAgAAASxWap83VkMEJ4yCBHJpcGUDbmV0ADyhc2zuMQhsu3nU8h2qGCjw/uQM3bzqsrfbaFfSCDH3qG3pPuYJtyzkyFpI8jsUpzYjJJoy29XPeAdqXWoSsHQAD4AhVqmg0/YBctjZuIMKPs7kI3ZWjkkpVqn9kl2OT0r+Moh+gL1W/a1uIkldil0mNCi1xp/V6bRqZfCS+bL0AAApEAAAAIAAAAA=","rt":21.768,"size":233},"src_addr":"2a02:2860:3:1::a","timestamp":1447251248,"type":"dns"}')
    assert(str(result.responses[0].qbuf) == "CcsAAAABAAAAAAABBHJpcGUDbmV0AAAcAAEAACkCAAAAgAAAAAAAAAA=")
    assert(result.responses[0].qbuf.edns0.do is True)


def test_qbuf_result_set():

    result = Result.get('{"from":"208.118.139.24","fw":4610,"group_id":1666151,"msm_id":1666151,"msm_name":"Tdig","prb_id":15112,"resultset":[{"af":4,"dst_addr":"8.8.8.8","proto":"TCP","qbuf":"dakBgAABAAAAAAABBTE1MTEyCjE0MDA2NjU1MjMDd3d3B3R3aXR0ZXIDY29tAAABAAEAACkCAAAAgAAABAADAAA=","result":{"ANCOUNT":0,"ARCOUNT":1,"ID":30121,"NSCOUNT":1,"QDCOUNT":1,"rt":57.764,"size":133},"src_addr":"10.0.5.101","subid":1,"submax":2,"time":1400665523},{"af":4,"dst_addr":"8.8.4.4","proto":"TCP","qbuf":"JTEBgAABAAAAAAABBTE1MTEyCjE0MDA2NjU1MjQDd3d3B3R3aXR0ZXIDY29tAAABAAEAACkCAAAAgAAABAADAAA=","result":{"ANCOUNT":0,"ARCOUNT":1,"ID":9521,"NSCOUNT":1,"QDCOUNT":1,"rt":57.263,"size":133},"src_addr":"10.0.5.101","subid":2,"submax":2,"time":1400665524}],"timestamp":1400665523,"type":"dns"}')
    assert(result.responses[0].abuf is None)
    assert(str(result.responses[0].qbuf) == "dakBgAABAAAAAAABBTE1MTEyCjE0MDA2NjU1MjMDd3d3B3R3aXR0ZXIDY29tAAABAAEAACkCAAAAgAAABAADAAA=")
    assert(result.responses[0].qbuf.header.aa is False)
    assert(result.responses[0].qbuf.header.qr is False)
    assert(result.responses[0].qbuf.header.nscount == 0)
    assert(result.responses[0].qbuf.header.qdcount == 1)
    assert(result.responses[0].qbuf.header.ancount == 0)
    assert(result.responses[0].qbuf.header.tc is False)
    assert(result.responses[0].qbuf.header.rd is True)
    assert(result.responses[0].qbuf.header.arcount == 1)
    assert(result.responses[0].qbuf.header.return_code == "NOERROR")
    assert(result.responses[0].qbuf.header.opcode == "QUERY")
    assert(result.responses[0].qbuf.header.ra is True)
    assert(result.responses[0].qbuf.header.z == 0)
    assert(result.responses[0].qbuf.header.id == 30121)
    assert(len(result.responses[0].qbuf.questions) == 1)
    assert(result.responses[0].qbuf.questions[0].klass == "IN")
    assert(result.responses[0].qbuf.questions[0].type == "A")
    assert(result.responses[0].qbuf.questions[0].name == "15112.1400665523.www.twitter.com.")
    assert(result.responses[0].qbuf.edns0.extended_return_code == 0)
    assert(result.responses[0].qbuf.edns0.udp_size == 512)
    assert(result.responses[0].qbuf.edns0.version == 0)
    assert(result.responses[0].qbuf.edns0.z == 0)
    assert(result.responses[0].qbuf.edns0.type == "OPT")
    assert(result.responses[0].qbuf.edns0.name == ".")
    assert(len(result.responses[0].qbuf.edns0.options) == 1)
    assert(result.responses[0].qbuf.edns0.options[0].code == 3)
    assert(result.responses[0].qbuf.edns0.options[0].name == "NSID")
    assert(result.responses[0].qbuf.edns0.options[0].nsid == "")
    assert(result.responses[0].qbuf.edns0.options[0].length == 0)


def test_aaaaanswer():
    result = Result.get('{"from":"2001:67c:2e8:11::c100:136c","msm_id":1663540,"fw":4620,"af":6,"timestamp":1403091608,"proto":"UDP","dst_addr":"2001:41d0:1:4874::1","prb_id":6012,"result":{"abuf":"1jKEAAABAAEAAgADCnBvc3RtYXN0ZXICZnIAABwAAcAMABwAAQAAASwAECABQdAAAUh0AAAAAAAAAAHADAACAAEAAAEsAAYDbnMxwAzADAACAAEAAAEsAAYDbnMywAzARwABAAEAAAEsAARXYtl0wEcAHAABAAABLAAQIAFB0AABSHQAAAAAAAAAAcBZAAEAAQAAASwABFzzEZ8=","rt":8.656,"NSCOUNT":2,"QDCOUNT":1,"ANCOUNT":1,"ARCOUNT":3,"ID":54834,"size":155},"result-rt":8.656,"src_addr":"2001:67c:2e8:11::c100:136c","group_id":1663540,"type":"dns","msm_name":"Tdig","name":"2001:41d0:1:4874:0:0:0:1"}')
    assert(isinstance(result.responses[0].abuf.answers[0], AaaaAnswer))
    assert(result.responses[0].abuf.answers[0].address == "2001:41d0:1:4874:0:0:0:1")
    assert(result.responses[0].abuf.answers[0].name == "postmaster.fr.")
    assert(result.responses[0].abuf.answers[0].ttl == 300)
    assert(result.responses[0].abuf.answers[0].type == "AAAA")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 16)


def test_cnameanswer():
    result = Result.get('{"from":"2001:410:90ff:0:a2f3:c1ff:fec4:4a01","msm_id":1687656,"timestamp":1403101065,"fw":4610,"proto":"UDP","af":6,"msm_name":"Tdig","prb_id":13330,"result":{"abuf":"n9mEAAABAAIABgACBHR0MDEEcmlwZQNuZXQAAAEAAcAMAAUAAQAAVGAABgNudHDAEcArAAEAAQAAVGAABMEAAOXAEQACAAEAAA4QABAGc25zLXBiA2lzYwNvcmcAwBEAAgABAAAOEAAMA25zMwNuaWMCZnIAwBEAAgABAAAOEAANBHNlYzEFYXBuaWPAFsARAAIAAQAADhAADgZ0aW5uaWUEYXJpbsAWwBEAAgABAAAOEAAHBHNlYzPAhsARAAIAAQAADhAADgNwcmkHYXV0aGRuc8ARwMcAAQABAAAOEAAEwQAJBcDHABwAAQAADhAAECABBnwA4AAAAAAAAAAAAAU=","rt":84.262,"NSCOUNT":6,"QDCOUNT":1,"ID":40921,"ARCOUNT":2,"ANCOUNT":2,"size":257},"result-rt":84.262,"src_addr":"2001:410:90ff:0:a2f3:c1ff:fec4:4a01","group_id":1687656,"type":"dns","dst_addr":"2001:67c:e0::5"}')
    assert(isinstance(result.responses[0].abuf.answers[0], CnameAnswer))
    assert(result.responses[0].abuf.answers[0].name == "tt01.ripe.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 21600)
    assert(result.responses[0].abuf.answers[0].type == "CNAME")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 6)
    assert(result.responses[0].abuf.answers[0].target == "ntp.ripe.net.")


def test_dnskeyanswer():
    result = Result.get('{"af":6,"dst_addr":"2001:500:40::1","from":"2605:e000:160f:4097:6666:b3ff:feb0:cd7c","fw":4610,"group_id":1672218,"msm_id":1672220,"msm_name":"Tdig","prb_id":15060,"proto":"TCP","result":{"ANCOUNT":7,"ARCOUNT":1,"ID":57207,"NSCOUNT":0,"QDCOUNT":1,"abuf":"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","rt":62.748,"size":1625},"result-rt":62.748,"src_addr":"2605:e000:160f:4097:6666:b3ff:feb0:cd7c","timestamp":1402768690,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], DnskeyAnswer))
    assert(result.responses[0].abuf.answers[0].flags == 256)
    assert(result.responses[0].abuf.answers[0].algorithm == 7)
    assert(result.responses[0].abuf.answers[0].protocol == 3)
    assert(result.responses[0].abuf.answers[0].key == "AwEAAX7wnIyA9rd+WWcUxE6ILCCtZWvJ9aVgG7wiNYbbQp6tPn5gTmZxR35tV2WK0bHordMGJrlTuH3u8rqBYxOM/LWHj6OAGtsE8RQQhcJCzOGpQADJggSAoSNhoJ/qiXAT6wcwPrwmVnUFLV8Sok/kEbRKnXuSqIPfSVj+j9VodpFH")
    assert(result.responses[0].abuf.answers[0].name == "org.")
    assert(result.responses[0].abuf.answers[0].ttl == 900)
    assert(result.responses[0].abuf.answers[0].type == "DNSKEY")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 136)


def test_dsanswer():
    result = Result.get('{"from":"2607:f0b0:e:1000:6666:b3ff:fec5:21e","msm_id":1687655,"timestamp":1403100350,"fw":4610,"proto":"UDP","af":6,"msm_name":"Tdig","prb_id":17460,"result":{"abuf":"I4SEAAABAAEAAAAAB3RlY2hpbmMCbmwAACsAAcAMACsAAQAAHCAAJB+nBwJJII0cWAXwOgMwXauyVu24mdSr2nOQuqNwJtBOj\/Kqfw==","rt":99.33,"NSCOUNT":0,"QDCOUNT":1,"ID":9092,"ARCOUNT":0,"ANCOUNT":1,"size":76},"result-rt":99.33,"src_addr":"2607:f0b0:e:1000:6666:b3ff:fec5:21e","group_id":1687655,"type":"dns","dst_addr":"2001:7b8:606::85"}')
    assert(isinstance(result.responses[0].abuf.answers[0], DsAnswer))
    assert(result.responses[0].abuf.answers[0].name == "techinc.nl.")
    assert(result.responses[0].abuf.answers[0].ttl == 7200)
    assert(result.responses[0].abuf.answers[0].type == "DS")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 36)
    assert(result.responses[0].abuf.answers[0].tag == 8103)
    assert(result.responses[0].abuf.answers[0].algorithm == 7)
    assert(result.responses[0].abuf.answers[0].digest_type == 2)
    assert(result.responses[0].abuf.answers[0].delegation_key == "49208d1c5805f03a03305dabb256edb899d4abda7390baa37026d04e8ff2aa7f")


def test_hinfoanswer():
    result = Result.get('{"af":4,"dst_addr":"192.31.231.42","from":"78.27.190.13","fw":4720,"group_id":2815158,"lts":23,"msm_id":2815158,"msm_name":"Tdig","prb_id":12534,"proto":"UDP","result":{"ANCOUNT":4,"ARCOUNT":5,"ID":24754,"NSCOUNT":4,"QDCOUNT":1,"abuf":"YLKEAAABAAQABAAFBHN0YXICY3MCdnUCbmwAAP8AAcAMAA0AAQABUYAACQNTdW4EVW5peMAMAA8AAQABUYAACwKaBnplcGh5csARwAwADwABAAFRgAAEAAHADMAMAAEAAQABUYAABMAf5yrAEQACAAEAAVGAAAYDdG9wwBHAEQACAAEAAVGAAAcEc29sb8ARwBEAAgABAAFRgAACwAzAEQACAAEAAVGAAAUCbnPAFMAMAAEAAQABUYAABMAf5yrAQgABAAEAAVGAAASCJRQKwKoAAQABAAFRgAAEgiWBBMB3AAEAAQABUYAABIIlFATAiQABAAEAAVGAAASCJRQF","rt":38.079,"size":255},"src_addr":"192.168.1.131","timestamp":1444999225,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], HinfoAnswer))
    assert(result.responses[0].abuf.answers[0].name == "star.cs.vu.nl.")
    assert(result.responses[0].abuf.answers[0].ttl == 86400)
    assert(result.responses[0].abuf.answers[0].type == "HINFO")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 9)
    assert(result.responses[0].abuf.answers[0].cpu == "Sun")
    assert(result.responses[0].abuf.answers[0].os == "Unix")


def test_mxanswer():
    result = Result.get('{"from":"2607:fcc0:3:2:220:4aff:fee0:219e","msm_id":1687652,"fw":4610,"timestamp":1403098937,"resultset":[{"src_addr":"208.70.247.155","proto":"UDP","submax":3,"af":4,"subid":1,"result":{"abuf":"KESBgAABAAIAAAAABHJpcGUDbmV0AAAPAAHADAAPAAEAAAEsAAkAyARrb2tvwAzADAAPAAEAAAEsAAkA+gRrYWthwAw=","rt":198.454,"NSCOUNT":0,"QDCOUNT":1,"ID":10308,"ARCOUNT":0,"ANCOUNT":2,"size":68},"time":1403098937,"dst_addr":"208.70.244.7"},{"src_addr":"208.70.247.155","proto":"UDP","submax":3,"af":4,"subid":2,"result":{"abuf":"emqBgAABAAIAAAAABHJpcGUDbmV0AAAPAAHADAAPAAEAAAEsAAkAyARrb2tvwAzADAAPAAEAAAEsAAkA+gRrYWthwAw=","rt":127.644,"NSCOUNT":0,"QDCOUNT":1,"ID":31338,"ARCOUNT":0,"ANCOUNT":2,"size":68},"time":1403098938,"dst_addr":"208.70.245.7"},{"src_addr":"2607:fcc0:3:2:220:4aff:fee0:219e","proto":"UDP","submax":3,"af":6,"subid":3,"time":1403098939,"error":{"timeout":5000},"dst_addr":"2001:4860:4860::8888"}],"prb_id":2793,"group_id":1687652,"type":"dns","msm_name":"Tdig"}')
    assert(isinstance(result.responses[0].abuf.answers[0], MxAnswer))
    assert(result.responses[0].abuf.answers[0].preference == 200)
    assert(result.responses[0].abuf.answers[0].mail_exchanger == "koko.ripe.net.")
    assert(result.responses[0].abuf.answers[0].name == "ripe.net.")
    assert(result.responses[0].abuf.answers[0].ttl == 300)
    assert(result.responses[0].abuf.answers[0].type == "MX")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 9)


def test_nsanswer():
    result = Result.get('{"from":"85.69.130.41","msm_id":1687666,"fw":4610,"timestamp":1403103973,"resultset":[{"src_addr":"10.0.50.116","proto":"UDP","submax":2,"af":4,"subid":1,"result":{"abuf":"sPKBgAABAAIAAAACCGpvaG5ib25kA29yZwAAAgABwAwAAgABAAAOEAAMA25zMQJoZQNuZXQAwAwAAgABAAAOEAAFAm5zwAzAQgABAAEAAVF\/AAS5IgCVwCoAAQABAABlRgAE2NqCAg==","rt":1688.621,"NSCOUNT":0,"QDCOUNT":1,"ID":45298,"ARCOUNT":2,"ANCOUNT":2,"size":103},"time":1403103973,"dst_addr":"10.0.0.34"},{"src_addr":"10.0.50.116","proto":"UDP","submax":2,"af":4,"subid":2,"result":{"abuf":"VkGBgAABAAIAAAACCGpvaG5ib25kA29yZwAAAgABwAwAAgABAAAOEAAFAm5zwAzADAACAAEAAA4QAAwDbnMxAmhlA25ldADAKgABAAEAAVGAAAS5IgCVwDsAAQABAAKjAAAE2NqCAg==","rt":932.26,"NSCOUNT":0,"QDCOUNT":1,"ID":22081,"ARCOUNT":2,"ANCOUNT":2,"size":103},"time":1403103976,"dst_addr":"10.0.0.35"}],"prb_id":17868,"group_id":1687666,"type":"dns","msm_name":"Tdig"}')
    assert(isinstance(result.responses[0].abuf.answers[0], NsAnswer))
    assert(result.responses[0].abuf.answers[0].name == "johnbond.org.")
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].type == "NS")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 12)
    assert(result.responses[0].abuf.answers[0].target == "ns1.he.net.")


def test_nsecanswer():
    result = Result.get('{"af":6,"dst_addr":"2001:7fd::1","from":"2a02:1810:3505:de00:a2f3:c1ff:fec4:5ba8","fw":4720,"group_id":2815340,"lts":8,"msm_id":2815340,"msm_name":"Tdig","prb_id":11939,"proto":"UDP","result":{"ANCOUNT":0,"ARCOUNT":1,"ID":62350,"NSCOUNT":4,"QDCOUNT":1,"abuf":"846GAwABAAAABAABCGFhcmR2YXJrAAABAAEDYWFhAAAvAAEAAVGAAA0DYWJiAAAGIAAAAAATwBoALgABAAFRgACTAC8IAQABUYBWLbNQViB2QPRCAC/+fyqSx+gLHZaTO357C33yMzG6vpgWV0neGCUWr1i9g2a0Nc9w4o739PXvpDBQfkDmS6x4msfjU1lQv47U/9jMf7mOrWvlhKXZQ8ZPphqbNfa31h1pCNHu/NzBRLTdWJfMBMWuVbVJLdD/lEi/LW8G61fPbyFZfoM/crsfAkG6AAAvAAEAAVGAAA4DYWFhAAAHIgAAAAADgAAALgABAAFRgACTAC8IAAABUYBWLbNQViB2QPRCAJe1XkAFWiDj0V50PxlG3qSVux6rLfquyrII9HA2VMCLDeetkEgdtW+N7FWoh1Rampi7rho7R32O7HIk561bzdtP5lEA415RXus4Hf8BCXKgRtRoNJsFNAbkPKnbtRzNJAFDbP0mLfC08wSi0zsWRYDxaBLwh9ru/lJjOOR82UFhAAApEAAAAIAAAAA=","rt":18.193,"size":407},"src_addr":"2a02:1810:3505:de00:a2f3:c1ff:fec4:5ba8","timestamp":1445001458,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.authorities[0], NsecAnswer))
    assert(result.responses[0].abuf.authorities[0].name == "aaa.")
    assert(result.responses[0].abuf.authorities[0].ttl == 86400)
    assert(result.responses[0].abuf.authorities[0].type == "NSEC")
    assert(result.responses[0].abuf.authorities[0].klass == "IN")
    assert(result.responses[0].abuf.authorities[0].rd_length == 13)
    assert(result.responses[0].abuf.authorities[0].next_domain_name == "abb.")
    assert(result.responses[0].abuf.authorities[0].types == [2, 43, 46, 47])


def test_nsec3answer():
    result = Result.get('{"af":6,"dst_addr":"2a04:b900::1:0:0:12","from":"2a02:aa8:0:2000::10","fw":4700,"group_id":2815716,"lts":25,"msm_id":2815716,"msm_name":"Tdig","prb_id":11602,"proto":"UDP","result":{"ANCOUNT":0,"ARCOUNT":1,"ID":43793,"NSCOUNT":8,"QDCOUNT":1,"abuf":"qxGEAwABAAAACAABCGFhcmR2YXJrBW5sbmV0Am5sAAABAAEganVsaGZmZm1ycnNrdWF2czZicjhmZW01djdkbzU4cTnAFQAyAAEAAEZQABoBAAABABSnxvPOSUe3yFdR1MH6YM87p7jtScAjAC4AAQAARlAAnAAyCAMAAEZQVkPiQVYe+EGYQwVubG5ldAJubACUzkwAhnwSePZ0EfeLqkc6iLP34HvDeGfgARozzdM3zLCJQFF4HNlifFCQR0x6ARyOx37ooBSlLGnbjnVPqSOxGvcZQ2/KXG6sKWVA7bC33okqLFuGXMIKNJra3HNnL9MTfvDOWT2zRpVHindoOcnvu708v7NpWSVchSgbg0kbhCBqYzFoMm1xZWNoOWttZ3MxdTI0bXBwNnM3MmE0YXBic8AVADIAAQAARlAAKQEAAAEAFJtOBqRGL60wKTOd/wJyipXJrPeGAA1iAYAIEAKQAAAAAAAQwRIALgABAABGUACcADIIAwAARlBWQ+JBVh74QZhDBW5sbmV0Am5sAH3nu47gh7pKKCm8CoIg7AxN/0OAXubN2oGyLE01aSsD9umicDjznilyptXzUDG7AStkQirudpV8jdJ5WmK024r1ie5thINv0RGvkTW6excf5gBeDbVCAEOlR0PESprWFfgisosvpGFz4QxGa/uXwTniJhZAicnWl3UVNu41NdIuIDZmbDFyY21vcWR0OG1nNXRwOTNwMWpxcGFlbW9pZTJrwBUAMgABAABGUAAiAQAAAQAUNxopag2Cp74L6/fYTv+/0iKL8H4ABgQAAAAAAsIQAC4AAQAARlAAnAAyCAMAAEZQVkPiQVYe+EGYQwVubG5ldAJubAAALouKU48w+kGrY6rp8atTgoocvdJysokaZsB3GOMf4tic6tuRMMWbVb9AJaiK8mn0MzAktZCN6FEY319mzB7P0fkqyHCaXOG4jnFcSj18vGm9mqIMZMoSwAHkD8djaWwHHWmoYCQ/vxBPYcspOk51d1zz0BhmIrd/rkbS2mKCdMAVAAYAAQAARlAANQJucwlubG5ldGxhYnPAGwpob3N0bWFzdGVyBG9wZW7AFXgcAjwAAHCAAAAcIAAJOoAAAEZQwBUALgABAABGUACcAAYIAgABUYBWQ+JBVh74QZhDBW5sbmV0Am5sAKPDfqXXDY0bZrsihjWsTd2XLPMpT3djq2FnqhKixso9poQJ1DNYN+u2BejNUAwWPX0xcD3itTwVCeGDTblQv5JpLUmIs0KESuC0fyy4sSJ32QwOGvh0p1g6eDXY/hKu+j7Z6isrhyMFJsyRgwFDWcvYqSeS6PSIMvdTb3vioHtKAAApEAAAAIAAAAA=","rt":37.356,"size":1019},"src_addr":"2a02:aa8:0:2000::10","timestamp":1445006271,"type":"dns"}')
    print(result.responses[0].abuf.authorities[2].flags)
    assert(isinstance(result.responses[0].abuf.authorities[2], Nsec3Answer))
    assert(result.responses[0].abuf.authorities[2].name == "jc1h2mqech9kmgs1u24mpp6s72a4apbs.nlnet.nl.")
    assert(result.responses[0].abuf.authorities[2].ttl == 18000)
    assert(result.responses[0].abuf.authorities[2].type == "NSEC3")
    assert(result.responses[0].abuf.authorities[2].klass == "IN")
    assert(result.responses[0].abuf.authorities[2].rd_length == 41)
    assert(result.responses[0].abuf.authorities[2].hash_algorithm == 1)
    assert(result.responses[0].abuf.authorities[2].flags == 0)
    assert(result.responses[0].abuf.authorities[2].iterations == 1)
    assert(result.responses[0].abuf.authorities[2].salt == "")
    assert(result.responses[0].abuf.authorities[2].hash == "jd70d9265umj0a9jjnvg4skain4qpts6")
    assert(result.responses[0].abuf.authorities[2].types == [1, 2, 6, 15, 16, 28, 35, 46, 48, 51, 99])


def test_nsec3paramanswer():
    result = Result.get('{"af":4,"dst_addr":"185.49.140.12","from":"78.27.190.13","fw":4720,"group_id":2816176,"lts":14,"msm_id":2816176,"msm_name":"Tdig","prb_id":12534,"proto":"UDP","result":{"ANCOUNT":24,"ARCOUNT":1,"ID":22156,"NSCOUNT":0,"QDCOUNT":1,"abuf":"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","answers":[{"MNAME":"ns.nlnetlabs.nl.","NAME":"nlnet.nl.","RNAME":"hostmaster.open.nlnet.nl.","SERIAL":2015101500,"TTL":86400,"TYPE":"SOA"}],"rt":39.686,"size":2770},"src_addr":"192.168.1.131","timestamp":1445010704,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[20], Nsec3ParamAnswer))
    assert(result.responses[0].abuf.answers[20].name == 'nlnet.nl.')
    assert(result.responses[0].abuf.answers[20].ttl == 3600)
    assert(result.responses[0].abuf.answers[20].type == "NSEC3PARAM")
    assert(result.responses[0].abuf.answers[20].klass == "IN")
    assert(result.responses[0].abuf.answers[20].rd_length == 5)
    assert(result.responses[0].abuf.answers[20].algorithm == 1)
    assert(result.responses[0].abuf.answers[20].flags == 0)
    assert(result.responses[0].abuf.answers[20].iterations == 1)
    assert(result.responses[0].abuf.answers[20].salt == '')


def test_ptranswer():
    result = Result.get('{"af":6,"dst_addr":"2001:888:1044:10:2a0:c9ff:fe9f:17a9","from":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","fw":4700,"group_id":2827383,"lts":14,"msm_id":2827383,"msm_name":"Tdig","prb_id":12750,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":52292,"NSCOUNT":1,"QDCOUNT":1,"abuf":"zESEAAABAAEAAQAAATkBQQE3ATEBRgE5AUUBRgFGAUYBOQFDATABQQEyATABMAExATABMAE0ATQBMAExATgBOAE4ATABMQEwATABMgNpcDYEYXJwYQAADAABATkBYQE3ATEBZgE5AWUBZgFmAWYBOQFjATABYQEyATABMAExATABMAE0ATQBMAExATgBOAE4ATABMQEwATABMgNpcDYEYXJwYQAADAABAAAOEAAXB3N0ZXJlbzYCaHEGcGhpY29oA25ldADAggACAAEAAA4QAAYDbnMzwLk=","rt":34.676,"size":215},"src_addr":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","timestamp":1445246958,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], PtrAnswer))
    assert(result.responses[0].abuf.answers[0].name == '9.a.7.1.f.9.e.f.f.f.9.c.0.a.2.0.0.1.0.0.4.4.0.1.8.8.8.0.1.0.0.2.ip6.arpa.')
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].type == "PTR")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 23)
    assert(result.responses[0].abuf.answers[0].target == 'stereo6.hq.phicoh.net.')


def test_rrsiganswer():
    result = Result.get('{"af":4,"dst_addr":"193.0.9.5","from":"188.134.80.2","fw":4670,"group_id":1863527,"lts":164,"msm_id":1863527,"msm_name":"Tdig","prb_id":10221,"proto":"UDP","result":{"ANCOUNT":2,"ARCOUNT":1,"ID":43644,"NSCOUNT":0,"QDCOUNT":1,"abuf":"qnyEAAABAAIAAAABA3d3dwRyaXBlA25ldAAAAQABwAwAAQABAABUYAAEwQAGi8AMAC4AAQAAVGAAnAABBQMAAFRgVQF0I1TZ2RP39gRyaXBlA25ldAAKTSpMfJr47JtCHrIXQlklDB4CoLtux0tTGbfOUYCL1XBcbCU9mRj9WHd52gkyDqPYT6IFF6i56xYAxidn1/9o2Ou+X2PGTt0L/Fb+Ht1CN3exboitJq2FnIC1jKUcJIWF3VcLg5AwLkOklifPJqAeeHL98BOZ4IdNC/jDSNHbRAAAKRAAAACAAAAA","rt":15.705,"size":225},"src_addr":"10.250.10.104","timestamp":1423566533,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[1], RRSigAnswer))
    assert(result.responses[0].abuf.answers[1].type_covered == 'A')
    assert(result.responses[0].abuf.answers[1].algorithm == 5)
    assert(result.responses[0].abuf.answers[1].labels == 3)
    assert(result.responses[0].abuf.answers[1].original_ttl == 21600)
    assert(result.responses[0].abuf.answers[1].signature_expiration == 1426158627)
    assert(result.responses[0].abuf.answers[1].signature_inception == 1423563027)
    assert(result.responses[0].abuf.answers[1].key_tag == 63478)
    assert(result.responses[0].abuf.answers[1].signer_name == 'ripe.net.')
    assert(result.responses[0].abuf.answers[1].signature == 'Ck0qTHya+OybQh6yF0JZJQweAqC7bsdLUxm3zlGAi9VwXGwlPZkY/Vh3edoJMg6j2E+iBReouesWAMYnZ9f/aNjrvl9jxk7dC/xW/h7dQjd3sW6IrSathZyAtYylHCSFhd1XC4OQMC5DpJYnzyagHnhy/fATmeCHTQv4w0jR20Q=')


def test_soaanswer():
    result = Result.get('{"af":6,"dst_addr":"2001:dcd:7::1","from":"2a03:b280::280:a3ff:fe91:3bb2","fw":4610,"group_id":1674999,"msm_id":1675002,"msm_name":"Tdig","name":"2001:dcd:7:0:0:0:0:1","prb_id":3498,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":1,"ID":53767,"NSCOUNT":0,"QDCOUNT":1,"abuf":"0geEAAABAAEAAAABCHRlc3R6b25lAAAGAAHADAAGAAEAAAOEAEYDYXJpBWFscGhhBmFyaWRucwNuZXQCYXUAB3N1cHBvcnQLYXJpc2VydmljZXMDY29tAFOhbEUAAAcIAAABLAAbr4AAAAcIAAApEAAAAAAAAAwAAwAIZG5zMi5hbXM=","answers":[{"MNAME":"ari.alpha.aridns.net.au.","NAME":"testzone.","RNAME":"support.ariservices.com.","SERIAL":1403087941,"TTL":900,"TYPE":"SOA"}],"rt":21.566,"size":131},"result-rdata":null,"result-rname":"support.ariservices.com.","result-rt":21.566,"result-serial":1403087941,"src_addr":"2a03:b280::280:a3ff:fe91:3bb2","timestamp":1403087945,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], SoaAnswer))
    assert(result.responses[0].abuf.answers[0].retry == 300)
    assert(result.responses[0].abuf.answers[0].name == 'testzone.')
    assert(result.responses[0].abuf.answers[0].minimum == 1800)
    assert(result.responses[0].abuf.answers[0].refresh == 1800)
    assert(result.responses[0].abuf.answers[0].mname == "ari.alpha.aridns.net.au.")
    assert(result.responses[0].abuf.answers[0].expire == 1814400)
    assert(result.responses[0].abuf.answers[0].rname == "support.ariservices.com.")
    assert(result.responses[0].abuf.answers[0].ttl == 900)
    assert(result.responses[0].abuf.answers[0].serial == 1403087941)
    assert(result.responses[0].abuf.answers[0].type == "SOA")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 70)


def test_srvanswer():
    result = Result.get('{"af":4,"dst_addr":"5.9.91.110","from":"213.169.87.0","fw":4720,"group_id":2827808,"lts":2,"msm_id":2827808,"msm_name":"Tdig","prb_id":11712,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":2,"ID":50101,"NSCOUNT":5,"QDCOUNT":1,"abuf":"w7WEAAABAAEABQACDF94bXBwLXNlcnZlcgRfdGNwCmJ1ZGR5Y2xvdWQDY29tAAAhAAHADAAhAAEAAAEsABsABQAAFJUEeG1wcApidWRkeWNsb3VkA2NvbQDASQACAAEAAAEsAAwDbnMyAmhlA25ldADASQACAAEAAAEsAAYDbnMzwGnASQACAAEAAAEsAAYDbnMxwEnASQACAAEAAAEsAAYDbnM0wGnASQACAAEAAAEsAAYDbnM1wGnARAABAAEAAAEsAAQFCVtuwI8AAQABAAABLAAEBQlbbg==","rt":39.476,"size":217},"src_addr":"192.168.1.145","timestamp":1445257644,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], SrvAnswer))
    assert(result.responses[0].abuf.answers[0].name == '_xmpp-server._tcp.buddycloud.com.')
    assert(result.responses[0].abuf.answers[0].ttl == 300)
    assert(result.responses[0].abuf.answers[0].type == "SRV")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 27)
    assert(result.responses[0].abuf.answers[0].priority == 5)
    assert(result.responses[0].abuf.answers[0].weight == 0)
    assert(result.responses[0].abuf.answers[0].port == 5269)
    assert(result.responses[0].abuf.answers[0].target == 'xmpp.buddycloud.com.')


def test_sshfpanswer():
    result = Result.get('{"af":6,"dst_addr":"2001:67c:e0::5","from":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","fw":4700,"group_id":2828051,"lts":80,"msm_id":2828051,"msm_name":"Tdig","prb_id":12750,"proto":"UDP","result":{"ANCOUNT":5,"ARCOUNT":0,"ID":13066,"NSCOUNT":0,"QDCOUNT":1,"abuf":"MwqGAAABAAUAAAAABWJhbmtzBWF0bGFzBHJpcGUDbmV0AAD/AAHADAAcAAEAAFRgABAgAQZ8AugAEQAAAADBABMxwAwAAQABAABUYAAEwQATMcAMACwAAQAAVGAAFgEBXRM9wY0Cr3JqHks1Pm8TwyElyCDADAAsAAEAAFRgABYCAT5GQt0IOKjrSbJhxNhi9/IcKKtNwAwALwABAAABLAAjBGlwdjQFYmFua3MFYXRsYXMEcmlwZQNuZXQAAAZAAAAIAAs=","rt":17.846,"size":197},"src_addr":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","timestamp":1445260363,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[2], SshfpAnswer))
    assert(result.responses[0].abuf.answers[2].name == 'banks.atlas.ripe.net.')
    assert(result.responses[0].abuf.answers[2].ttl == 21600)
    assert(result.responses[0].abuf.answers[2].type == "SSHFP")
    assert(result.responses[0].abuf.answers[2].klass == "IN")
    assert(result.responses[0].abuf.answers[2].rd_length == 22)
    assert(result.responses[0].abuf.answers[2].algorithm == 1)
    assert(result.responses[0].abuf.answers[2].digest_type == 1)
    assert(result.responses[0].abuf.answers[2].fingerprint == '5d133dc18d02af726a1e4b353e6f13c32125c820')


def test_tlsaanswer():
    result = Result.get('{"af":6,"dst_addr":"2001:67c:e0::5","from":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","fw":4700,"group_id":2828271,"lts":79,"msm_id":2828271,"msm_name":"Tdig","prb_id":12750,"proto":"UDP","result":{"ANCOUNT":4,"ARCOUNT":0,"ID":36436,"NSCOUNT":1,"QDCOUNT":1,"abuf":"jlSGAAABAAQAAQAABF80NDMEX3RjcAVhdGxhcwRyaXBlA25ldAAA/wABwAwANAABAAABLAAjAQAByKo6/qz2tjWS9PH44aqDIVYC/qQykybwJ4xFm54/I+nADAAvAAEAAAEsAB8FYWRtaW4FYXRsYXMEcmlwZQNuZXQAAAcAAAAAAAMIwAwALgABAAABLACcADQFBQAAASxWTEzQViSxwPQ+BHJpcGUDbmV0AG0lz8nbHKhBeKmPGKWAJ3oeQGRQpXbD9sKH2Hv/zrU5T2uXzufSq9ZsKJwx28x28mI5zbLgDoyCAiHlctdDNJLfPMpaHpZ/fw9095jnOvj9+iYAg6YiL1V/Pv5tSRbNvwHV1vIH7lb6YMASOBeifP4B/tszDDNKN6YzD+0ib+n5wAwALgABAAABLACcAC8FBQAAASxWTEzQViSxwPQ+BHJpcGUDbmV0AFOfKo+nqvdicU0rEmuXLJcQoHlNoxmnkWATtxT+AN6X2+Fd4RLQLRiqUXwj8cOE6VHfgeG/KHT9sETwKvrzKFS3wxO16Vd0ATqhIBshGtgb73WVFADrL2TKVSMxaHuXul6sWATeP5L4E4FFI9wW+RsxFB9kuFFeXOVVHH59B5OhwUoAAgABAAAOEAAOBnRpbm5pZQRhcmluwU8=","rt":17.932,"size":494},"src_addr":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","timestamp":1445263153,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], TlsaAnswer))
    assert(result.responses[0].abuf.answers[0].name == '_443._tcp.atlas.ripe.net.')
    assert(result.responses[0].abuf.answers[0].ttl == 300)
    assert(result.responses[0].abuf.answers[0].type == "TLSA")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 35)
    assert(result.responses[0].abuf.answers[0].certificate_usage == 1)
    assert(result.responses[0].abuf.answers[0].selector == 0)
    assert(result.responses[0].abuf.answers[0].matching_type == 1)
    assert(result.responses[0].abuf.answers[0].certificate_associated_data == 'c8aa3afeacf6b63592f4f1f8e1aa83215602fea4329326f0278c459b9e3f23e9')


def test_txtanswer():
    result = Result.get('{"af":4,"dst_addr":"185.49.140.12","from":"78.27.190.13","fw":4720,"group_id":2816176,"lts":14,"msm_id":2816176,"msm_name":"Tdig","prb_id":12534,"proto":"UDP","result":{"ANCOUNT":24,"ARCOUNT":1,"ID":22156,"NSCOUNT":0,"QDCOUNT":1,"abuf":"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","answers":[{"MNAME":"ns.nlnetlabs.nl.","NAME":"nlnet.nl.","RNAME":"hostmaster.open.nlnet.nl.","SERIAL":2015101500,"TTL":86400,"TYPE":"SOA"}],"rt":39.686,"size":2770},"src_addr":"192.168.1.131","timestamp":1445010704,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[10], TxtAnswer))
    assert(result.responses[0].abuf.answers[10].name == 'nlnet.nl.')
    assert(result.responses[0].abuf.answers[10].ttl == 86400)
    assert(result.responses[0].abuf.answers[10].type == "TXT")
    assert(result.responses[0].abuf.answers[10].klass == "IN")
    assert(result.responses[0].abuf.answers[10].rd_length == 16)
    assert(result.responses[0].abuf.answers[10].data == ['Stichting NLnet'])


def test_unknownanswer():
    result = Result.get('{"af":6,"dst_addr":"2001:888:1044:10:2a0:c9ff:fe9f:17a9","from":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","fw":4700,"group_id":2828518,"lts":17,"msm_id":2828518,"msm_name":"Tdig","prb_id":12750,"proto":"UDP","result":{"ANCOUNT":1,"ARCOUNT":0,"ID":5025,"NSCOUNT":0,"QDCOUNT":1,"abuf":"E6GGAAABAAEAAAAADHVua25vd24tdHlwZQRhaW95AmV1AAD/AAEMdW5rbm93bi10eXBlBGFpb3kCZXUA/wAAAQAADhAADEhlbGxvIFdvcmxkIQ==","rt":34.265,"size":82},"src_addr":"2001:920:6801:11:a2f3:c1ff:fec4:3fe7","timestamp":1445266555,"type":"dns"}')
    assert(isinstance(result.responses[0].abuf.answers[0], Answer))
    assert(result.responses[0].abuf.answers[0].name == 'unknown-type.aioy.eu.')
    assert(result.responses[0].abuf.answers[0].ttl == 3600)
    assert(result.responses[0].abuf.answers[0].type == "65280")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 12)
    assert(result.responses[0].abuf.answers[0].rdata == '48656c6c6f20576f726c6421')


def test_dns_lts():
    result = Result.get('{"lts":161,"from":"46.17.16.18","msm_id":1004041,"timestamp":1406560725,"fw":4650,"proto":"UDP","af":4,"msm_name":"Tdig","prb_id":778,"result":{"abuf":"vb2EAAABAAEAAAAABWFzMjUwA25ldAAAAQABwAwAAQABAAAOEAAEwpaooA==","rt":36.661,"NSCOUNT":0,"QDCOUNT":1,"ID":48573,"ARCOUNT":0,"ANCOUNT":1,"size":43},"result-rt":36.661,"src_addr":"192.168.1.12","type":"dns","dst_addr":"193.227.234.53"}')
    assert(result.seconds_since_sync == 161)


def test_txt_with_class_in():
    result = Result.get('{"msm_id": 10209, "fw": 4660, "timestamp": 1413417973, "prb_id": 4232, "result": {"abuf": "nfCAgAABAAEAAAAAB3ZlcnNpb24EYmluZAAAEAADwAwAEAABAAAfMAAdHFBvd2VyRE5TIFJlY3Vyc29yIDMuNS4yICRJZCQ=", "rt": 298.828, "size": 71, "ARCOUNT": 0, "NSCOUNT": 0, "QDCOUNT": 1, "ANCOUNT": 1, "answers": [{"TYPE": "TXT", "NAME": "version.bind", "RDATA": "PowerDNS Recursor 3.5.2 $Id$"}], "ID": 40432}, "src_addr": "10.0.3.6", "msm_name": "Tdig", "lts": 71, "from": "89.179.73.12", "proto": "UDP", "af": 4, "type": "dns", "dst_addr": "198.41.0.4"}')
    print(result.responses[0].abuf.answers[0].raw_data)
    assert(result.responses[0].abuf.answers[0].name == "version.bind.")
    assert(result.responses[0].abuf.answers[0].klass == "IN")
    assert(result.responses[0].abuf.answers[0].rd_length == 29)
    assert(result.responses[0].abuf.answers[0].type == "TXT")
    assert(result.responses[0].abuf.answers[0].ttl == 7984)
    assert(len(result.responses[0].abuf.answers[0].data) == 1)
    assert(result.responses[0].abuf.answers[0].data[0] == "PowerDNS Recursor 3.5.2 $Id$")


def test_unparsed_abuf():
    result = Result.get('{"msm_id": 10209, "fw": 4660, "timestamp": 1413417973, "prb_id": 4232, "result": {"abuf": "nfCAgAABAAEAAAAAB3ZlcnNpb24EYmluZAAAEAADwAwAEAABAAAfMAAdHFBvd2VyRE5TIFJlY3Vyc29yIDMuNS4yICRJZCQ=", "rt": 298.828, "size": 71, "ARCOUNT": 0, "NSCOUNT": 0, "QDCOUNT": 1, "ANCOUNT": 1, "answers": [{"TYPE": "TXT", "NAME": "version.bind", "RDATA": "PowerDNS Recursor 3.5.2 $Id$"}], "ID": 40432}, "src_addr": "10.0.3.6", "msm_name": "Tdig", "lts": 71, "from": "89.179.73.12", "proto": "UDP", "af": 4, "type": "dns", "dst_addr": "198.41.0.4"}', parse_buf=False)
    assert(result.responses[0].abuf.answers[0].name == "version.bind")
    assert(result.responses[0].abuf.answers[0].klass is None)
    assert(result.responses[0].abuf.answers[0].rd_length is None)
    assert(result.responses[0].abuf.answers[0].type == "TXT")
    assert(result.responses[0].abuf.answers[0].ttl is None)
    assert(len(result.responses[0].abuf.answers[0].data) == 1)
    assert(result.responses[0].abuf.answers[0].data[0] == "PowerDNS Recursor 3.5.2 $Id$")


def test_unparsed_abuf_with_txt_list():
    result = Result.get('{"msm_id": 10209, "fw": 4660, "timestamp": 1413417973, "prb_id": 4232, "result": {"abuf": "nfCAgAABAAEAAAAAB3ZlcnNpb24EYmluZAAAEAADwAwAEAABAAAfMAAdHFBvd2VyRE5TIFJlY3Vyc29yIDMuNS4yICRJZCQ=", "rt": 298.828, "size": 71, "ARCOUNT": 0, "NSCOUNT": 0, "QDCOUNT": 1, "ANCOUNT": 1, "answers": [{"TYPE": "TXT", "NAME": "version.bind", "RDATA": ["PowerDNS Recursor 3.5.2 $Id$"]}], "ID": 40432}, "src_addr": "10.0.3.6", "msm_name": "Tdig", "lts": 71, "from": "89.179.73.12", "proto": "UDP", "af": 4, "type": "dns", "dst_addr": "198.41.0.4"}', parse_buf=False)
    assert(result.responses[0].abuf.answers[0].name == "version.bind")
    assert(result.responses[0].abuf.answers[0].klass is None)
    assert(result.responses[0].abuf.answers[0].rd_length is None)
    assert(result.responses[0].abuf.answers[0].type == "TXT")
    assert(result.responses[0].abuf.answers[0].ttl is None)
    assert(len(result.responses[0].abuf.answers[0].data) == 1)
    assert(result.responses[0].abuf.answers[0].data[0] == "PowerDNS Recursor 3.5.2 $Id$")


def test_flags():
    result = Result.get('{"from":"2001:67c:2e8:11::c100:136c","msm_id":1663540,"fw":4620,"af":6,"timestamp":1403091608,"proto":"UDP","dst_addr":"2001:41d0:1:4874::1","prb_id":6012,"result":{"abuf":"1jKEAAABAAEAAgADCnBvc3RtYXN0ZXICZnIAABwAAcAMABwAAQAAASwAECABQdAAAUh0AAAAAAAAAAHADAACAAEAAAEsAAYDbnMxwAzADAACAAEAAAEsAAYDbnMywAzARwABAAEAAAEsAARXYtl0wEcAHAABAAABLAAQIAFB0AABSHQAAAAAAAAAAcBZAAEAAQAAASwABFzzEZ8=","rt":8.656,"NSCOUNT":2,"QDCOUNT":1,"ANCOUNT":1,"ARCOUNT":3,"ID":54834,"size":155},"result-rt":8.656,"src_addr":"2001:67c:2e8:11::c100:136c","group_id":1663540,"type":"dns","msm_name":"Tdig","name":"2001:41d0:1:4874:0:0:0:1"}')
    Flags = namedtuple("Flags", ("qr", "aa", "tc", "rd", "ra", "z", "ad", "cd"))
    assert(result.responses[0].abuf.header.flags == Flags(qr=True, aa=True, tc=False, rd=False, ra=False, z=0, ad=False, cd=False))


def test_sections():
    result = Result.get('{"from":"2001:67c:2e8:11::c100:136c","msm_id":1663540,"fw":4620,"af":6,"timestamp":1403091608,"proto":"UDP","dst_addr":"2001:41d0:1:4874::1","prb_id":6012,"result":{"abuf":"1jKEAAABAAEAAgADCnBvc3RtYXN0ZXICZnIAABwAAcAMABwAAQAAASwAECABQdAAAUh0AAAAAAAAAAHADAACAAEAAAEsAAYDbnMxwAzADAACAAEAAAEsAAYDbnMywAzARwABAAEAAAEsAARXYtl0wEcAHAABAAABLAAQIAFB0AABSHQAAAAAAAAAAcBZAAEAAQAAASwABFzzEZ8=","rt":8.656,"NSCOUNT":2,"QDCOUNT":1,"ANCOUNT":1,"ARCOUNT":3,"ID":54834,"size":155},"result-rt":8.656,"src_addr":"2001:67c:2e8:11::c100:136c","group_id":1663540,"type":"dns","msm_name":"Tdig","name":"2001:41d0:1:4874:0:0:0:1"}')
    Sections = namedtuple("Sections", ("QDCOUNT", "ANCOUNT", "NSCOUNT", "ARCOUNT"))
    assert(result.responses[0].abuf.header.sections == Sections(QDCOUNT=1, ANCOUNT=1, NSCOUNT=2, ARCOUNT=3))


def test_non_ascii_in_abuf():
    result = Result.get('{"lts":136,"from":"83.163.117.153","msm_id":1020268,"fw":4670,"proto":"UDP","af":4,"msm_name":"Tdig","prb_id":96,"result":{"abuf":"sPKEAAABAAEAAQACB2RyYWdvbnMEYWlveQJldQAAEAABB2RyYWdvbnMEYWlveQJldQAAEAABAAAOEAATEkhlcmUgYmUg\/yBkcmFnb25zIcApAAIAAQAADhAABgNuczHAKcBbAAEAAQAADhAABIIlDyPAWwAcAAEAAA4QABAgAQiIEEQAEAKgyf\/+nxep","rt":33.973,"NSCOUNT":1,"QDCOUNT":1,"answers":[{"TYPE":"TXT","NAME":"dragons.aioy.eu","RDATA":"Here be \u00ff dragons!"}],"ID":45298,"ARCOUNT":2,"ANCOUNT":1,"size":141},"timestamp":1422535611,"src_addr":"10.0.1.61","group_id":1020268,"type":"dns","dst_addr":"130.37.15.35"}')
    assert(len(result.responses[0].abuf.answers) == 1)
    assert(len(result.responses[0].abuf.answers[0].data) == 1)
    assert(result.responses[0].abuf.answers[0].data[0] == "Here be \\255 dragons!")


def test_quotes_in_multiline_txt_record():
    result = Result.get('{"lts":136,"from":"83.163.117.153","msm_id":1020268,"fw":4670,"proto":"UDP","af":4,"msm_name":"Tdig","prb_id":96,"result":{"abuf":"sPKEAAABAAEAAgACB2RyYWdvbnMEYWlveQJldQAAEAABB2RyYWdvbnMEYWlveQJldQAAEAABAAAOEABPJUhlcmUgYmUg/yBkcmFnb25zISBXaXRoIFwgYW5kICIgYW5kIH8IYXMgd2VsbC4fVGhyb3dpbmcgaW4ggCBmb3IgZ29vZCBtZWFzdXJlLsApAAIAAQAADhAABgNuczHAKcApAAIAAQAADhAABgNuczLAKcCXAAEAAQAADhAABIIlDyPAqQAcAAEAAA4QABAgAQRw0WoAEAKgyf/+nxep","rt":33.973,"NSCOUNT":1,"QDCOUNT":1,"answers":[{"TYPE":"TXT","NAME":"dragons.aioy.eu","RDATA":"Here be \u00ff dragons!"}],"ID":45298,"ARCOUNT":2,"ANCOUNT":1,"size":141},"timestamp":1422535611,"src_addr":"10.0.1.61","group_id":1020268,"type":"dns","dst_addr":"130.37.15.35"}')
    assert result.responses[0].abuf.answers[0].data == [
        "Here be \\255 dragons! With \\\\ and \\\" and \\127",
        "as well.",
        "Throwing in \\128 for good measure."
    ]
    assert result.responses[0].abuf.answers[0].data_string == "Here be \\255 dragons! With \\\\ and \\\" and \\127 as well. Throwing in \\128 for good measure."


def test_string_representations():

    # A
    result = Result.get('{"lts":0,"from":"2a02:8429:80a0:7c00:ea94:f6ff:fee3:643e","msm_id":1888719,"fw":4670,"proto":"UDP","af":6,"msm_name":"Tdig","prb_id":21567,"result":{"abuf":"ldWEAAABAAEAAAAAA3d3dwZlZHV0ZWwCbmwAAAEAAcAMAAEAAQABUYAABFfpweI=","rt":22.34,"NSCOUNT":0,"QDCOUNT":1,"ID":38357,"ARCOUNT":0,"ANCOUNT":1,"size":47},"timestamp":1425632241,"src_addr":"2a02:8429:80a0:7c00:ea94:f6ff:fee3:643e","group_id":1888719,"type":"dns","dst_addr":"2a02:2170:201:1::8"}')
    assert(str(result.responses[0].abuf.answers[0]) == "www.edutel.nl.          86400    IN     A      87.233.193.226")

    # AAAA
    result = Result.get('{"from":"2a02:2b30:1:101:fa1a:67ff:fe52:eae5","msm_id":1032026,"fw":"4560","proto":"UDP","submax":1,"af":4,"dst_addr":"80.92.230.65","subid":1,"prb_id":12601,"result":{"abuf":"JZ2BgAABAAEAAQABCGJhc2VsaW5lBnJpcGU2NwlubG5ldGxhYnMCbmwAABwAAcAMABwAAQAAAB4AECoCKzAAAAEAAAAAAAAAABLAFQACAAEAABBkAAUCbnPAFcBWABwAAQAAEGQAECABB7gAQAAB0OEAAAAAAAI=","rt":69.793,"NSCOUNT":1,"QDCOUNT":1,"ID":9629,"ARCOUNT":1,"ANCOUNT":1,"size":119},"timestamp":1380927781,"src_addr":"80.92.230.185","type":"dns","msm_name":"Tdig"}')
    assert(str(result.responses[0].abuf.answers[0]) == "baseline.ripe67.nlnetlabs.nl.  30       IN     AAAA   2a02:2b30:0:100:0:0:0:12")

    # NS
    result = Result.get('{"from":"2a02:2b30:1:101:fa1a:67ff:fe52:eae5","msm_id":1032026,"fw":"4560","proto":"UDP","submax":1,"af":4,"dst_addr":"80.92.230.65","subid":1,"prb_id":12601,"result":{"abuf":"JZ2BgAABAAEAAQABCGJhc2VsaW5lBnJpcGU2NwlubG5ldGxhYnMCbmwAABwAAcAMABwAAQAAAB4AECoCKzAAAAEAAAAAAAAAABLAFQACAAEAABBkAAUCbnPAFcBWABwAAQAAEGQAECABB7gAQAAB0OEAAAAAAAI=","rt":69.793,"NSCOUNT":1,"QDCOUNT":1,"ID":9629,"ARCOUNT":1,"ANCOUNT":1,"size":119},"timestamp":1380927781,"src_addr":"80.92.230.185","type":"dns","msm_name":"Tdig"}')
    assert(str(result.responses[0].abuf.answers[0]) == "baseline.ripe67.nlnetlabs.nl.  30       IN     AAAA   2a02:2b30:0:100:0:0:0:12")

    # CNAME
    result = Result.get('{"lts":49,"from":"2a02:3a8:0:4::2","msm_id":2439409,"fw":4700,"timestamp":1442848754,"resultset":[{"lts":49,"src_addr":"193.91.33.126","proto":"TCP","submax":3,"af":4,"subid":1,"result":{"rt":3.408,"abuf":"B6qBgAABAAEABQAIA3d3dwV5YWhvbwNjb20AAAUAAcAMAAUAAQAAAOAADwZmZC1mcDMDd2cxAWLAEMAQAAIAAQACToMABgNuczPAEMAQAAIAAQACToMABgNuczLAEMAQAAIAAQACToMABgNuczTAEMAQAAIAAQACToMABgNuczHAEMAQAAIAAQACToMABgNuczXAEMB8AAEAAQAE34wABES0gxDAfAAcAAEAANWvABAgAUmYATAAAAAAAAAAABABwFgAAQABAAJ/ggAERI7/EMBYABwAAQABTgEAECABSZgBQAAAAAAAAAAAEALARgABAAEAAjXFAATLVN01wEYAHAABAAArWAAQJAaGAAC4/gMAAAAAAAAQA8BqAAEAAQAChBsABGKKC53AjgABAAEAAmOFAAR3oPd8","NSCOUNT":5,"QDCOUNT":1,"ID":1962,"ARCOUNT":8,"ANCOUNT":1,"size":312},"time":1442848754,"dst_addr":"217.31.66.232"},{"lts":50,"src_addr":"193.91.33.126","proto":"TCP","submax":3,"af":4,"subid":2,"result":{"rt":3.155,"abuf":"2qyBgAABAAEABQAIA3d3dwV5YWhvbwNjb20AAAUAAcAMAAUAAQAAAG4ADwZmZC1mcDMDd2cxAWLAEMAQAAIAAQACcl8ABgNuczXAEMAQAAIAAQACcl8ABgNuczHAEMAQAAIAAQACcl8ABgNuczPAEMAQAAIAAQACcl8ABgNuczLAEMAQAAIAAQACcl8ABgNuczTAEMBYAAEAAQAI7C0ABES0gxDAWAAcAAEAATc+ABAgAUmYATAAAAAAAAAAABABwHwAAQABAAj5qAAERI7/EMB8ABwAAQABNz4AECABSZgBQAAAAAAAAAAAEALAagABAAEABM+NAATLVN01wGoAHAABAAE3PgAQJAaGAAC4/gMAAAAAAAAQA8COAAEAAQAI7C0ABGKKC53ARgABAAEABM+NAAR3oPd8","NSCOUNT":5,"QDCOUNT":1,"ID":55980,"ARCOUNT":8,"ANCOUNT":1,"size":312},"time":1442848755,"dst_addr":"217.31.71.30"},{"lts":56,"src_addr":"193.91.33.126","proto":"TCP","submax":3,"af":6,"subid":3,"time":1442848756,"error":{"timeout":5000},"dst_addr":"2a02:3a8:100::100"}],"prb_id":18394,"group_id":2439409,"type":"dns","msm_name":"Tdig"}')
    assert(str(result.responses[0].abuf.answers[0]) == "www.yahoo.com.          224      IN     CNAME  fd-fp3.wg1.b.yahoo.com.")

    # MX
    result = Result.get('{"src_addr":"147.83.206.82","msm_id":1012182,"fw":4520,"timestamp":1372322532,"proto":"UDP","prb_id":4662,"af":4,"result":{"abuf":"gCOEAAABAAQAAgAGBW1leGlzA25ldAAADwABwAwADwABAAACWAAZAAoGZnJvbnQxDWVtYWlsc2VjdXJpdHnADMAMAA8AAQAAAlgACwAKBmZyb250MsAwwAwADwABAAACWAALAAoGZnJvbnQzwDDADAAPAAEAAAJYAAsACgZmcm9udDTAMMAMAAIAAQAAA4QAEANuczIJaW5mb2FjY2VzwBLADAACAAEAAAOEAAYDbnMxwJXAKQABAAEAAqMAAATP+U8kwE4AAQABAAKjAAAEz/lPJcBlAAEAAQACowAABM/5TybAfAABAAEAAqMAAATP+U8qwK0AAQABAAAOEAAEz/lD/cCRAAEAAQAAHCAABM/5Tf0=","rt":209.769,"NSCOUNT":2,"QDCOUNT":1,"ANCOUNT":4,"ARCOUNT":6,"ID":32803,"size":275},"type":"dns","dst_addr":"207.249.67.253"}')
    assert(str(result.responses[0].abuf.answers[0]) == "mexis.net.              600      IN     MX     10 front1.emailsecurity.mexis.net.")

    # SOA
    result = Result.get('{"from":"2001:67c:2e8:13:220:4aff:fec6:cc9d","msm_id":1005129,"fw":"4570","af":6,"timestamp":1389966232,"proto":"UDP","msm_name":"Tdig","prb_id":9,"result":{"abuf":"NaCEAAABAAEACwALATQBNARlMTY0BGFycGEAAAYAAcAMAAYAAQACowAAOQNuczEDbmljAnVrAApob3N0bWFzdGVyB25vbWluZXQDb3JnwDNQ0vXjAAAcIAAAASwAJOoAAAAqMMAMAAIAAQACowAABgNuczPAL8AMAAIAAQACowAABgNuc2HAL8AMAAIAAQACowAABgNuczfAL8AMAAIAAQACowAABgNuc2TAL8AMAAIAAQACowAABgNuc2LAL8AMAAIAAQACowAABgNuczLAL8AMAAIAAQACowAABgNuc2PAL8AMAAIAAQACowAAAsArwAwAAgABAAKjAAAGA25zNMAvwAwAAgABAAKjAAAGA25zNcAvwAwAAgABAAKjAAAGA25zNsAvwCsAAQABAAKjAAAEw0LwgsArABwAAQACowAAECoBAEAQAQA1AAAAAAAAAALAygABAAEAAqMAAATZT6SDwHAAAQABAAKjAAAE1dsNg8D8AAEAAQACowAABMJT9IPA/AAcAAEAAqMAABAgAQYwAYEANQAAAAAAAACDwQ4AAQABAAKjAAAE1fang8EgAAEAAQACowAABNX4/oLAlAABAAEAAqMAAATUeSiCwIIAAQABAAKjAAAEnJpkA8CCABwAAQACowAAECABBQKtCQAAAAAAAAAAAAM=","rt":16.205,"NSCOUNT":11,"QDCOUNT":1,"answers":[{"RNAME":"hostmaster.nominet.org.uk.","NAME":"4.4.e164.arpa.","MNAME":"ns1.nic.uk.","TTL":172800,"SERIAL":1356002787,"TYPE":"SOA"}],"ANCOUNT":1,"ARCOUNT":11,"ID":13728,"size":506},"src_addr":"2001:67c:2e8:13:220:4aff:fec6:cc9d","type":"dns","dst_addr":"2a01:40:1001:35::2","name":"ns1.nic.uk"}')
    print(str(result.responses[0].abuf.answers[0]))
    assert(str(result.responses[0].abuf.answers[0]) == "4.4.e164.arpa.          172800   IN     SOA    ns1.nic.uk. hostmaster.nominet.org.uk. 1356002787 7200 300 2419200 10800")

    # DS
    result = Result.get('{"from":"2001:67c:2e8:11::c100:136c","msm_id":1665633,"fw":4620,"timestamp":1400801282,"resultset":[{"src_addr":"127.0.0.1","af":4,"submax":2,"proto":"UDP","subid":1,"result":{"abuf":"26SBgAABAAIAAAAADWF0dGFja3BsYW5uZXIDY29tAAArAAHADAArAAEAAN09ABhyzQgBFFW4DrGGzCGwpeh2g57Aru+SmW7ADAArAAEAAN09ACRyzQgCbb+EE82FAYk/5+rLzVV9JFVdBeTllqCu4EwDic/YGaw=","rt":0.275,"NSCOUNT":0,"QDCOUNT":1,"ANCOUNT":2,"ARCOUNT":0,"ID":56228,"size":119},"time":1400801282,"dst_addr":"127.0.0.1"},{"src_addr":"193.0.19.108","af":4,"submax":2,"proto":"UDP","subid":2,"result":{"abuf":"L0yBgAABAAIAAAAADWF0dGFja3BsYW5uZXIDY29tAAArAAHADAArAAEAAFRfACRyzQgCbb+EE82FAYk/5+rLzVV9JFVdBeTllqCu4EwDic/YGazADAArAAEAAFRfABhyzQgBFFW4DrGGzCGwpeh2g57Aru+SmW4=","rt":90.513,"NSCOUNT":0,"QDCOUNT":1,"ANCOUNT":2,"ARCOUNT":0,"ID":12108,"size":119},"time":1400801283,"dst_addr":"8.8.8.8"}],"prb_id":6012,"group_id":1665633,"type":"dns","msm_name":"Tdig"}')
    assert(str(result.responses[0].abuf.answers[0]) == "attackplanner.com.      56637    IN     DS     29389 8 1 1455b80eb186cc21b0a5e876839ec0aeef92996e")
    assert(str(result.responses[0].abuf.answers[1]) == "attackplanner.com.      56637    IN     DS     29389 8 2 6dbf8413cd8501893fe7eacbcd557d24555d05e4e596a0aee04c0389cfd819ac")

    # DNSKEY
    result = Result.get('{"lts":42,"from":"2001:df2:c00:900:c24a:ff:fecc:7938","msm_id":2392850,"fw":4700,"af":6,"timestamp":1441539311,"proto":"UDP","dst_addr":"240c:f:1:32::191","prb_id":19895,"result":{"abuf":"3y6EAAABAAMAAAABAAAwAAEAADAAAQABUYAAiAEAAwgDAQABvII3lhtZpiMzHDZyv67qQ1YDVURqv4srgiY7UMAnHqaNYhp4oaQ8pOxerUkMX1PGW4lERPY7jjphczKHH+Zd6d2itiv8DABew4Wkqgrc/Im3fCCQ7qa/wsgCeScBc3z0Gbj0PLwwZQjpET6mYGbttAuaoXeIhT27UIu6af7J/BsAADAAAQABUYABCAEBAwgDAQABy83PCnPGYP2+qafBCf+B/K6ZA1T1nPNNLQuP+63s4jxifdnr3WVVn8LjNpZpulrP7W1ZIgWr5fSd1iaktMo/E2iDh2GKYuDmnJHy+d2hh3w6/BpucWTK/zFoBz6XI7GFAmbGktJ6luV18ijMIMczK6lkRl1kEi2MPqNBQUAdYsgsebD9hQ24LOvuBgyQoUkRlhKNhvf95dcWomtUhvg8bheevpm3FX+whzMrSxY3c++NH+W1SAeoA4EceUaHJ4frScmZIMfkR77oPPs/Grrsts2jPxr9umojX8SvnZ6vH49wP/MBUWZ5FATUcac6jG289TAnVdEX2cW4KXJW7UVIIQAALgABAAFRgAETADAIAAABUYBWE6PTVewW0wvmAIZ3VP+pHu5o6u5sYU3biQwequ0b7ut2IWo2/cai8nSXLejXQeFkY1i7JlTNEKK6sHE/QGnO4x2AulHOIsbLm1VNwtDl42advEXQnojiIsH+nH4+vMP38ZLPn8eF1e5NE51ul8ixt9+2Z3SzH42B3i0AO0IiD7nfylgLJxt5m0LpNzL/DWn3aFWueSqJo6+hW/a4ghh1mRwQ+UQiO5ZR33AxNL8uZjKHSTogr0oEqklADtuaCuJJfLeEGh7gLIXmCgw59mRZEuNociaQUhFcx7EJ+GctR5Ht8EtDStHTVYtkvcjZlJZCAMYuo26X9+m+n1e6aDzasxDSD35GVnZfnHUAACkQAAAAgAAAAA==","rt":180.324,"NSCOUNT":0,"QDCOUNT":1,"ANCOUNT":3,"ARCOUNT":1,"ID":57134,"size":736},"src_addr":"2001:df2:c00:900:c24a:ff:fecc:7938","group_id":2392850,"type":"dns","msm_name":"Tdig"}')
    assert(str(result.responses[0].abuf.answers[0]) == ".                       86400    IN     DNSKEY  256 8 3 AwEAAbyCN5YbWaYjMxw2cr+u6kNWA1VEar+LK4ImO1DAJx6mjWIaeKGkPKTsXq1JDF9TxluJRET2O446YXMyhx/mXendorYr/AwAXsOFpKoK3PyJt3wgkO6mv8LIAnknAXN89Bm49Dy8MGUI6RE+pmBm7bQLmqF3iIU9u1CLumn+yfwb")
    assert(str(result.responses[0].abuf.answers[1]) == ".                       86400    IN     DNSKEY  257 8 3 AwEAAcvNzwpzxmD9vqmnwQn/gfyumQNU9ZzzTS0Lj/ut7OI8Yn3Z691lVZ/C4zaWabpaz+1tWSIFq+X0ndYmpLTKPxNog4dhimLg5pyR8vndoYd8OvwabnFkyv8xaAc+lyOxhQJmxpLSepbldfIozCDHMyupZEZdZBItjD6jQUFAHWLILHmw/YUNuCzr7gYMkKFJEZYSjYb3/eXXFqJrVIb4PG4Xnr6ZtxV/sIczK0sWN3PvjR/ltUgHqAOBHHlGhyeH60nJmSDH5Ee+6Dz7Pxq67LbNoz8a/bpqI1/Er52erx+PcD/zAVFmeRQE1HGnOoxtvPUwJ1XRF9nFuClyVu1FSCE=")
    assert(str(result.responses[0].abuf.answers[2]) == ".                       86400    IN     RRSIG  DNSKEY 8 0 86400 20151006103459 20150906103459 3046 . hndU/6ke7mjq7mxhTduJDB6q7Rvu63Yhajb9xqLydJct6NdB4WRjWLsmVM0QorqwcT9Aac7jHYC6Uc4ixsubVU3C0OXjZp28RdCeiOIiwf6cfj68w/fxks+fx4XV7k0TnW6XyLG337ZndLMfjYHeLQA7QiIPud/KWAsnG3mbQuk3Mv8NafdoVa55Komjr6Fb9riCGHWZHBD5RCI7llHfcDE0vy5mModJOiCvSgSqSUAO25oK4kl8t4QaHuAsheYKDDn2ZFkS42hyJpBSEVzHsQn4Zy1Hke3wS0NK0dNVi2S9yNmUlkIAxi6jbpf36b6fV7poPNqzENIPfkZWdl+cdQ==")

    # TXT
    result = Result.get('{"lts":15,"from":"62.237.82.14","msm_id":1423386,"fw":4700,"proto":"UDP","af":4,"msm_name":"Tdig","prb_id":6036,"result":{"abuf":"iO6EAAABAAEAAQAACGhvc3RuYW1lBGJpbmQAABAAA8AMABAAAwAAAAAAFhVuczEuZmktaGVsLmsucmlwZS5uZXTADAACAAMAAAAAAALADA==","rt":1.347,"NSCOUNT":1,"QDCOUNT":1,"answers":[{"TYPE":"TXT","NAME":"hostname.bind","RDATA":"ns1.fi-hel.k.ripe.net"}],"ID":35054,"ARCOUNT":0,"ANCOUNT":1,"size":79},"timestamp":1442845198,"src_addr":"62.237.82.14","group_id":1423314,"type":"dns","dst_addr":"193.0.14.129"}')
    assert(str(result.responses[0].abuf.answers[0]) == "hostname.bind.          0        CH     TXT    ns1.fi-hel.k.ripe.net")

    # RRSIG
    result = Result.get('{"lts":17,"from":"62.245.181.100","msm_id":2355293,"fw":4700,"timestamp":1440751763,"resultset":[{"lts":17,"src_addr":"127.0.0.1","af":4,"submax":3,"proto":"UDP","subid":1,"result":{"abuf":"rqaBgAABAAEAAgAECGNvbm9zdGl4Amx1AAAuAAHADAAuAAEAAA4QAJ8AAggCAAAOEFYHp0xV4AyX5sQIY29ub3N0aXgCbHUAlLKDqgDxe5ARXC36xLHkCTVJHGXu2iPl8iN5MskUcOcgWx4eyj+M31AoN5kUfkhwJPiDQBtt1s5ULwItBa1dFuwjTaj/4DYzIp/n1Wn59ahLR60fhwpeZxVV7nhntbZplwSETDZ47nkfp5kOhikkaJtsh85hbLqA5pkYC/42qPjAOwACAAEAAKi/ABIDbnMxCGNvbm9zdGl4A2NvbQDAOwACAAEAAKi/AAYDbnMwwNjA8gABAAEAAqMAAAQfFngjwPIAHAABAAKjAAAQKgJvAADAAAEAAAAAAAAQNcDUAAEAAQACowAABLAfcaLA1AAcAAEAAqMAABAgAUHQAAg4ogAAAAAAABA1","rt":775.563,"NSCOUNT":2,"QDCOUNT":1,"ANCOUNT":1,"ARCOUNT":4,"ID":44710,"size":336},"time":1440751763,"dst_addr":"127.0.0.1"},{"lts":18,"src_addr":"2001:a60:91ea::16","af":6,"submax":3,"proto":"UDP","subid":2,"result":{"abuf":"UQKDgAABAAAAAAAACGNvbm9zdGl4Amx1AAAuAAE=","rt":67.873,"NSCOUNT":0,"QDCOUNT":1,"ANCOUNT":0,"ARCOUNT":0,"ID":20738,"size":29},"time":1440751765,"dst_addr":"2001:4860:4860::8888"},{"lts":19,"src_addr":"62.245.181.100","af":4,"submax":3,"proto":"UDP","subid":3,"result":{"abuf":"dkiDgAABAAAAAAAACGNvbm9zdGl4Amx1AAAuAAE=","rt":129.617,"NSCOUNT":0,"QDCOUNT":1,"ANCOUNT":0,"ARCOUNT":0,"ID":30280,"size":29},"time":1440751766,"dst_addr":"8.8.8.8"}],"prb_id":6123,"group_id":2355293,"type":"dns","msm_name":"Tdig"}')
    assert(str(result.responses[0].abuf.answers[0]) == "conostix.lu.            3600     IN     RRSIG  NS 8 2 3600 20150927082236 20150828072407 59076 conostix.lu. lLKDqgDxe5ARXC36xLHkCTVJHGXu2iPl8iN5MskUcOcgWx4eyj+M31AoN5kUfkhwJPiDQBtt1s5ULwItBa1dFuwjTaj/4DYzIp/n1Wn59ahLR60fhwpeZxVV7nhntbZplwSETDZ47nkfp5kOhikkaJtsh85hbLqA5pkYC/42qPg=")


def test_error_propagation():
    result = Result.get('{"lts":31,"from":"190.111.120.51","msm_id":10301,"fw":4700,"af":4,"timestamp":1443691516,"proto":"UDP","dst_addr":"193.0.14.129","prb_id":11180,"result":{"abuf":"NSSAhAAAAAAAAAAA","rt":1.282,"NSCOUNT":0,"QDCOUNT":0,"ANCOUNT":0,"ARCOUNT":0,"ID":13604,"size":12},"src_addr":"172.16.0.45","type":"dns","msm_name":"Tdig"}')
    assert(bool(result.responses[0].abuf))
    assert(bool(result.responses[0].is_error))

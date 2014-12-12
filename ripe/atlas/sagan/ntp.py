from .base import Result, ValidationMixin


class Packet(ValidationMixin):

    def __init__(self, data, **kwargs):

        ValidationMixin.__init__(self, **kwargs)

        self.final_ts = self.ensure("final-ts", float)
        self.offset = self.ensure("offset", float)
        self.origin_ts = self.ensure("origin-ts", float)
        self.receive_ts = self.ensure("receive-ts", float)
        self.rtt = self.ensure("rtt", float)
        self.transmit_ts = self.ensure("transmit-ts", float)


class NtpResult(Result):
    """
    {"af":4,"dst_addr":"193.0.0.229","dst_name":"193.0.0.229","from":"193.0.0.78","fw":4670,
    "group_id":1020237,"li":"no","lts":-1,"mode":"server","msm_id":1020237,"msm_name":"Ntp",
    "poll":1,"prb_id":71,"precision":0.0000019074,"proto":"UDP","ref-id":"GPS",
    "ref-ts":3627199357.7446351051,"result":[
        {"final-ts":3627199379.8182010651,"offset":-8.363271,"origin-ts":3627199379.7962741852,
        "receive-ts":3627199388.1704945564,"rtt":0.021899,"transmit-ts":3627199388.170522213},
        {"final-ts":3627199379.831638813,"offset":-8.36871,"origin-ts":3627199379.8214530945,
        "receive-ts":3627199388.1952428818,"rtt":0.01016,"transmit-ts":3627199388.195268631},
        {"final-ts":3627199379.8474769592,"offset":-8.372775,"origin-ts":3627199379.8454480171,
        "receive-ts":3627199388.2192249298,"rtt":0.002004,"transmit-ts":3627199388.2192502022}
    ],
    "root-delay":0,"root-dispersion":0.00140381,"src_addr":"10.0.2.12","stratum":1,
    "timestamp":1418210579,"type":"ntp","version":4}
    """

    def __init__(self, data, **kwargs):

        Result.__init__(self, data, **kwargs)

        self.af = self.ensure("af", int)
        self.destination_address = self.ensure("dst_addr", str)
        self.destination_name = self.ensure("dst_name", str)
        self.source_address = self.ensure("src_addr", str)
        self.end_time = self.ensure("endtime",  "datetime")
        self.li = self.ensure("li", str)
        self.mode = self.ensure("mode", str)
        self.poll = self.ensure("poll", str)
        self.precision = self.ensure("precision", float)
        self.ref_id = self.ensure("ref-id", str)
        self.root_delay = self.ensure("root-delay", int)
        self.root_dispersion = self.ensure("root-dispersion", int)
        self.stratum = self.ensure("stratum", int)
        self.version = self.ensure("version", int)

        self.responses = []

        if "result" not in self.raw_data:
            self._handle_malformation("No result value found")
            return

        for response in self.raw_data["result"]:
            self.responses.append(Packet(response, **kwargs))


__all__ = (
    "NtpResult"
)

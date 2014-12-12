from ripe.atlas.sagan import Result, ResultError
from ripe.atlas.sagan.ntp import NtpResult

def test_ntp_valid():
    result = (
        '{"af":4,"dst_addr":"193.0.0.229","dst_name":"193.0.0.229","from":"193.0.0.78","fw":4670,'
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
    assert(result.destination_name == "193.0.0.229")
    assert(result.source_address == "10.0.2.12")

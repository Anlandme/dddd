select A.FChannelRateRuleID as rule_id
    , B.FPayMdmMerchantID as merchant_id
    , C.FOU as merchant_name
    , A.FMdmMerchantID as mdm_merchant_id
from sett_conf_v2.t_merchant_rateid_relation A
left join midaspay_conf.t_midaspay_merchant_relation B
    on A.FMdmMerchantID = B.FMdmMerchantID
left join mdm_merchant_conf.t_mdm_merchant_info C
    on A.FMdmMerchantID = C.FMdmMerchantID
where A.FStatus = 1 and B.FStatus = 1 and C.FStatus = 1
;


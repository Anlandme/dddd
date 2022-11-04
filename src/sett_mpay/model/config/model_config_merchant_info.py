"""
    商户信息
    sett_conf_v2.t_business_merchant_info
"""
from typing import List, Dict
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import OUInfoData


class MerchantInfoData(BaseBean):
    def __init__(self):
        self.contract_no = ''
        self.rule_id = ''
        self.rule_name = ''
        self.merchant_type = ''
        self.merchant_ou_id = ''
        self.merchant_ou_name = ''
        self.merchant_ou_short = ''
        self.merchant_mdm_id = ''
        self.merchant_mdm_name = ''
        self.merchant_coa_no = ''
        self.merchant_coa_name = ''
        self.merchant_cost_no = ''
        self.merchant_cost_name = ''
        self.date_begin = ''
        self.mdate_end = ''

    def update_merchant_info(self, merchant_ou_info: OUInfoData):
        self.merchant_ou_id = merchant_ou_info.FOuID
        self.merchant_ou_name = merchant_ou_info.FOuFullName
        self.merchant_ou_short = merchant_ou_info.FOuName
        if str(self.merchant_type) == "1":
            self.merchant_type = "INTERNAL"
        elif str(self.merchant_type) == "2":
            self.merchant_type = "EXTERNAL"

    @staticmethod
    def get_merchant_rules_dict(
            sett_midas_merchant: MySQLClient
            , ou_info_dict: Dict[str, OUInfoData]
    ):
        sql = '''
            select FContractNo as contract_no
                , FChannelRateRuleID as rule_id
                , FChannelRateRuleName as rule_name
                , FMerchantType as merchant_type
                , FMerchantOuID as merchant_ou_id
                , FMdmID as merchant_mdm_id
                , FMdmName as merchant_mdm_name
                , FCoaProductNo as merchant_coa_no
                , FCoaProductName as merchant_coa_name
                , FMerchantCostID as merchant_cost_no
                , FMerchantCostCenter as merchant_cost_name
                , FBeginDate as date_begin
                , FEndDate as date_end
            from sett_conf_v2.t_business_merchant_info
            where FStatus = 1
        '''
        db_ret = sett_midas_merchant.query(sql, cls=MerchantInfoData)
        data_list: List[MerchantInfoData] = db_ret.data

        msg_set = set()
        data_dict = {}
        for data in data_list:
            if data.merchant_ou_id not in ou_info_dict:
                msg_set.add("missing ou info: {}".format(data.merchant_ou_id))
                continue
            merchant_ou_info = ou_info_dict[data.merchant_ou_id]
            data.update_merchant_info(merchant_ou_info)
            data_dict[data.contract_no] = data
        # end for
        return True, msg_set, data_dict


if __name__ == '__main__':
    pass

"""
    商户规则
    sett_conf_v2.t_business_merchant_info
    sett_conf_v2.t_merchant_channel_rate_info
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import OUInfoData
from src import PltInfoData


class MerchantRulesData(BaseBean):
    def __init__(self):
        self.contract_no = ''
        self.rule_id = ''
        self.mcid = ''
        self.country = ''
        self.province = ''
        self.city = ''
        self.percent_fee_rate = ''
        self.per_transaction_fee = ''
        self.per_transaction_fee_currency = ''
        self.had_special_rules = ''
        self.special_rules = ''
        self.tax_fee_order = ''

        self.plt_type = ''
        self.plt_ou_id = ''
        self.plt_ou_name = ''
        self.plt_ou_short = ''
        self.plt_mdm_id = ''
        self.plt_mdm_name = ''
        self.plt_coa_no = ''
        self.plt_coa_name = ''
        self.plt_cost_no = ''
        self.plt_cost_name = ''
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
        self.main_date_begin = ''
        self.main_date_end = ''
        self.sub_date_begin = ''
        self.sub_date_end = ''

    def update_plt_info(self, plt_info: PltInfoData, plt_ou_info: OUInfoData):
        self.plt_type = plt_info.plt_type
        self.plt_ou_id = plt_ou_info.FOuID
        self.plt_ou_name = plt_ou_info.FOuFullName
        self.plt_ou_short = plt_ou_info.FOuName
        self.plt_mdm_id = plt_info.plt_mdm_id
        self.plt_mdm_name = plt_info.plt_mdm_name
        self.plt_coa_no = plt_info.plt_coa_no
        self.plt_coa_name = plt_info.plt_coa_name
        self.plt_cost_no = plt_info.plt_cost_no
        self.plt_cost_name = plt_info.plt_cost_name

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
            , data_month
            , ou_info_dict: Dict[str, OUInfoData]
            , plt_info_dict: Dict[str, PltInfoData]
    ):
        last_date = Xutil.get_month_last_day(data_month)
        sql = '''
            select A.FContractNo as contract_no
                , A.FChannelRateRuleID as rule_id
                , A.FMidasChannelID as mcid
                , A.FCountryCode as country
                , A.FProvince as province
                , A.FCity as city
                , A.FChannelRate as percent_fee_rate
                , A.FPerTransactionFee as per_transaction_fee
                , A.FPerTransactionFeeCurrencyType as per_transaction_fee_currency
                , A.FHadSpecialRules as had_special_rules
                , A.FSpecialRules as special_rules
                , A.FTaxFeeOrder as tax_fee_order
                
                , B.FOuID as plt_ou_id
                , B.FMerchantType as merchant_type
                , B.FMerchantOuID as merchant_ou_id
                , B.FMdmID as merchant_mdm_id
                , B.FMdmName as merchant_mdm_name
                , B.FCoaProductNo as merchant_coa_no
                , B.FCoaProductName as merchant_coa_name
                , B.FMerchantCostID as merchant_cost_no
                , B.FMerchantCostCenter as merchant_cost_name
                , B.FBeginDate as main_date_begin
                , B.FEndDate as main_date_end
                , A.FBeginDate as sub_date_begin
                , A.FEndDate as sub_date_end
            from sett_conf_v2.t_merchant_channel_rate_info A
            left join sett_conf_v2.t_business_merchant_info B
                on A.FChannelRateRuleID = B.FChannelRateRuleID and A.FContractNo = B.FContractNo    
            where A.FStatus = 1 and A.FBeginDate <= '{data_date}' and A.FEndDate >= '{data_date}'
                and B.FStatus = 1 and B.FBeginDate <= '{data_date}' and B.FEndDate >= '{data_date}'
        '''.format(data_date=last_date)
        db_ret = sett_midas_merchant.query(sql, cls=MerchantRulesData)
        data_list: List[MerchantRulesData] = db_ret.data

        msg_set = set()
        data_dict = {}
        for data in data_list:
            if data.plt_ou_id not in plt_info_dict:
                msg_set.add("missing plt info: {}".format(data.plt_ou_id))
                continue
            if data.plt_ou_id not in ou_info_dict:
                msg_set.add("missing ou info: {}".format(data.plt_ou_id))
                continue
            if data.merchant_ou_id not in ou_info_dict:
                msg_set.add("missing ou info: {}".format(data.merchant_ou_id))
                continue
            plt_info = plt_info_dict[data.plt_ou_id]
            plt_ou_info = ou_info_dict[data.plt_ou_id]
            merchant_ou_info = ou_info_dict[data.merchant_ou_id]

            data.update_plt_info(plt_info, plt_ou_info)
            data.update_merchant_info(merchant_ou_info)
            data.country = str(data.country).upper()

            key = Xutil.link_words(data.rule_id, data.mcid, data.country)
            if key not in data_dict:
                data_dict[key] = data
            else:
                msg_set.add("duplicate channel rule: {}".format(key))
        # end for
        return True, msg_set, data_dict

    @staticmethod
    def get_rule_id_mapper(db_sett_merchant: MySQLClient):
        sql = '''
            select B.FPayMdmMerchantID as mch_id
                , A.FChannelRateRuleID as rule_id
            from sett_conf_v2.t_merchant_rateid_relation A
            left join midaspay_conf.t_midaspay_merchant_relation B
                on A.FMdmMerchantID = B.FMdmMerchantID
            where A.FStatus = 1 and B.FStatus = 1
        '''
        db_ret = db_sett_merchant.query(sql)

        data_dict = {}
        for line in db_ret.data:
            mch_id = line["mch_id"]
            rule_id = line["rule_id"]
            data_dict[mch_id] = rule_id
        # end for
        return data_dict

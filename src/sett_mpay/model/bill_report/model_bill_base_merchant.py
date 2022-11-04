"""
    账单基础: 渠道账单
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import CountryInfoData
from src import ChannelRulesData
from src import MerchantRulesData
from src import MerchantMapperData


class MerchantBillBaseData(BaseBean):
    def __init__(self):
        self.sett_month = ''
        self.bill_month = ''
        self.due_month = ''
        self.due_date = ''
        self.merchant_id = ''
        self.merchant_name = ''
        self.sub_merchant_id = ''
        self.sub_merchant_name = ''
        self.product_no = ''
        self.product_name = ''
        self.channel = ''
        self.cid = ''
        self.mcid = ''
        self.sub_channel = ''
        self.channel_country_code = ''
        self.channel_country_name = ''
        self.midas_country_code = ''
        self.midas_country_name = ''
        self.ori_currency = ''
        self.ori_income = 0.0
        self.ori_refund = 0.0
        self.ori_channel_tax = 0.0
        self.ori_channel_tax_rate = 0.0
        self.ori_channel_fee = 0.0
        self.ori_channel_fee_rate = 0.0
        self.ori_merchant_fee = 0.0
        self.ori_merchant_fee_rate = 0.0
        self.ori_plt_fee = 0.0
        self.ori_sett_currency_rate = 0.0
        self.sett_currency = ''
        self.sett_income = 0.0
        self.sett_refund = 0.0
        self.sett_channel_tax = 0.0
        self.sett_channel_fee = 0.0
        self.sett_merchant_fee = 0.0
        self.sett_plt_fee = 0.0
        self.sett_rmb_currency_rate = ''
        self.rmb_income = 0.0
        self.rmb_refund = 0.0
        self.rmb_channel_tax = 0.0
        self.rmb_channel_fee = 0.0
        self.rmb_merchant_fee = 0.0
        self.rmb_plt_fee = 0.0

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
        self.merchant_contract_no = ''
        self.channel_mdm_id = ''
        self.channel_mdm_name = ''
        self.channel_contract_no = ''

    def update_period(self):
        self.due_month = Xutil.get_month_next(self.bill_month)
        self.due_date = Xutil.get_month_last_day(self.due_month)
        return True, "SUCCESS"

    def update_country_info(self, country_info_dict: Dict[str, CountryInfoData]):
        if self.channel_country_name in country_info_dict:
            channel_country_info = country_info_dict[self.channel_country_name]
            self.channel_country_name = channel_country_info.country_name
            self.channel_country_code = channel_country_info.country_code
        if self.midas_country_name in country_info_dict:
            midas_country_info = country_info_dict[self.midas_country_name]
            self.midas_country_name = midas_country_info.country_name
            self.midas_country_code = midas_country_info.country_code
        return True, "SUCCESS"

    def update_channel_rule(self, channel_rules_dict: Dict[str, ChannelRulesData]):
        cid = self.cid
        country = self.channel_country_code
        if cid.startswith("UniPin"):
            country = self.midas_country_code
        key1 = Xutil.link_words(cid, country)
        key2 = Xutil.link_words(cid, "Global")
        key3 = Xutil.link_words(cid, "*")
        if key1 in channel_rules_dict:
            channel_rule = channel_rules_dict[key1]
        elif key2 in channel_rules_dict:
            channel_rule = channel_rules_dict[key2]
        elif key3 in channel_rules_dict:
            channel_rule = channel_rules_dict[key3]
        else:
            msg = "missing channel rule: {}".format(Xutil.link_words(
                self.channel, self.cid, self.channel_country_code
            ))
            return False, msg
        self.channel = channel_rule.channel
        self.channel_mdm_id = channel_rule.channel_mdm_id
        self.channel_mdm_name = channel_rule.channel_mdm_name
        self.channel_contract_no = channel_rule.contract_no
        self.sett_currency = channel_rule.sett_currency
        return True, "SUCCESS"

    def cal_exchange(self, exchange_dict: Dict[str, float]):
        ori_currency = self.ori_currency
        sett_currency = self.sett_currency
        key_ori_sett = Xutil.link_words("HS", self.bill_month, ori_currency, sett_currency)
        key_sett_rmb = Xutil.link_words("HS", self.bill_month, sett_currency, "CNY")
        if key_ori_sett not in exchange_dict:
            msg = "missing exchange rate: {}".format(key_ori_sett)
            return False, msg
        if key_sett_rmb not in exchange_dict:
            msg = "missing exchange rate: {}".format(key_ori_sett)
            return False, msg
        ori_sett_rate = float(exchange_dict[key_ori_sett])
        sett_rmb_rate = float(exchange_dict[key_sett_rmb])

        self.ori_sett_currency_rate = ori_sett_rate
        self.sett_income = ori_sett_rate * float(self.ori_income)
        self.sett_channel_tax = ori_sett_rate * float(self.ori_channel_tax)
        self.sett_channel_fee = ori_sett_rate * float(self.ori_channel_fee)
        self.sett_merchant_fee = ori_sett_rate * float(self.ori_merchant_fee)
        self.sett_plt_fee = ori_sett_rate * float(self.ori_plt_fee)

        self.sett_rmb_currency_rate = sett_rmb_rate
        self.rmb_income = sett_rmb_rate * float(self.sett_income)
        self.rmb_channel_tax = sett_rmb_rate * float(self.sett_channel_tax)
        self.rmb_channel_fee = sett_rmb_rate * float(self.sett_channel_fee)
        self.rmb_merchant_fee = sett_rmb_rate * float(self.sett_merchant_fee)
        self.rmb_plt_fee = sett_rmb_rate * float(self.sett_plt_fee)
        return True, "SUCCESS"

    def update_merchant_rule(
            self
            , merchant_rules_dict: Dict[str, MerchantRulesData]
            , merchant_mapper_dict: Dict[str, MerchantMapperData]
    ):
        """
            更新商户规则信息
        :param rule_id_mapper: merchant_id -> rule_id
        :param merchant_rules_dict:
        :return:
        """
        if self.merchant_id not in merchant_mapper_dict:
            msg = "missing merchant rule_id: {}".format(self.merchant_id)
            return False, msg
        merchant_biz_info = merchant_mapper_dict[self.merchant_id]
        rule_id = merchant_biz_info.rule_id
        merchant_name = merchant_biz_info.merchant_name

        key1 = Xutil.link_words(rule_id, self.mcid, self.midas_country_code)
        key2 = Xutil.link_words(rule_id, self.mcid, "GLOBAL")
        key3 = Xutil.link_words(rule_id, self.mcid, self.midas_country_code)
        if key1 in merchant_rules_dict:
            merchant_rule = merchant_rules_dict[key1]
        elif key2 in merchant_rules_dict:
            merchant_rule = merchant_rules_dict[key2]
        elif key3 in merchant_rules_dict:
            merchant_rule = merchant_rules_dict[key3]
        else:
            msg = "missing merchant_rule: {}".format(Xutil.link_words(
                rule_id, self.mcid, self.midas_country_code, self.merchant_id, self.channel, self.cid
            ))
            return False, msg

        self.merchant_name = merchant_name
        self.plt_type = merchant_rule.plt_type
        self.plt_ou_id = merchant_rule.plt_ou_id
        self.plt_ou_name = merchant_rule.plt_ou_name
        self.plt_ou_short = merchant_rule.plt_ou_short
        self.plt_mdm_id = merchant_rule.plt_mdm_id
        self.plt_mdm_name = merchant_rule.plt_mdm_name
        self.plt_coa_no = merchant_rule.plt_coa_no
        self.plt_coa_name = merchant_rule.plt_coa_name
        self.plt_cost_no = merchant_rule.plt_cost_no
        self.plt_cost_name = merchant_rule.plt_cost_name

        self.merchant_type = merchant_rule.merchant_type
        self.merchant_ou_id = merchant_rule.merchant_ou_id
        self.merchant_ou_name = merchant_rule.merchant_ou_name
        self.merchant_ou_short = merchant_rule.merchant_ou_short
        self.merchant_mdm_id = merchant_rule.merchant_mdm_id
        self.merchant_mdm_name = merchant_rule.merchant_mdm_name
        self.merchant_coa_no = merchant_rule.merchant_coa_no
        self.merchant_coa_name = merchant_rule.merchant_coa_name
        self.merchant_cost_no = merchant_rule.merchant_cost_no
        self.merchant_cost_name = merchant_rule.merchant_cost_name
        self.merchant_contract_no = merchant_rule.contract_no
        return True, "SUCCESS"

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, data_list):
        sql = '''
            delete from db_mpay_income.t_mpay_bill_base_merchant
            where sett_month = '{}'
        '''.format(sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_income", "t_mpay_bill_base_merchant")

    @staticmethod
    def get_base_bill_list(db_sett: MySQLClient, sett_moth, merchant_type=None):
        sql = '''
            select * 
            from db_mpay_income.t_mpay_bill_base_merchant
            where sett_month = '{}'
        '''.format(sett_moth)
        if merchant_type:
            sql += " and merchant_type = '{}'".format(merchant_type)
        db_ret = db_sett.query(sql, cls=MerchantBillBaseData)
        data_list: List[MerchantBillBaseData] = db_ret.data
        return data_list

    @staticmethod
    def get_merchant_sett_base(db_sett: MySQLClient, bill_month):
        sql = '''
            select bill_month
                , merchant_id
                , merchant_name
                , sub_merchant_id
                , sub_merchant_name
                , cid
                , mcid
                , payment_channel as sub_channel
                , channel_country as channel_country_name
                , midas_country as midas_country_name
                , ori_currency as ori_currency
                , sum(tran_amount) as ori_income
                , sum(tax_amount) as ori_channel_tax
                , sum(c_fee_total) as ori_channel_fee
                , sum(m_fee_total) as ori_merchant_fee
                , sum(m_fee_total - c_fee_total) as ori_plt_fee
            from db_sett_oversea_merchant_v2.t_merchant_sett_base
            where bill_month = '{}' 
            group by bill_month, merchant_id, merchant_name
                , sub_merchant_id, sub_merchant_name, cid, mcid
                , payment_channel, channel_country, midas_country, ori_currency
        '''.format(bill_month)
        db_ret = db_sett.query(sql, cls=MerchantBillBaseData)
        base_list: List[MerchantBillBaseData] = db_ret.data

        data_list = []
        for base_data in base_list:
            data_list.append(base_data)
        # end for
        return data_list

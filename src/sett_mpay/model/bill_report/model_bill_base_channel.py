"""
    账单基础: 渠道账单
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import ChannelRulesData
from src import BillSettlementBaseData


class ChannelBillBaseData(BaseBean):
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

    def update_base_data(self, base_data: BillSettlementBaseData):
        self.sett_month = base_data.sett_month
        self.bill_month = base_data.bill_month
        self.due_month = base_data.due_month
        self.due_date = base_data.due_date
        self.product_no = base_data.product_no
        self.product_name = base_data.product_name
        self.channel = base_data.channel
        self.cid = base_data.cid
        self.mcid = base_data.mcid
        self.sub_channel = base_data.sub_channel
        self.channel_country_code = base_data.channel_country_code
        self.channel_country_name = base_data.channel_country_name
        self.midas_country_code = base_data.midas_country_code
        self.midas_country_name = base_data.midas_country_name
        self.ori_currency = base_data.ori_currency
        self.ori_income = base_data.ori_income
        self.ori_channel_tax = base_data.ori_channel_tax
        self.ori_channel_fee = base_data.ori_channel_fee
        self.ori_merchant_fee = 0.0
        self.ori_plt_fee = 0.0
        self.sett_currency = base_data.sett_currency
        self.product_no = ""
        self.product_name = "MidasPay"

    def update_channel_rule(self, channel_rules_dict: Dict[str, ChannelRulesData]):
        cid = self.cid
        country = self.channel_country_code
        key1 = Xutil.link_words(cid, country)
        key2 = Xutil.link_words(cid, "GLOBAL")
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
        self.channel_mdm_id = channel_rule.channel_mdm_id
        self.channel_mdm_name = channel_rule.channel_mdm_name
        self.channel_contract_no = channel_rule.contract_no
        self.plt_type = channel_rule.plt_type
        self.plt_ou_id = channel_rule.plt_ou_id
        self.plt_ou_name = channel_rule.plt_ou_name
        self.plt_ou_short = channel_rule.plt_ou_short
        self.plt_mdm_id = channel_rule.plt_mdm_id
        self.plt_mdm_name = channel_rule.plt_mdm_name
        self.plt_coa_no = channel_rule.plt_coa_no
        self.plt_coa_name = channel_rule.plt_coa_name
        self.plt_cost_no = channel_rule.plt_cost_no
        self.plt_cost_name = channel_rule.plt_cost_name
        return True, "SUCCESS"

    def cal_exchange(self, exchange_dict: Dict[str, float]):
        ori_currency = self.ori_currency
        sett_currency = self.sett_currency
        key_ori_sett = Xutil.link_words("HS", self.bill_month, ori_currency, sett_currency)
        key_sett_rmb = Xutil.link_words("HS", self.bill_month, sett_currency, "CNY")
        if key_ori_sett not in exchange_dict:
            msg = "missing exchange rate: {}".format(Xutil.link_words(key_ori_sett, self.channel))
            return False, msg
        if key_sett_rmb not in exchange_dict:
            msg = "missing exchange rate: {}".format(Xutil.link_words(key_ori_sett, self.channel))
            return False, msg
        ori_sett_rate = float(exchange_dict[key_ori_sett])
        sett_rmb_rate = float(exchange_dict[key_sett_rmb])

        self.ori_sett_currency_rate = ori_sett_rate
        self.sett_income = ori_sett_rate * self.ori_income
        self.sett_channel_tax = ori_sett_rate * self.ori_channel_tax
        self.sett_channel_fee = ori_sett_rate * self.ori_channel_fee
        self.sett_merchant_fee = ori_sett_rate * self.ori_merchant_fee
        self.sett_plt_fee = ori_sett_rate * self.ori_plt_fee

        self.sett_rmb_currency_rate = sett_rmb_rate
        self.rmb_income = sett_rmb_rate * self.sett_income
        self.rmb_channel_tax = sett_rmb_rate * self.sett_channel_tax
        self.rmb_channel_fee = sett_rmb_rate * self.sett_channel_fee
        self.rmb_merchant_fee = sett_rmb_rate * self.sett_merchant_fee
        self.rmb_plt_fee = sett_rmb_rate * self.sett_plt_fee
        return True, "SUCCESS"

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, data_list):
        sql = '''
            delete from db_mpay_income.t_mpay_bill_base_channel
            where sett_month = '{}'
        '''.format(sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_income", "t_mpay_bill_base_channel")

    @staticmethod
    def get_base_bill_list(db_sett: MySQLClient, sett_moth):
        sql = '''
               select * 
               from db_mpay_income.t_mpay_bill_base_channel
               where sett_month = '{}'
           '''.format(sett_moth)
        db_ret = db_sett.query(sql, cls=ChannelBillBaseData)
        data_list: List[ChannelBillBaseData] = db_ret.data
        return data_list

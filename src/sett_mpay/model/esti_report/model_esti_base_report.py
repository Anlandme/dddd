"""
    暂估基础流水
    db_sett_oversea.t_hs_base_water_v3
"""
from typing import List, Dict

from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import TaxFeeData
from src import ChannelFeeData
from src import MerchantFeeData
from src import RefundFeeData
from src import ChannelRulesData
from src import MerchantRulesData
from src import EstiBaseWater


class EstiBaseReport(BaseBean):
    def __init__(self):
        self.sett_month = ''
        self.bill_month = ''
        self.data_month = ''
        self.data_date = ''
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
        self.payment_period = ''
        self.channel_country_code = ''
        self.channel_country_name = ''
        self.midas_country_code = ''
        self.midas_country_name = ''
        self.tran_type = ''
        self.tran_currency = ''
        self.tran_amount = 0.0
        self.tran_numbers = 0.0
        self.tax_fee_order = ''
        self.ori_currency = ''
        self.ori_income = 0.0
        self.ori_refund = 0.0
        self.ori_channel_refund_fee = 0.0
        self.ori_merchant_refund_fee = 0.0
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
        self.sett_channel_refund_fee = 0.0
        self.sett_merchant_refund_fee = 0.0
        self.sett_channel_tax = 0.0
        self.sett_channel_fee = 0.0
        self.sett_merchant_fee = 0.0
        self.sett_plt_fee = 0.0
        self.sett_rmb_currency_rate = 0.0
        self.rmb_income = 0.0
        self.rmb_refund = 0.0
        self.rmb_channel_refund_fee = 0.0
        self.rmb_merchant_refund_fee = 0.0
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

    def update_period(self, sett_month):
        self.sett_month = sett_month
        self.bill_month = Xutil.get_month_next(sett_month)

    def update_base_water(self, base_data: EstiBaseWater):
        self.data_month = base_data.data_month
        self.data_date = base_data.data_date
        self.merchant_id = base_data.merchant_id
        self.sub_merchant_id = base_data.sub_merchant_id
        self.channel = base_data.channel
        self.cid = base_data.cid
        self.mcid = base_data.mcid
        self.sub_channel = base_data.sub_channel
        self.channel_country_code = base_data.channel_country_code
        self.channel_country_name = base_data.channel_country_name
        self.midas_country_code = base_data.midas_country_code
        self.midas_country_name = base_data.midas_country_name
        self.tran_type = base_data.tran_type
        self.tran_currency = base_data.tran_currency
        self.tran_amount = base_data.tran_amount
        self.tran_numbers = base_data.tran_numbers
        self.ori_currency = base_data.tran_currency
        self.ori_income = base_data.tran_amount

    def update_tax_fee(self, tax_fee: TaxFeeData):
        self.ori_channel_tax = tax_fee.tax_amount
        self.ori_channel_tax_rate = tax_fee.tax_rate

    def update_channel_fee(self, channel_fee: ChannelFeeData):
        self.tax_fee_order = channel_fee.tax_fee_order
        self.ori_channel_fee = channel_fee.channel_fee_total
        self.ori_channel_percent_fee_rate = channel_fee.channel_percent_fee_rate
        self.ori_channel_percent_fee_amount = channel_fee.channel_percent_fee_amount
        self.ori_channel_per_transaction_fee = channel_fee.channel_per_transaction_fee
        self.ori_channel_per_transaction_fee_amount = channel_fee.channel_per_transaction_fee_amount

        channel_rule: ChannelRulesData = channel_fee.channel_rule
        self.sett_currency = channel_rule.sett_currency
        self.payment_period = channel_rule.payment_period
        self.channel_mdm_id = channel_rule.channel_mdm_id
        self.channel_mdm_name = channel_rule.channel_mdm_name
        self.channel_contract_no = channel_rule.contract_no

    def update_merchant_fee(self, merchant_fee: MerchantFeeData):
        self.merchant_id = merchant_fee.merchant_id
        self.merchant_name = merchant_fee.merchant_name
        self.ori_merchant_fee = merchant_fee.merchant_fee_total
        self.ori_merchant_percent_fee_rate = merchant_fee.merchant_percent_fee_rate
        self.ori_merchant_percent_fee_amount = merchant_fee.merchant_percent_fee_amount
        self.ori_merchant_per_transaction_fee = merchant_fee.merchant_per_transaction_fee
        self.ori_merchant_per_transaction_fee_amount = merchant_fee.merchant_per_transaction_fee_amount

        merchant_rule: MerchantRulesData = merchant_fee.merchant_rule
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

    def update_refund_fee(self, refund_fee: RefundFeeData):
        self.ori_channel_refund_fee = refund_fee.channel_refund_fee_total
        self.ori_merchant_refund_fee = refund_fee.merchant_refund_fee_total

    def cal_exchange(self, exchange_rate_dict: Dict[str, float]):
        key_ori_sett = Xutil.link_words(self.ori_currency, self.sett_currency)
        key_sett_rmb = Xutil.link_words(self.sett_currency, "CNY")
        if key_ori_sett not in exchange_rate_dict:
            msg = "missing currency rate: {}".format(key_ori_sett)
            return False, msg
        if key_sett_rmb not in exchange_rate_dict:
            msg = "missing currency rate: {}".format(key_ori_sett)
            return False, msg

        ori_sett_rate = float(exchange_rate_dict[key_ori_sett])
        self.ori_sett_currency_rate = ori_sett_rate
        self.sett_income = ori_sett_rate * self.ori_income
        self.sett_refund = ori_sett_rate * self.ori_refund
        self.sett_channel_tax = ori_sett_rate * self.ori_channel_tax
        self.sett_channel_fee = ori_sett_rate * self.ori_channel_fee
        self.sett_merchant_fee = ori_sett_rate * self.ori_merchant_fee
        self.sett_plt_fee = ori_sett_rate * self.ori_plt_fee
        self.sett_channel_refund_fee = ori_sett_rate * self.ori_channel_refund_fee
        self.sett_merchant_refund_fee = ori_sett_rate * self.ori_merchant_refund_fee

        sett_rmb_rate = float(exchange_rate_dict[key_sett_rmb])
        self.sett_rmb_currency_rate = sett_rmb_rate
        self.rmb_income = sett_rmb_rate * self.sett_income
        self.rmb_refund = sett_rmb_rate * self.sett_refund
        self.rmb_channel_tax = sett_rmb_rate * self.sett_channel_tax
        self.rmb_channel_fee = sett_rmb_rate * self.sett_channel_fee
        self.rmb_merchant_fee = sett_rmb_rate * self.sett_merchant_fee
        self.rmb_plt_fee = sett_rmb_rate * self.sett_plt_fee
        self.rmb_channel_refund_fee = ori_sett_rate * self.sett_channel_refund_fee
        self.rmb_merchant_refund_fee = ori_sett_rate * self.sett_merchant_refund_fee
        return True, "SUCCESS"

    @staticmethod
    def get_data_list(db_sett: MySQLClient, sett_month):
        sql = '''
            select * from db_mpay_income.t_mpay_esti_base
            where sett_month = '{sett_month}'
        '''.format(sett_month=sett_month)
        db_ret = db_sett.query(sql, cls=EstiBaseReport)
        data_list: List[EstiBaseReport] = db_ret.data
        return data_list

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, data_list):
        sql = '''
            delete from db_mpay_income.t_mpay_esti_base 
            where sett_month = '{sett_month}'
        '''.format(sett_month=sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_income", "t_mpay_esti_base")

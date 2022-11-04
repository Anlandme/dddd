"""
    账单基础基础汇率：对账交集 * XE汇率
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient


class BillBaseExchangeData(BaseBean):
    def __init__(self):
        self.data_type = ''
        self.data_date = ''
        self.data_month = ''
        self.channel = ''
        self.cid = ''
        self.mcid = ''
        self.merchant_id = ''
        self.sub_merchant_id = ''
        self.tran_type = ''
        self.tran_currency = ''
        self.tran_amount = 0
        self.tran_sett_rate = 0
        self.sett_currency = ''
        self.sett_amount = 0
        self.sett_rmb_rate = 0
        self.rmb_amount = 0

    def update_exchange(self, xe_exchange_dict: Dict[str, float], sett_currency_dict: Dict[str, str]):
        """
            汇率转换
        :param xe_exchange_dict: {"YYYY-MM-DD | currency_ori | currency_dst": 1.0}
        :param sett_currency_dict: {"cid": "USD"}
        :return:
        """
        self.data_date = Xutil.format_date(self.data_date, format_input="%Y%m%d", format_output="%Y-%m-%d")
        self.data_month = Xutil.format_date(self.data_month, format_input="%Y%m", format_output="%Y-%m")
        if self.tran_type not in ["TRADE_TYPE_PAY"]:
            msg = "new TRADE_TYPE_PAY: {} | {}".format(self.channel, self.tran_type)
            return False, msg

        # 结算币种
        if self.cid not in sett_currency_dict:
            msg = "missing sett_currency: {} | {}".format(self.channel, self.cid)
            return False, msg
        sett_currency = sett_currency_dict[self.cid]

        # 汇率
        key_tran_sett = Xutil.link_words(self.data_date, self.tran_currency, sett_currency)
        if key_tran_sett not in xe_exchange_dict:
            msg = "missing xe_exchange_rate: {}".format(key_tran_sett)
            return False, msg
        key_sett_rmb = Xutil.link_words(self.data_date, sett_currency, "CNY")
        if key_sett_rmb not in xe_exchange_dict:
            msg = "missing xe_exchange_rate: {}".format(key_sett_rmb)
            return False, msg
        tran_sett_rate = float(xe_exchange_dict[key_tran_sett])
        sett_rmb_rate = float(xe_exchange_dict[key_sett_rmb])

        # 金额转换
        sett_amount = tran_sett_rate * float(self.tran_amount)
        rmb_amount = sett_rmb_rate * sett_amount

        # 结果处理
        self.data_type = "HS"
        self.tran_sett_rate = tran_sett_rate
        self.sett_currency = sett_currency
        self.sett_amount = sett_amount
        self.sett_rmb_rate = sett_rmb_rate
        self.rmb_amount = rmb_amount
        return True, "SUCCESS"

    @staticmethod
    def batch_insert(db_sett: MySQLClient, data_month, data_list):
        sql = '''
            delete from db_mpay_income.t_bill_base_exchange_data where data_month = '{}'
        '''.format(data_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_income", "t_bill_base_exchange_data")

    @staticmethod
    def get_bill_base_exchange_rate_dict(db_sett: MySQLClient, data_month):
        sql = '''
            select data_type
                , data_month
                , ori_currency
                , dst_currency
                , exchange_rate
            from db_mpay_income.v_bill_base_exchange_rate
            where data_month = '{}'
        '''.format(data_month)
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            data_type = str(line["data_type"]).strip()
            data_month = str(line["data_month"]).strip()
            ori_currency = str(line["ori_currency"]).strip()
            dst_currency = str(line["dst_currency"]).strip()
            exchange_rate = float(line["exchange_rate"])

            data_dict[Xutil.link_words(data_type, data_month, ori_currency, ori_currency)] = 1.0
            data_dict[Xutil.link_words(data_type, data_month, ori_currency, dst_currency)] = exchange_rate
        # end for
        data_dict[Xutil.link_words("HS", data_month, "USD", "USD")] = 1.0
        data_dict[Xutil.link_words("HS", data_month, "CNY", "CNY")] = 1.0
        return data_dict

    @staticmethod
    def get_bill_base_exchange_rate_list(db_sett: MySQLClient, data_month):
        sql = '''
            select data_type
                , data_month
                , ori_currency
                , dst_currency
                , exchange_rate
            from db_mpay_income.v_bill_base_exchange_rate
            where data_month = '{}'
        '''.format(data_month)
        db_ret = db_sett.query(sql)
        data_list = db_ret.data
        return data_list

    @staticmethod
    def get_tdw_data(db_sett: MySQLClient, data_month):
        data_moth6 = str(data_month).replace("-", "")[0:6]
        sql = '''
            select data_date
                , data_month
                , channel
                , cid
                , mcid
                , merchant_id
                , sub_merchant_id
                , tran_type
                , pay_currency as tran_currency
                , sum(pay_amount) as tran_amount
            from db_tdw_data.t_ssb_midaspay_sum
            where data_month = '{}' and check_result = 'SUCCESS'
            group by data_date, data_month, channel, merchant_id
                , sub_merchant_id, tran_type, pay_currency
        '''.format(data_moth6)
        db_ret = db_sett.query(sql, cls=BillBaseExchangeData)
        data_list: List[BillBaseExchangeData] = db_ret.data
        return data_list

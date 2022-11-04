"""
    渠道账单-BASE表
"""
from typing import List, Dict
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient


class BillSettlementBaseData(BaseBean):
    def __init__(self):
        self.uniq_no = ''
        self.bill_type = ''
        self.bill_month = ''
        self.sett_month = ''
        self.data_month = ''
        self.data_date = ''
        self.due_month = ''
        self.due_date = ''
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
        self.tran_type = ''
        self.tran_currency = ''
        self.tran_amount = 0.0
        self.tran_numbers = 0.0
        self.ori_currency = ''
        self.ori_income = 0.0
        self.ori_refund = 0.0
        self.ori_channel_tax = 0.0
        self.ori_channel_fee = 0.0
        self.ori_channel_settlement = 0.0
        self.sett_currency = ''
        self.remark = ''
        self.special_note = ''

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, channel, data_list):
        sql = '''
            delete from db_mpay_channel.t_bill_settlement_base
            where sett_month = '{}' and channel = '{}'
        '''.format(sett_month, channel)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_channel", "t_bill_settlement_base")

    @staticmethod
    def get_settlement_base_list(db_sett: MySQLClient, sett_month):
        sql = '''
            select * from db_mpay_channel.t_bill_settlement_base where sett_month = '{}'
        '''.format(sett_month)
        db_ret = db_sett.query(sql, cls=BillSettlementBaseData)
        data_list: List[BillSettlementBaseData] = db_ret.data
        return data_list

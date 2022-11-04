"""
    账单报表：BOSS账单，平台费 + 内部商户收入
    db_mpay_income.t_boss_channel_bill
"""
from typing import List

from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import PltBillReportData


class BossBillReportData(BaseBean):
    def __init__(self):
        self.Fbill_type = ''
        self.Fsett_month = ''
        self.Fbill_month = ''
        self.Fchannel_id = ''
        self.Fchannel_name = ''
        self.Fsubchannel_id = ''
        self.Fsubchannel_name = ''
        self.Fsett_type = ''
        self.Fbilling_type = ''
        self.Fmerchant_type = ''
        self.Fmdm_id = ''
        self.Fmdm_name = ''
        self.Fbiz_customer_no = ''
        self.Fbiz_customer_name = ''
        self.Fcountry = ''
        self.Fou_id = ''
        self.Fou_name = ''
        self.Fspoa_id = ''
        self.Fspoa_name = ''
        self.Fsett_group = ''
        self.Fsett_group_name = ''
        self.Fbusi_group = ''
        self.Fbusi_group_name = ''
        self.Fdept = ''
        self.Fdept_name = ''
        self.Foriginal_currency_type = ''
        self.Foriginal_income = 0.0
        self.Foriginal_tax_rate = 0.0
        self.Foriginal_tax = 0.0
        self.Forigina_work_cost_rate = 0.0
        self.Foriginal_work_cost = 0.0
        self.Foriginal_refund = 0.0
        self.Foriginal_loss = 0.0
        self.Foriginal_divide = 0.0
        self.Foriginal_sett_fee = 0.0
        self.Fsettlement_currency_type = ''
        self.Forigina_settlement_currency_rate = 0.0
        self.Fsettlement_income = 0.0
        self.Fsettlement_work_cost = 0.0
        self.Fsettlement_refund = 0.0
        self.Fsettlement_loss = 0.0
        self.Fsettlement_divide = 0.0
        self.Fsettlement_sett_fee = 0.0
        self.Fsettlement_rmb_currency_rate = 0.0
        self.Frmb_income = 0.0
        self.Frmb_work_cost = 0.0
        self.Frmb_refund = 0.0
        self.Frmb_loss = 0.0
        self.Frmb_divide = 0.0
        self.Frmb_sett_fee = 0.0
        self.Fims_channel_id = ''
        self.Fims_channel_name = ''
        self.Fims_region = ''
        self.Ffusion_ou_id = ''
        self.Fboss_no = ''
        self.Fcontract_no = ''

    def cal_plt_bill(self, bill_data: PltBillReportData):
        self.Fbill_type = "PLATFORM"
        self.Fsett_month = bill_data.Fsett_month
        self.Fbill_month = bill_data.Fbill_month
        self.Fchannel_id = ''
        self.Fchannel_name = bill_data.Fchannel_name
        self.Fsubchannel_id = ''
        self.Fsubchannel_name = bill_data.Fsubchannel_name
        self.Fsett_type = ''
        self.Fbilling_type = bill_data.Fbilling_type
        self.Fmerchant_type = bill_data.Fmerchant_type
        self.Fmdm_id = bill_data.Fmdm_id
        self.Fmdm_name = bill_data.Fmdm_name
        self.Fbiz_customer_no = bill_data.Fbiz_customer_no
        self.Fbiz_customer_name = bill_data.Fbiz_customer_name
        self.Fcountry = bill_data.Fcountry
        self.Fou_id = bill_data.Fou_id
        self.Fou_name = bill_data.Fou_name
        self.Fspoa_id = bill_data.Fspoa_id
        self.Fspoa_name = bill_data.Fspoa_name
        self.Fsett_group = bill_data.Fsett_group
        self.Fsett_group_name = bill_data.Fsett_group_name
        self.Fbusi_group = bill_data.Fbusi_group
        self.Fbusi_group_name = bill_data.Fbusi_group_name
        self.Fdept = bill_data.Fdept
        self.Fdept_name = bill_data.Fdept_name
        self.Foriginal_currency_type = bill_data.Fori_currency
        self.Foriginal_income = bill_data.Fori_income
        self.Foriginal_refund = bill_data.Fori_refund
        self.Foriginal_tax = bill_data.Fori_tax
        self.Foriginal_work_cost = bill_data.Fori_channel_amount
        self.Foriginal_loss = bill_data.Fori_tax
        self.Foriginal_divide = 0.0
        self.Foriginal_sett_fee = bill_data.Fori_settlement
        self.Fsettlement_currency_type = bill_data.Fsett_currency
        self.Forigina_settlement_currency_rate = bill_data.Fori_sett_currency_rate
        self.Fsettlement_income = bill_data.Fsett_income
        self.Fsettlement_refund = bill_data.Fsett_refund
        self.Fsettlement_work_cost = bill_data.Fsett_channel_amount
        self.Fsettlement_loss = bill_data.Fsett_tax
        self.Fsettlement_divide = 0.0
        self.Fsettlement_sett_fee = bill_data.Fsett_settlement
        self.Fsettlement_rmb_currency_rate = bill_data.Fsett_rmb_currency_rate
        self.Frmb_income = bill_data.Frmb_income
        self.Frmb_refund = bill_data.Frmb_refund
        self.Frmb_work_cost = bill_data.Frmb_channel_amount
        self.Frmb_loss = bill_data.Frmb_tax
        self.Frmb_divide = 0.0
        self.Frmb_sett_fee = bill_data.Frmb_settlement
        self.Fims_channel_id = ''
        self.Fims_channel_name = ''
        self.Fims_region = ''
        self.Ffusion_ou_id = ''
        self.Fboss_no = ''
        self.Fcontract_no = ''

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, bill_type, data_list):
        sql = '''
            delete from db_mpay_income.t_boss_channel_bill 
            where Fsett_month = '{}' and Fbill_type = '{}'
        '''.format(sett_month, bill_type)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_income", "t_boss_channel_bill")

    @staticmethod
    def get_bill_list(db_sett: MySQLClient, sett_month):
        sql = '''
            select * from db_mpay_income.t_boss_channel_bill where Fsett_month = '{}'
        '''.format(sett_month)
        db_ret = db_sett.query(sql, cls=BossBillReportData)
        data_list: List[BossBillReportData] = db_ret.data
        return data_list


if __name__ == '__main__':
    pass

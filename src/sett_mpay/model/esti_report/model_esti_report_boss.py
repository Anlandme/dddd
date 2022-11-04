"""
    暂估报表：BOSS账单，平台费 + 内部商户收入
    db_mpay_income.t_boss_channel_esti
"""
from typing import List

from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import PltEstiReportData


class BossEstiReportData(BaseBean):
    def __init__(self):
        self.Fbill_type = ''
        self.Fsett_month = ''
        self.Fsett_day = ''
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
        self.Foriginal_work_cost_rate = 0.0
        self.Foriginal_work_cost = 0.0
        self.Foriginal_refund = 0.0
        self.Foriginal_loss = 0.0
        self.Foriginal_divide = 0.0
        self.Foriginal_sett_fee = 0.0
        self.Fsettlement_currency_type = ''
        self.Foriginal_settlement_currency_rate = 0.0
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

    def cal_plt_bill(self, plt_data: PltEstiReportData):
        self.Fbill_type = "PLATFORM"
        self.Fsett_month = plt_data.Fsett_month
        self.Fsett_day = plt_data.Fdata_date
        self.Fbill_month = plt_data.Fbill_month
        self.Fchannel_id = ''
        self.Fchannel_name = plt_data.Fchannel_name
        self.Fsubchannel_id = ''
        self.Fsubchannel_name = plt_data.Fsubchannel_name
        self.Fsett_type = ''
        self.Fbilling_type = plt_data.Fbilling_type
        self.Fmerchant_type = plt_data.Fmerchant_type
        self.Fmdm_id = plt_data.Fmdm_id
        self.Fmdm_name = plt_data.Fmdm_name
        self.Fbiz_customer_no = plt_data.Fbiz_customer_no
        self.Fbiz_customer_name = plt_data.Fbiz_customer_name
        self.Fcountry = plt_data.Fcountry
        self.Fou_id = plt_data.Fou_id
        self.Fou_name = plt_data.Fou_name
        self.Fspoa_id = plt_data.Fspoa_id
        self.Fspoa_name = plt_data.Fspoa_name
        self.Fsett_group = plt_data.Fsett_group
        self.Fsett_group_name = plt_data.Fsett_group_name
        self.Fbusi_group = plt_data.Fbusi_group
        self.Fbusi_group_name = plt_data.Fbusi_group_name
        self.Fdept = plt_data.Fdept
        self.Fdept_name = plt_data.Fdept_name
        self.Foriginal_currency_type = plt_data.Fori_currency
        self.Foriginal_income = plt_data.Fori_income
        self.Foriginal_refund = plt_data.Fori_refund
        self.Foriginal_tax = plt_data.Fori_tax
        self.Foriginal_work_cost = plt_data.Fori_channel_amount
        self.Foriginal_loss = plt_data.Fori_tax
        self.Foriginal_divide = 0.0
        self.Foriginal_sett_fee = plt_data.Fori_settlement
        self.Fsettlement_currency_type = plt_data.Fsett_currency
        self.Foriginal_settlement_currency_rate = plt_data.Fori_sett_currency_rate
        self.Fsettlement_income = plt_data.Fsett_income
        self.Fsettlement_refund = plt_data.Fsett_refund
        self.Fsettlement_work_cost = plt_data.Fsett_channel_amount
        self.Fsettlement_loss = plt_data.Fsett_tax
        self.Fsettlement_divide = 0.0
        self.Fsettlement_sett_fee = plt_data.Fsett_settlement
        self.Fsettlement_rmb_currency_rate = plt_data.Fsett_rmb_currency_rate
        self.Frmb_income = plt_data.Frmb_income
        self.Frmb_refund = plt_data.Frmb_refund
        self.Frmb_work_cost = plt_data.Frmb_channel_amount
        self.Frmb_loss = plt_data.Frmb_tax
        self.Frmb_divide = 0.0
        self.Frmb_sett_fee = plt_data.Frmb_settlement
        self.Fims_channel_id = ''
        self.Fims_channel_name = ''
        self.Fims_region = ''
        self.Ffusion_ou_id = ''
        self.Fboss_no = ''
        self.Fcontract_no = ''

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, bill_type, data_list):
        sql = '''
            delete from db_mpay_income.t_boss_channel_esti 
            where Fsett_month = '{}' and Fbill_type = '{}'
        '''.format(sett_month, bill_type)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_income", "t_boss_channel_esti")

    @staticmethod
    def get_bill_list(db_sett: MySQLClient, sett_month):
        sql = '''
            select * from db_mpay_income.t_boss_channel_esti where Fsett_month = '{}'
        '''.format(sett_month)
        db_ret = db_sett.query(sql, cls=BossEstiReportData)
        data_list: List[BossEstiReportData] = db_ret.data
        return data_list


if __name__ == '__main__':
    pass

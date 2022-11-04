"""
    成本确认报表
"""
from src import List
from src import BaseBean
from src import MySQLClient
from src import MerchantBillBaseData


class CostConfirmData(BaseBean):
    def __init__(self):
        self.Fsett_month = ''
        self.Fbill_month = ''
        self.Fchannel_id = ''
        self.Fchannel_name = ''
        self.Fchannel_ims = ''
        self.Fsubchannel_id = ''
        self.Fsubchannel_name = ''
        self.Fsett_type = ''
        self.Fbilling_type = ''
        self.Fmdm_id = ''
        self.Fmdm_name = ''
        self.Fbiz_customer_no = ''
        self.Fbiz_customer_name = ''
        self.Fmerchant_type = ''
        self.Ficp_code = ''
        self.Ficp_name = ''
        self.Fcoa_product_no = ''
        self.Fcoa_product_name = ''
        self.Fou_id = ''
        self.Fou_name = ''
        self.Fou_name_short = ''
        self.Foffer_id = ''
        self.Foffer_name = ''
        self.Fproduct_no = ''
        self.Fproduct_name = ''
        self.Fspoa_id = ''
        self.Fspoa_name = ''
        self.Fsett_group = ''
        self.Fsett_group_name = ''
        self.Fbusi_group = ''
        self.Fbusi_group_name = ''
        self.Fdept = ''
        self.Fdept_name = ''
        self.Fcountry = ''
        self.Fori_currency = ''
        self.Fori_income = 0.0
        self.Fori_refund = 0.0
        self.Fori_plt_rate = 0.0
        self.Fori_plt_amount = 0.0
        self.Fori_tax_rate = 0.0
        self.Fori_tax = 0.0
        self.Fori_channel_rate = 0.0
        self.Fori_channel_amount = 0.0
        self.Fori_settlement = 0.0
        self.Fori_sett_currency_rate = 0.0
        self.Fsett_currency = ''
        self.Fsett_income = 0.0
        self.Fsett_refund = 0.0
        self.Fsett_plt_amount = 0.0
        self.Fsett_tax = 0.0
        self.Fsett_channel_amount = 0.0
        self.Fsett_settlement = 0.0
        self.Fsett_rmb_currency_rate = 0.0
        self.Frmb_income = 0.0
        self.Frmb_refund = 0.0
        self.Frmb_plt_amount = 0.0
        self.Frmb_tax = 0.0
        self.Frmb_channel_amount = 0.0
        self.Frmb_settlement = 0.0
        self.Fchannel_contract_no = ''
        self.Fmerchant_contract_no = ''
        self.Fdata_source_no = ''
        self.Fdata_source_name = ''
        self.Fapproval_status = ''
        self.Fapproval_reason = ''

    def update_merchant_bill(self, base_data: MerchantBillBaseData):
        self.Fsett_month = base_data.sett_month
        self.Fbill_month = base_data.bill_month
        self.Fchannel_name = base_data.channel
        self.Fsubchannel_name = base_data.sub_channel
        self.Fmdm_id = '72334889'
        self.Fmdm_name = '虚拟-增值电信-Midaspay支付'
        self.Fbiz_customer_no = base_data.merchant_mdm_id
        self.Fbiz_customer_name = base_data.merchant_mdm_name
        self.Fmerchant_type = base_data.merchant_type
        self.Fcoa_product_no = base_data.merchant_coa_no
        self.Fcoa_product_name = base_data.merchant_coa_name
        self.Fou_id = base_data.merchant_ou_id
        self.Fou_name = base_data.merchant_ou_name
        self.Fou_name_short = base_data.merchant_ou_short
        self.Fproduct_no = base_data.merchant_id
        self.Fproduct_name = base_data.merchant_name
        self.Fcountry = base_data.channel_country_code
        self.Fori_currency = base_data.ori_currency
        self.Fori_income = base_data.ori_income
        self.Fori_refund = base_data.ori_refund
        self.Fori_plt_amount = base_data.ori_plt_fee
        self.Fori_settlement = base_data.ori_plt_fee
        self.Fori_sett_currency_rate = base_data.ori_sett_currency_rate
        self.Fsett_currency = base_data.sett_currency
        self.Fsett_income = base_data.sett_income
        self.Fsett_refund = base_data.sett_refund
        self.Fsett_plt_amount = base_data.sett_plt_fee
        self.Fsett_settlement = base_data.sett_plt_fee
        self.Fsett_rmb_currency_rate = base_data.sett_rmb_currency_rate
        self.Frmb_income = base_data.rmb_income
        self.Frmb_refund = base_data.rmb_refund
        self.Frmb_plt_amount = base_data.rmb_plt_fee
        self.Frmb_settlement = base_data.rmb_plt_fee
        self.Fchannel_contract_no = base_data.channel_contract_no
        self.Fmerchant_contract_no = base_data.merchant_contract_no

    @staticmethod
    def get_data_list(db_sett: MySQLClient, sett_month, approval_status='3'):
        sql = '''
            select * 
            from db_sett_oversea.t_merchant_internal_cost_bill
            where Fsett_month = '{}' and Fapproval_status = '{}'
        '''.format(sett_month, approval_status)
        db_ret = db_sett.query(sql, cls=CostConfirmData)
        data_list: List[CostConfirmData] = db_ret.data
        return data_list

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, data_list):
        sql = '''
            delete from db_sett_oversea.t_merchant_internal_cost_bill where Fsett_month = '{}'
        '''.format(sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea", "t_merchant_internal_cost_bill")


if __name__ == '__main__':
    pass

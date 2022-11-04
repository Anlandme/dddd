"""
    账单报表：代收付
    db_sett_oversea.t_channel_month_agency_bill
"""
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import SpoaInfoData
from src import MerchantBillBaseData


class AgencyBillReportData(BaseBean):
    def __init__(self):
        self.Fsett_month = ''
        self.Fbill_month = ''
        self.Fdue_month = ''
        self.Fdue_date = ''
        self.Fchannel_id = ''
        self.Fchannel_name = ''
        self.Fchannel_ims = ''
        self.Fsubchannel_id = ''
        self.Fsubchannel_name = ''
        self.Fsett_type = ''
        self.Fbilling_type = ''
        self.Fmdm_id = ''
        self.Fmdm_name = ''
        self.Fchannel_mdm_id = ''
        self.Fchannel_mdm_name = ''
        self.Fbiz_customer_no = ''
        self.Fbiz_customer_name = ''
        self.Fmerchant_type = ''
        self.Fmerchant_mdm_id = ''
        self.Fmerchant_mdm_name = ''
        self.Ficp_code = ''
        self.Ficp_name = ''
        self.Fou_id = ''
        self.Fou_name = ''
        self.Fou_name_short = ''
        self.Fproduct_no = ''
        self.Fproduct_name = ''
        self.Foffer_id = ''
        self.Foffer_name = ''
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
        self.Fori_plt_rate = 0.0
        self.Fori_plt_amount = 0.0
        self.Fori_tax_rate = 0.0
        self.Fori_tax = 0.0
        self.Fori_plt_tax_rate = 0.0
        self.Fori_plt_tax = 0.0
        self.Fori_channel_tax_rate = 0.0
        self.Fori_channel_tax = 0.0
        self.Fori_channel_rate = 0.0
        self.Fori_channel_amount = 0.0
        self.Fori_refund = 0.0
        self.Fori_settlement = 0.0
        self.Fchannel_rule_type = ''
        self.Fori_channel_fee_total = 0.0
        self.Fori_channel_percent_fee_rate = 0.0
        self.Fori_channel_percent_fee_total = 0.0
        self.Fori_channel_per_transaction_fee = 0.0
        self.Fori_channel_per_transaction_fee_total = 0.0
        self.Fori_channel_per_transaction_min_fee = 0.0
        self.Fori_channel_per_transaction_min_fee_total = 0.0
        self.Fori_channel_installment_fee_rate = 0.0
        self.Fori_channel_installment_fee_total = 0.0
        self.Fori_channel_ot_fee_total = 0.0
        self.Fmerchant_rule_type = ''
        self.Fori_merchant_fee_total = 0.0
        self.Fori_merchant_percent_fee_rate = 0.0
        self.Fori_merchant_percent_fee_total = 0.0
        self.Fori_merchant_per_transaction_fee = 0.0
        self.Fori_merchant_per_transaction_fee_total = 0.0
        self.Fori_merchant_per_transaction_min_fee = 0.0
        self.Fori_merchant_per_transaction_min_fee_total = 0.0
        self.Fori_merchant_installment_fee_rate = 0.0
        self.Fori_merchant_installment_fee_total = 0.0
        self.Fori_merchant_ot_fee_total = 0.0
        self.Fori_plt_fee_total = 0.0
        self.Fori_sett_currency_rate = 0.0
        self.Fsett_currency = ''
        self.Fsett_income = 0.0
        self.Fsett_plt_amount = 0.0
        self.Fsett_tax = 0.0
        self.Fsett_plt_tax = 0.0
        self.Fsett_channel_tax = 0.0
        self.Fsett_channel_amount = 0.0
        self.Fsett_refund = 0.0
        self.Fsett_settlement = 0.0
        self.Fsett_rmb_currency_rate = 0.0
        self.Frmb_income = 0.0
        self.Frmb_plt_amount = 0.0
        self.Frmb_tax = 0.0
        self.Frmb_plt_tax = 0.0
        self.Frmb_channel_tax = 0.0
        self.Frmb_channel_amount = 0.0
        self.Frmb_refund = 0.0
        self.Frmb_settlement = 0.0
        self.Fims_channel_id = ''
        self.Fims_channel_name = ''
        self.Fcontract_no = ''
        self.Fchannel_contract_no = ''
        self.Fmerchant_contract_no = ''
        self.Fdata_source_no = ''
        self.Fdata_source_name = ''

    def update_merchant_base_bill(self, base_bill: MerchantBillBaseData):
        spoa_pay = SpoaInfoData.get_spoa_pay()
        ori_settlement = base_bill.ori_income - base_bill.ori_refund - \
                         base_bill.ori_channel_tax - base_bill.ori_channel_fee - base_bill.ori_plt_fee
        sett_settlement = base_bill.sett_income - base_bill.sett_refund - \
                          base_bill.sett_channel_tax - base_bill.sett_channel_fee - base_bill.sett_plt_fee
        rmb_settlement = base_bill.rmb_income - base_bill.rmb_refund - \
                         base_bill.rmb_channel_tax - base_bill.rmb_channel_fee - base_bill.rmb_plt_fee

        self.Fsett_month = base_bill.sett_month
        self.Fbill_month = base_bill.bill_month
        self.Fdue_month = base_bill.due_month
        self.Fdue_date = base_bill.due_date
        self.Fchannel_id = ''
        self.Fchannel_name = base_bill.channel
        self.Fchannel_ims = ''
        self.Fsubchannel_id = ''
        self.Fsubchannel_name = base_bill.sub_channel
        self.Fsett_type = ''
        self.Fbilling_type = "MidasPay"
        self.Fmdm_id = base_bill.channel_mdm_id
        self.Fmdm_name = base_bill.channel_mdm_name
        self.Fchannel_mdm_id = base_bill.channel_mdm_id
        self.Fchannel_mdm_name = base_bill.channel_mdm_name
        self.Fbiz_customer_no = base_bill.merchant_mdm_id
        self.Fbiz_customer_name = base_bill.merchant_mdm_name
        self.Fmerchant_type = base_bill.merchant_type
        self.Fmerchant_mdm_id = base_bill.merchant_mdm_id
        self.Fmerchant_mdm_name = base_bill.merchant_mdm_name
        self.Ficp_code = ''
        self.Ficp_name = ''
        self.Fou_id = base_bill.plt_ou_id
        self.Fou_name = base_bill.plt_ou_name
        self.Fou_name_short = base_bill.plt_ou_short
        self.Fproduct_no = base_bill.product_no
        self.Fproduct_name = base_bill.product_name
        self.Foffer_id = ''
        self.Foffer_name = ''
        self.Fspoa_id = spoa_pay.spoa_id
        self.Fspoa_name = spoa_pay.spoa_name
        self.Fsett_group = spoa_pay.sett_group
        self.Fsett_group_name = spoa_pay.sett_group_name
        self.Fbusi_group = spoa_pay.busi_group
        self.Fbusi_group_name = spoa_pay.busi_group_name
        self.Fdept = spoa_pay.dept
        self.Fdept_name = spoa_pay.dept_name
        self.Fcountry = base_bill.channel_country_code

        self.Fori_currency = base_bill.ori_currency
        self.Fori_income = base_bill.ori_income
        self.Fori_refund = base_bill.ori_refund
        self.Fori_tax = base_bill.ori_channel_tax
        self.Fori_plt_tax = 0.0
        self.Fori_channel_tax = base_bill.ori_channel_tax
        self.Fori_channel_amount = base_bill.ori_channel_fee
        self.Fori_plt_amount = base_bill.ori_plt_fee
        self.Fori_settlement = ori_settlement
        self.Fori_sett_currency_rate = base_bill.ori_sett_currency_rate

        self.Fsett_currency = base_bill.sett_currency
        self.Fsett_income = base_bill.sett_income
        self.Fsett_refund = base_bill.sett_refund
        self.Fsett_tax = base_bill.sett_channel_tax
        self.Fsett_plt_tax = 0.0
        self.Fsett_channel_tax = base_bill.sett_channel_tax
        self.Fsett_channel_amount = base_bill.sett_channel_fee
        self.Fsett_plt_amount = base_bill.sett_plt_fee
        self.Fsett_settlement = sett_settlement
        self.Fsett_rmb_currency_rate = base_bill.sett_rmb_currency_rate

        self.Frmb_income = base_bill.rmb_income
        self.Frmb_refund = base_bill.rmb_refund
        self.Frmb_tax = base_bill.rmb_channel_tax
        self.Frmb_plt_tax = 0.0
        self.Frmb_channel_tax = base_bill.rmb_channel_tax
        self.Frmb_channel_amount = base_bill.rmb_channel_fee
        self.Frmb_plt_amount = base_bill.rmb_plt_fee
        self.Frmb_settlement = rmb_settlement
        self.Fims_channel_id = '0939'
        self.Fims_channel_name = 'Midas-代收代付'
        self.Fchannel_contract_no = base_bill.channel_contract_no
        self.Fmerchant_contract_no = base_bill.merchant_contract_no

    @staticmethod
    def batch_insert(db_sett: MySQLClient, sett_month, data_list):
        sql = '''
            delete from db_sett_oversea.t_channel_month_agency_bill where Fsett_month = '{}'
        '''.format(sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea", "t_channel_month_agency_bill")


if __name__ == '__main__':
    pass

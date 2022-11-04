"""
    成本预提报表
"""
from src import List
from src import BaseBean
from src import MySQLClient


class CostWithholdingData(BaseBean):
    def __init__(self):
        self.Fsett_month = ''
        self.Fwithholding_type = ''
        self.Fproduct_no = ''
        self.Fproduct_name = ''
        self.Fcompany_no = ''
        self.Fcompany_name = ''
        self.Fcostcenter_no = ''
        self.Fcostcenter_name = ''
        self.Faccount_no = ''
        self.Faccount_name = ''
        self.Fsubaccount_no = ''
        self.Fsubaccount_name = ''
        self.Fcoa_product_no = ''
        self.Fcoa_product_name = ''
        self.Ficp_no = ''       # 废弃
        self.Ficp_name = ''     # 废弃
        self.Fdrawing_account_bases = ''
        self.Fvendor_name = ''  # 供应商
        self.Fcurrency = ''
        self.Fperiod_name = ''
        self.Fda_period_name = ''
        self.Fprepay_month = ''
        self.Fdept_name = ''
        self.Fcontract_no = ''
        self.Ffinance_people = ''
        self.Ffinance_people_id = ''
        self.Fdrawing_account_amount = 0  # 预提金额
        self.Fannotations = ''    # 备注
        self.Fsource_id = ''      # 系统编号
        self.Fsystem_pk_id = ''   # 防重编号
        self.Fdata_source = ''

    @staticmethod
    def get_data_list(db_sett: MySQLClient, sett_month):
        sql = '''
            select * 
            from db_sett_oversea.t_merchant_internal_cost
            where Fsett_month = '{}'
        '''.format(sett_month)
        db_ret = db_sett.query(sql, cls=CostWithholdingData)
        data_list: List[CostWithholdingData] = db_ret.data
        return data_list


if __name__ == '__main__':
    pass

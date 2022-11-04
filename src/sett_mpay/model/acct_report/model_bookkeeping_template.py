"""
    记账模版
    db_sett_oversea.t_bookkeeping_template
"""
from typing import List
from src import BaseBean
from src import MySQLClient


class BookkeepingTemplateData(BaseBean):
    def __init__(self):
        self.template_no = ''
        self.template_name = ''
        self.template_type = ''
        self.period_type = ''
        self.voucher_type = ''
        self.org_name = ''
        self.business_category = ''
        self.business_type = ''
        self.dr_cost_center_no = ''
        self.dr_cost_center_name = ''
        self.dr_account_no = ''
        self.dr_account_name = ''
        self.dr_product_no = ''
        self.dr_product_name = ''
        self.cr_cost_center_no = ''
        self.cr_cost_center_name = ''
        self.cr_account_no = ''
        self.cr_account_name = ''
        self.cr_product_no = ''
        self.cr_product_name = ''
        self.mdm_id = ''
        self.mdm_name = ''
        self.status = ''

    @staticmethod
    def get_bookkeeping_template_dict(db_sett: MySQLClient, template_no=None, template_type=None, period_type=None):
        sql = '''
            select * 
            from db_gss_config.t_bookkeeping_template
            where status = 'Y'
        '''
        if template_no:
            sql += " and template_no = '{}'".format(template_no)
        if template_type:
            sql += " and template_type = '{}'".format(template_type)
        if period_type:
            sql += " and period_type = '{}'".format(period_type)
        db_ret = db_sett.query(sql, cls=BookkeepingTemplateData)
        data_list: List[BookkeepingTemplateData] = db_ret.data

        data_dict = {}
        for data in data_list:
            data_dict[data.template_no] = data
        # end for
        return data_dict


def import_template():
    from src import ExcelUtil, db_sett
    file_path = "./JM账务模版-Midas配置表.xlsx"
    field_list = [
        'template_no', 'template_name', 'template_type', 'voucher_type', 'org_name', 'business_category',
        'business_type', 'dr_cost_center_name', 'dr_cost_center_no', 'dr_account_name', 'dr_account_no',
        'dr_product_name', 'dr_product_no', 'cr_cost_center_name', 'cr_cost_center_no', 'cr_account_name',
        'cr_account_no', 'cr_product_name', 'cr_product_no', 'mdm_id', 'mdm_name', 'status'
    ]
    file_content = ExcelUtil.read_excel_xlrd(file_path, field_list, sheet_name="config")

    data_list = []
    for line in file_content:
        if str(line["template_no"]).startswith("BP"):
            data_list.append(line)
    # end for

    # save data
    sql = '''
        delete from db_gss_config.t_bookkeeping_template 
    '''
    db_sett.update(sql)
    db_sett.batch_insert(data_list, "db_gss_config", "t_bookkeeping_template")


if __name__ == '__main__':
    import_template()
    pass

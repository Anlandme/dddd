"""
    记账凭证表
    db_sett_oversea.t_bookkeeping_voucher
"""
import random
import datetime
from src import MySQLClient
from src import BookkeepingTemplateData


class BookkeepingVoucherData(object):
    def __init__(self):
        self.seq_no = 0              # 序号
        self.voucher_no = ''         # 凭证编号
        self.voucher_type = ''       # 凭证类型：集团、米大师
        self.bookkeeping_date = ''
        self.bookkeeping_period = ''
        self.sett_currency = ""
        self.sett_amount_dr = 0
        self.sett_amount_cr = 0

        # 模版信息
        self.process_no = ''         # 模版编号
        self.process_name = ''       # 模版名称
        self.finance_type = ''       # 模版类型：AR、AP
        self.ou_id = ''              # 入账主体OU ID
        self.ou_name = ''            # 入账主体OU名称
        self.org_name = ''           # 入账主体机构名称

        self.business_category = ''  # JM大类
        self.business_type = ''      # JM小类
        self.dr_cost_center_no = ''  # DR 成本中心编号
        self.dr_cost_center_name = ''     # DR 成本中心名称
        self.dr_account_no = ''      # DR 科目编号
        self.dr_account_name = ''         # DR 科目名称
        self.dr_product_no = ''      # DR COA产品编号
        self.dr_product_name = ''         # DR COA产品名称
        self.cr_cost_center_no = ''  # CR 成本中心编号
        self.cr_cost_center_name = ''     # CR 成本中心名称
        self.cr_account_no = ''      # CR 科目编号
        self.cr_account_name = ''         # CR 科目名称
        self.cr_product_no = ''      # CR COA产品编号
        self.cr_product_name = ''         # CR COA产品名称
        self.mdm_id = ''             # 客户MDM ID
        self.mdm_name = ''           # 客户MDM名称

        # 冗余信息
        self.sett_month = ''
        self.data_month = ''
        self.bill_month = ''
        self.defer_month = ''
        self.offer_id = ''     # NEW 202205
        self.offer_name = ''   # NEW 202205
        self.product_id = ''
        self.product_name = ''
        self.channel_mdm_id = ''
        self.channel_mdm_name = ''
        self.channel_contract_no = ''
        self.merchant_type = ''
        self.merchant_mdm_id = ''
        self.merchant_mdm_name = ''
        self.merchant_contract_no = ''
        self.biz_type = "代收付业务"
        self.operate_type = "INIT"
        self.bookkeeper = "System"
        self.reviewer = "System"
        self.data_source_no = ''

        # 状态
        self.approval_status = ''
        self.approval_reason = ''
        self.charge_off_status = ''
        self.charge_off_date = ''   # NEW 202205
        self.jm_status = ''         # NEW 202205
        self.jm_date = ''           # NEW 202205

        # 废弃（兼容前台数据展示）
        self.account_dr = ''
        self.account_cr = ''
        self.abstract = ''

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    def update_template_info(self, template_info: BookkeepingTemplateData):
        self.voucher_no = BookkeepingVoucherData.get_voucher_no_v2()
        self.process_no = template_info.template_no
        self.process_name = template_info.template_name
        self.finance_type = template_info.template_type
        self.voucher_type = template_info.voucher_type
        self.org_name = template_info.org_name
        self.business_category = template_info.business_category
        self.business_type = template_info.business_type
        self.dr_cost_center_no = template_info.dr_cost_center_no
        self.dr_cost_center_name = template_info.dr_cost_center_name
        self.dr_account_no = template_info.dr_account_no
        self.dr_account_name = template_info.dr_account_name
        self.dr_product_no = template_info.dr_product_no
        self.dr_product_name = template_info.dr_product_name
        self.cr_cost_center_no = template_info.cr_cost_center_no
        self.cr_cost_center_name = template_info.cr_cost_center_name
        self.cr_account_no = template_info.cr_account_no
        self.cr_account_name = template_info.cr_account_name
        self.cr_product_no = template_info.cr_product_no
        self.cr_product_name = template_info.cr_product_name
        self.mdm_id = template_info.mdm_id
        self.mdm_name = template_info.mdm_name

        # 兼容前台展示
        self.account_dr = template_info.dr_account_name
        self.account_cr = template_info.cr_account_name
        self.abstract = template_info.template_name

    @staticmethod
    def get_max_seq_no(db_sett):
        sql = '''
            select max(seq_no) as max_no from db_sett_oversea.t_bookkeeping_voucher
        '''
        db_ret = db_sett.query(sql)

        if db_ret is None or db_ret.data is None:
            return 0
        if len(db_ret.data) != 1 or "max_no" not in db_ret.data[0]:
            return 0

        max_no = db_ret.data[0]["max_no"]
        if max_no is None:
            max_no = 0
        else:
            max_no = int(max_no)
        return max_no

    @staticmethod
    def get_voucher_no(seq_no):
        temp = "000000000000{}".format(str(seq_no))
        return "M{}".format(temp[-12:])

    @staticmethod
    def get_voucher_no_v2():
        # 毫秒级时间 + 2位随机
        dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        return "M{}{}".format(dt_ms, random.randint(10, 99))

    @staticmethod
    def update_voucher_no(db_sett: MySQLClient, bookkeeping_period):
        # get seq_no
        max_no = 0
        sql = '''
            select max(seq_no) as max_no from db_sett_oversea.t_bookkeeping_voucher where sett_month < '{}'
        '''.format(bookkeeping_period)
        db_ret = db_sett.query(sql)
        if db_ret.data and len(db_ret.data) == 1 and "max_no" in db_ret.data[0]:
            max_no = db_ret.data[0]["max_no"]
            if max_no is None:
                max_no = 1
            else:
                max_no = int(max_no)

        # get_data
        data_list = []
        sql = '''
                select id, seq_no, voucher_no, modify_time 
                from db_sett_oversea.t_bookkeeping_voucher 
                where sett_month = '{}'
            '''.format(bookkeeping_period)
        db_ret = db_sett.query(sql)
        for line in db_ret.data:
            max_no += 1
            line["seq_no"] = max_no
            line["voucher_no"] = BookkeepingVoucherData.get_voucher_no(max_no)
            data_list.append(line)
        # end for

        # update data
        for data in data_list:
            id = data["id"]
            seq_no = data["seq_no"]
            voucher_no = data["voucher_no"]
            sql = '''
                update db_sett_oversea.t_bookkeeping_voucher
                set seq_no = '{}', voucher_no = '{}'
                where id = '{}'
            '''.format(seq_no, voucher_no, id)
            db_sett.update(sql)
        # end for


if __name__ == '__main__':
    pass

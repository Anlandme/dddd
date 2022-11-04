"""
    JM数据
    db_sett_oversea.t_bookkeeping_jm_midas
"""
from src import List
from src import Xutil
from src import BaseBean
from src import MySQLClient


class BookkeepingJMData(BaseBean):
    TEMPLATE_MAPPER = {
        "BP01001": {"template_type": "AR", "period_type": "ESTIMATE", "desc": "【流水期间】代收-暂估应收"}

        , "BP01012": {"template_type": "AR", "period_type": "WRITE_OFF", "desc": "【核销期间】代收-汇兑损益"}
        , "BP01013": {"template_type": "AR", "period_type": "WRITE_OFF", "desc": "【核销期间】代收-核销结果"}
        , "BP02008": {"template_type": "AP", "period_type": "WRITE_OFF", "desc": "【核销期间】应收应付互抵（内部商户）"}

        , "BP01004": {"template_type": "AR", "period_type": "BILL", "desc": "【账单期间】代收-暂估冲销"}
        , "BP01005": {"template_type": "AR", "period_type": "BILL", "desc": "【账单期间】代收-账单应收"}
        , "BP02007": {"template_type": "AP", "period_type": "BILL", "desc": "【账单期间】成本确认（内部商户）"}
        , "BP02017": {"template_type": "AP", "period_type": "BILL", "desc": "【账单期间】确认平台代缴税"}
    }

    def __init__(self):
        self.sett_month = ''
        self.data_month = ''
        self.template_no = ''
        self.template_name = ''
        self.template_type = ''
        self.org_name = ''
        self.business_category = ''
        self.business_type = ''
        self.period_name = ''
        self.ref_approver = ''
        self.dr_cost_center_no = ''
        self.dr_cost_center_name = ''
        self.dr_account_no = ''
        self.dr_account_name = ''
        self.dr_sub_account_no = ''
        self.dr_sub_account_name = ''
        self.dr_product_no = ''
        self.dr_product_name = ''
        self.cr_cost_center_no = ''
        self.cr_cost_center_name = ''
        self.cr_account_no = ''
        self.cr_account_name = ''
        self.cr_sub_account_no = ''
        self.cr_sub_account_name = ''
        self.cr_product_no = ''
        self.cr_product_name = ''
        self.mdm_id = ''
        self.mdm_name = ''
        self.transaction_amount = 0.0
        self.currency_code = ''
        self.source_system_pk_id = ''
        self.apply_reason = ''
        self.apply_remark = ''
        self.push_status = ''
        self.product_name = ''
        self.amount_symbol = ''

    @staticmethod
    def gen_jm_data_report(db_sett: MySQLClient, period, template_no, template_type):
        if template_type == "AP":
            # AP 区分产品
            sql = '''
                select data_month
                    , bookkeeping_period as period_name
                    , process_no as template_no
                    , process_name as template_name
                    , finance_type as template_type
                    , org_name
                    , business_category
                    , business_type
                    , dr_cost_center_no
                    , dr_cost_center_name
                    , dr_account_no
                    , dr_account_name
                    , dr_product_no
                    , dr_product_name
                    , cr_cost_center_no
                    , cr_cost_center_name
                    , cr_account_no
                    , cr_account_name
                    , cr_product_no
                    , cr_product_name
                    , mdm_id
                    , mdm_name
                    , product_name
                    , '+' as amount_symbol
                    , sett_currency as currency_code
                    , sum(sett_amount_dr) as transaction_amount
                from db_sett_oversea.t_bookkeeping_voucher
                where bookkeeping_period = '{period}' and process_no = '{template_no}' and sett_amount_dr > 0
                group by data_month, bookkeeping_period, process_no, process_name, finance_type, org_name
                    , business_category , business_type, dr_cost_center_no, dr_cost_center_name, dr_account_no
                    , dr_account_name, dr_product_no, dr_product_name, cr_cost_center_no, cr_cost_center_name
                    , cr_account_no, cr_account_name, cr_product_no, cr_product_name, mdm_id, mdm_name, sett_currency
                    , product_name

                union all
                select data_month
                    , bookkeeping_period as period_name
                    , process_no as template_no
                    , process_name as template_name
                    , finance_type as template_type
                    , org_name
                    , business_category
                    , business_type
                    , dr_cost_center_no
                    , dr_cost_center_name
                    , dr_account_no
                    , dr_account_name
                    , dr_product_no
                    , dr_product_name
                    , cr_cost_center_no
                    , cr_cost_center_name
                    , cr_account_no
                    , cr_account_name
                    , cr_product_no
                    , cr_product_name
                    , mdm_id
                    , mdm_name
                    , product_name
                    , '-' as amount_symbol
                    , sett_currency as currency_code
                    , sum(sett_amount_dr) as transaction_amount
                from db_sett_oversea.t_bookkeeping_voucher
                where bookkeeping_period = '{period}' and process_no = '{template_no}' and sett_amount_dr < 0
                group by data_month, bookkeeping_period, process_no, process_name, finance_type, org_name
                    , business_category , business_type, dr_cost_center_no, dr_cost_center_name, dr_account_no
                    , dr_account_name, dr_product_no, dr_product_name, cr_cost_center_no, cr_cost_center_name
                    , cr_account_no, cr_account_name, cr_product_no, cr_product_name, mdm_id, mdm_name, sett_currency
                    , product_name
            '''.format(period=period, template_no=template_no)
        else:
            # AR 不区分产品
            sql = '''
                select data_month
                    , bookkeeping_period as period_name
                    , process_no as template_no
                    , process_name as template_name
                    , finance_type as template_type
                    , org_name
                    , business_category
                    , business_type
                    , dr_cost_center_no
                    , dr_cost_center_name
                    , dr_account_no
                    , dr_account_name
                    , dr_product_no
                    , dr_product_name
                    , cr_cost_center_no
                    , cr_cost_center_name
                    , cr_account_no
                    , cr_account_name
                    , cr_product_no
                    , cr_product_name
                    , mdm_id
                    , mdm_name
                    , '' as product_name
                    , '+' as amount_symbol
                    , sett_currency as currency_code
                    , sum(sett_amount_dr) as transaction_amount
                from db_sett_oversea.t_bookkeeping_voucher
                where bookkeeping_period = '{period}' and process_no = '{template_no}' and sett_amount_dr > 0
                group by data_month, bookkeeping_period, process_no, process_name, finance_type, org_name
                    , business_category , business_type, dr_cost_center_no, dr_cost_center_name, dr_account_no
                    , dr_account_name, dr_product_no, dr_product_name, cr_cost_center_no, cr_cost_center_name
                    , cr_account_no, cr_account_name, cr_product_no, cr_product_name, mdm_id, mdm_name, sett_currency

                union all
                select data_month
                    , bookkeeping_period as period_name
                    , process_no as template_no
                    , process_name as template_name
                    , finance_type as template_type
                    , org_name
                    , business_category
                    , business_type
                    , dr_cost_center_no
                    , dr_cost_center_name
                    , dr_account_no
                    , dr_account_name
                    , dr_product_no
                    , dr_product_name
                    , cr_cost_center_no
                    , cr_cost_center_name
                    , cr_account_no
                    , cr_account_name
                    , cr_product_no
                    , cr_product_name
                    , mdm_id
                    , mdm_name
                    , '' as product_name
                    , '-' as amount_symbol
                    , sett_currency as currency_code
                    , sum(sett_amount_dr) as transaction_amount
                from db_sett_oversea.t_bookkeeping_voucher
                where bookkeeping_period = '{period}' and process_no = '{template_no}' and sett_amount_dr < 0
                group by data_month, bookkeeping_period, process_no, process_name, finance_type, org_name
                    , business_category , business_type, dr_cost_center_no, dr_cost_center_name, dr_account_no
                    , dr_account_name, dr_product_no, dr_product_name, cr_cost_center_no, cr_cost_center_name
                    , cr_account_no, cr_account_name, cr_product_no, cr_product_name, mdm_id, mdm_name, sett_currency
            '''.format(period=period, template_no=template_no)
        db_ret = db_sett.query(sql, cls=BookkeepingJMData)

        data_list = []
        for line in db_ret.data:
            data: BookkeepingJMData = line
            data.sett_month = period
            data.ref_approver = ""
            data.dr_sub_account_no = "00000000"
            data.dr_sub_account_name = "缺省"
            data.cr_sub_account_no = "00000000"
            data.cr_sub_account_name = "缺省"
            data.apply_reason = "MidasPay入账 | {}".format(period)
            data.apply_remark = Xutil.link_words(
                data.template_name, data.period_name, data.data_month, data.product_name)
            data.source_system_pk_id = Xutil.md5_str(Xutil.link_words(
                data.data_month, data.period_name, data.template_no, data.template_type, data.org_name
                , data.business_category, data.business_type, data.dr_cost_center_no, data.dr_account_no
                , data.dr_product_no, data.cr_cost_center_no, data.cr_sub_account_no, data.cr_product_no
                , data.mdm_id, data.mdm_name, data.currency_code, data.product_name, data.amount_symbol
            ), case="UPPER")
            data_list.append(data)
        # end for

        # save data
        sql = '''
            delete from db_sett_oversea.t_bookkeeping_jm_midas
            where period_name = '{}' and template_no = '{}' and push_status <> 'Y'
        '''.format(period, template_no)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea", "t_bookkeeping_jm_midas")

    @staticmethod
    def get_jm_data_list(db_sett: MySQLClient, period, template_no, push_status='N'):
        """
            按集团JM格式返回查询数据
        """
        sql = '''
            select * from db_sett_oversea.t_bookkeeping_jm_midas
            where period_name = '{}' and template_no = '{}' and push_status = '{}'
        '''.format(period, template_no, push_status)
        db_ret = db_sett.query(sql, cls=BookkeepingJMData)

        data_list = []
        for line in db_ret.data:
            local_data: BookkeepingJMData = line
            push_data = {}
            push_data['orgName'] = local_data.org_name
            push_data['businessCategory'] = local_data.business_category
            push_data['businessType'] = local_data.business_type
            push_data['periodName'] = local_data.period_name
            push_data['refApprover'] = local_data.ref_approver
            push_data['segment2DR'] = local_data.dr_cost_center_no   # 2DR 成本中心
            push_data['segment3DR'] = local_data.dr_account_no       # 3DR 科目段
            push_data['segment4DR'] = local_data.dr_sub_account_no   # 4DR 辅助段
            push_data['segment5DR'] = local_data.dr_product_no       # 5DR 产品段
            push_data['segment7DR'] = ''                             # 7DR 渠道段
            push_data['segment8DR'] = '000'                          # 8DR ICP段
            push_data['segment2CR'] = local_data.cr_cost_center_no
            push_data['segment3CR'] = local_data.cr_account_no
            push_data['segment4CR'] = local_data.cr_sub_account_no
            push_data['segment5CR'] = local_data.cr_product_no
            push_data['segment7CR'] = ''
            push_data['segment8CR'] = '000'
            push_data['transactionAmount'] = str(local_data.transaction_amount)
            push_data['currencyCode'] = local_data.currency_code
            push_data['sourceSystemPkId'] = local_data.source_system_pk_id
            push_data['applyReason'] = local_data.apply_reason
            push_data['applyRemark'] = local_data.apply_remark
            push_data['mdmId'] = local_data.mdm_id

            data_list.append(push_data)
        # end for
        return data_list

    @staticmethod
    def get_data_list(db_sett: MySQLClient, period):
        sql = '''
            select * 
            from db_sett_oversea.t_bookkeeping_jm_midas
            where period_name = '{}'
        '''.format(period)
        db_ret = db_sett.query(sql, cls=BookkeepingJMData)
        data_list: List[BookkeepingJMData] = db_ret.data
        return data_list

    @staticmethod
    def update_push_status(db_sett: MySQLClient, system_pk_id, push_status='Y'):
        sql = '''
            update db_sett_oversea.t_bookkeeping_jm_midas 
            set push_status = '{}' where source_system_pk_id = '{}'
        '''.format(push_status, system_pk_id)
        db_sett.update(sql)


if __name__ == '__main__':
    pass

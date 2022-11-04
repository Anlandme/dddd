"""
    成本预提报表
    内部商户付给HM的平台手续费，基于暂估平台费
"""
from src import MailToConfig
from src import CostWithholdingData


class CostWithholdingService(object):
    def __init__(self):
        self.msg_set = set()
        self.sett_month = ""
        self.sett_month6 = ""

    def init(self, sett_month):
        self.msg_set = set()
        self.sett_month = sett_month
        self.sett_month6 = sett_month.replace("-", "")

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> message info: {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData(">> message info", self.msg_set),
        ]
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        mail_title = "【MPay月结】{}成本预提_{}".format(sys_tag, self.sett_month6)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def gen_report(self):
        # 成本预提：取内部商户暂估平台费
        sql = '''
            select sett_month
                , bill_month
                , merchant_id
                , merchant_name
                , sub_merchant_id
                , sub_merchant_name
                , plt_ou_id
                , plt_ou_name
                , merchant_ou_id
                , merchant_ou_name
                , merchant_ou_short
                , merchant_coa_no
                , merchant_coa_name
                , merchant_cost_no
                , merchant_cost_name
                , merchant_contract_no
                , sett_currency
                , sum(sett_plt_fee) as sett_plt_amount
            from db_mpay_income.t_mpay_esti_base
            where sett_month = '{}' and merchant_type = 'INTERNAL'
            group by sett_month, bill_month, merchant_id, merchant_name, sub_merchant_id
                , sub_merchant_name, plt_ou_id, plt_ou_name, merchant_ou_id, merchant_ou_name
                , merchant_ou_short, merchant_coa_no, merchant_coa_name, merchant_cost_no
                , merchant_cost_name, merchant_contract_no, sett_currency
        '''.format(self.sett_month)
        db_ret = db_sett.query(sql)

        idx = 1000
        withholding_type = "MidasPay手续费成本"
        data_list = []
        for line in db_ret.data:
            idx += 1
            period_name = str(line["sett_month"])
            da_period_name = str(line["sett_month"])
            prepay_month = Xutil.get_month_next(str(line["sett_month"]))
            currency = str(line["sett_currency"])
            drawing_account_amount = str(line["sett_plt_amount"])
            dept_name = ""
            annotations = Xutil.link_words(withholding_type, self.sett_month6)
            source_id = "{}{}".format(self.sett_month6, idx)
            system_pk_id = Xutil.md5_str(str(line), case="UPPER")

            data = CostWithholdingData()
            data.Fsett_month = self.sett_month
            data.Fwithholding_type = withholding_type
            data.Fproduct_no = str(line["merchant_id"]).strip()
            data.Fproduct_name = str(line["merchant_name"]).strip()
            data.Fcompany_no = str(line["merchant_ou_id"]).strip()
            data.Fcompany_name = str(line["merchant_ou_name"]).strip()
            data.Fcostcenter_no = str(line["merchant_cost_no"]).strip()
            data.Fcostcenter_name = str(line["merchant_cost_name"]).strip()
            data.Faccount_no = "54015080"
            data.Faccount_name = "主营业务成本-渠道及分销成本-渠道分成-其他"
            data.Fsubaccount_no = "00000000"
            data.Fsubaccount_name = "缺省"
            data.Fcoa_product_no = str(line["merchant_coa_no"]).strip()
            data.Fcoa_product_name = str(line["merchant_coa_name"]).strip()
            data.Fdrawing_account_bases = withholding_type
            data.Fvendor_name = str(line["plt_ou_name"]).strip()
            data.Fcurrency = currency
            data.Fperiod_name = period_name
            data.Fda_period_name = da_period_name
            data.Fprepay_month = prepay_month
            data.Fdept_name = dept_name
            data.Fcontract_no = str(line["merchant_contract_no"]).strip()
            data.Ffinance_people = "karinwang"
            data.Ffinance_people_id = "85174"
            data.Fannotations = annotations
            data.Fdrawing_account_amount = drawing_account_amount
            data.Fsource_id = source_id
            data.Fsystem_pk_id = system_pk_id
            data.Fdata_source = "SETT_OVERSEA"

            data_list.append(data)
        # end for

        # save data
        sql = '''
            delete from db_sett_oversea.t_merchant_internal_cost 
            where Fsett_month = '{}' and Fwithholding_type = '{}'
        '''.format(self.sett_month, withholding_type)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea", "t_merchant_internal_cost")

    def push2cos(self):
        data_list = CostWithholdingData.get_data_list(db_sett, self.sett_month)
        if data_list is None or len(data_list) == 0:
            self.msg_set.add("no data to push! {}".format(self.sett_month))
            return

        data_path = "{}/data/".format(sys_path)
        file_path = "{}/cost_withholding_{}.xlsx".format(data_path, self.sett_month6)
        FileUtil.mk_dirs(data_path)
        ExcelUtil.write_excel(data_list, file_path)
        cos_key = "{}/cost_withholding/{}".format(sys_tag, self.sett_month6)
        cos_client.upload_file(cos_key, file_path)

    def do_job(self, sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        self.init(sett_month)
        self.gen_report()
        self.push2cos()
        self.finish()

    @staticmethod
    def task():
        sett_month = "2022-06"
        if len(sys.argv) == 2:
            sett_month = sys.argv[1]
        obj = CostWithholdingService()
        obj.do_job(sett_month)


if "__main__" == __name__:
    CostWithholdingService.task()

"""
    成本确认报表
"""
from src import MailToConfig
from src import MerchantBillBaseData
from src import CostConfirmData


class CostConfirmService(object):
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
        merchant_bill_list = MerchantBillBaseData.get_base_bill_list(db_sett, self.sett_month, merchant_type="INTERNAL")

        data_list = []
        for merchant_bill in merchant_bill_list:
            report_data = CostConfirmData()
            report_data.update_merchant_bill(merchant_bill)
            data_list.append(report_data)
        # end for
        CostConfirmData.batch_insert(db_sett, self.sett_month, data_list)

    def do_job(self, sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        self.init(sett_month)
        self.gen_report()
        self.finish()

    @staticmethod
    def task():
        sett_month = "2022-06"
        if len(sys.argv) == 2:
            sett_month = sys.argv[1]
        obj = CostConfirmService()
        obj.do_job(sett_month)


if "__main__" == __name__:
    CostConfirmService.task()

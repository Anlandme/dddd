"""
    渠道基础账单
    对账交集匹配XE按天汇率，计算USD、CNY金额
"""
from src import OUInfoData
from src import MailToConfig
from src import ChannelRulesData
from src import BillBaseExchangeData
from src import ChannelBillBaseData
from src import BillSettlementBaseData
from src import PltInfoData


class ChannelBillService(object):
    def __init__(self):
        self.msg_set = set()
        self.sett_month = ""
        self.sett_month6 = ""
        self.bill_month = ""
        self.bill_month6 = ""
        self.ou_info_dict: Dict[str, OUInfoData] = {}
        self.exchange_rate_dict: Dict[str, float] = {}
        self.channel_rules_dict: Dict[str, ChannelRulesData]
        self.plt_info_dict: Dict[str, PltInfoData] = {}

    def init(self, sett_month):
        self.msg_set = set()
        self.sett_month = sett_month
        self.sett_month6 = str(sett_month).replace("-", "")
        self.bill_month = Xutil.get_month_before(sett_month)
        self.bill_month6 = str(self.bill_month).replace("-", "")
        self.plt_info_dict = PltInfoData.get_plt_info_dict(db_sett)
        self.ou_info_dict = OUInfoData.get_ou_info_dict(db_midas_merchant)
        self.exchange_rate_dict = BillBaseExchangeData.get_bill_base_exchange_rate_dict(db_sett, self.bill_month)

        flag, msg, self.channel_rules_dict = ChannelRulesData.get_channel_rules_dict(
            db_midas_merchant, self.sett_month, self.ou_info_dict, self.plt_info_dict)
        self.msg_set.update(msg)

    def finish(self):
        if len(self.msg_set) > 0:
            logger.warn(">> message info: {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData("message info", self.msg_set),
        ]
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        mail_title = "【MPay月结_{}】渠道账单基础表_{}".format(sys_tag, self.sett_month6)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def gen_bill_base_report(self):
        base_bill_list: List[BillSettlementBaseData] = \
            BillSettlementBaseData.get_settlement_base_list(db_sett, self.sett_month)

        report_list: List[ChannelBillBaseData] = []
        for base_bill in base_bill_list:
            report_data = ChannelBillBaseData()
            report_data.update_base_data(base_bill)

            flag, msg = report_data.update_channel_rule(self.channel_rules_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            flag, msg = report_data.cal_exchange(self.exchange_rate_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            report_list.append(report_data)
        # end for
        ChannelBillBaseData.batch_insert(db_sett, self.sett_month, report_list)

    def do_job(self, sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        self.init(sett_month)
        self.gen_bill_base_report()
        self.finish()

    @staticmethod
    def task():
        usage_example = "Usage Example: *.py [sett_month: YYYY-MM]"

        sett_month = ""
        sett_month = "2022-06"
        if len(sys.argv) == 2:
            sett_month = sys.argv[1]
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            print("Invalid Param! {}".format(usage_example))
            exit()

        obj = ChannelBillService()
        obj.do_job(sett_month)


if "__main__" == __name__:
    ChannelBillService.task()

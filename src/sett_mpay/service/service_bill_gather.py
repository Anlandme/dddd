"""
    PSP账单聚合
"""
from src import CountryInfoData
from src import MailToConfig
from src import ChannelRulesData
from src import SubChannelMappingData
from src import BillBaseExchangeData
from src import BillSettlementBaseData
from src import BillSettlementUnipinData
from src import BillSettlementMolDetailData
from src \
    import BillSettlementAdyenDetailData


class BillGatherService(object):
    def __init__(self):
        self.msg_set = set()
        self.sett_month = ""
        self.sett_month6 = ""
        self.bill_month = ""
        self.bill_month6 = ""

        self.sett_currency_dict: Dict[str, str] = {}
        self.bill_exchange_rate_dict: Dict[str, float] = {}
        self.country_info_dict: Dict[str, CountryInfoData] = {}
        self.sub_channel_dict: Dict[str, SubChannelMappingData] = {}
        self.default_cid_dict: Dict[str, dict] = {}

    def init(self, sett_month):
        self.msg_set = set()
        self.sett_month = sett_month
        self.sett_month6 = str(sett_month).replace("-", "")
        self.bill_month = Xutil.get_month_before(sett_month)
        self.bill_month6 = str(self.bill_month).replace("-", "")

        self.country_info_dict = CountryInfoData.get_country_info_dict(db_sett)
        self.sett_currency_dict = ChannelRulesData.get_sett_currency_dict(db_midas_merchant, logger)
        self.bill_exchange_rate_dict = BillBaseExchangeData.get_bill_base_exchange_rate_dict(db_sett, self.bill_month)
        self.sub_channel_dict = SubChannelMappingData.get_sub_channel_mapping_dict(db_midas_merchant)
        self.default_cid_dict = ChannelRulesData.get_default_cid_mapper(db_sett, self.sett_month)

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> error message! {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData("error message", self.msg_set),
        ]
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        mail_title = "【MPay月结_{}】账单解析汇总_{}".format(sys_tag, self.sett_month6)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def sync_bill_mol(self):
        channel = "razer"
        bill_list: List[BillSettlementMolDetailData] = \
            BillSettlementMolDetailData.get_bill_sum_list(db_sett, self.bill_month)

        result_list = []
        for data in bill_list:
            data.channel = channel
            flag, msg, base_bill = data.get_base_bill(
                self.country_info_dict, self.sub_channel_dict, self.sett_currency_dict, self.default_cid_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue
            base_bill.sett_month = self.sett_month
            result_list.append(base_bill)
        # end for
        BillSettlementBaseData.batch_insert(db_sett, self.sett_month, channel, result_list)

    def sync_bill_unipin(self):
        channel = "unipin"
        bill_list: List[BillSettlementUnipinData] = BillSettlementUnipinData.get_bill_list(db_sett, self.bill_month)

        result_list = []
        for data in bill_list:
            data.channel = channel
            flag, msg, base_bill = data.get_base_bill(
                self.country_info_dict, self.sub_channel_dict, self.sett_currency_dict, self.default_cid_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue
            base_bill.sett_month = self.sett_month
            result_list.append(base_bill)
        # end for
        BillSettlementBaseData.batch_insert(db_sett, self.sett_month, channel, result_list)

    def sync_bill_adyen(self):
        channel = "adyen"
        bill_list: List[BillSettlementAdyenDetailData] \
            = BillSettlementAdyenDetailData.get_bill_list(db_sett, self.bill_month)

        result_list = []
        for data in bill_list:
            data.channel = channel
            flag, msg = data.update_base_amount()
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            flag, msg, base_bill = data.get_base_bill(
                self.country_info_dict, self.sub_channel_dict, self.sett_currency_dict, self.default_cid_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue
            base_bill.sett_month = self.sett_month
            result_list.append(base_bill)
        # end for
        BillSettlementBaseData.batch_insert(db_sett, self.sett_month, channel, result_list)

    def do_job(self, sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]

        self.init(sett_month)
        self.sync_bill_mol()
        self.sync_bill_unipin()
        self.sync_bill_adyen()
        self.finish()

    @staticmethod
    def task():
        usage_example = "Usage Example: *.py [sett_month: YYYY-MM]"

        sett_month = ""
        if len(sys.argv) == 2:
            sett_month = sys.argv[1]
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            print("Invalid Param! {}".format(usage_example))
            exit()

        # sett_month = "2022-06"
        obj = BillGatherService()
        obj.do_job(sett_month)


if "__main__" == __name__:
    BillGatherService.task()

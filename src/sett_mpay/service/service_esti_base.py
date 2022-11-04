"""
    暂估基础报表
    db_sett_oversea.t_income_estimate_base_v2
"""
from src import OUInfoData
from src import MailToConfig
from src import XeExchangeData
from src import CountryInfoData
from src import TaxFeeData
from src import PltInfoData
from src import ChannelFeeData
from src import MerchantFeeData
from src import RefundFeeData
from src import MerchantMapperData
from src import MerchantRulesData
from src import ChannelRulesData
from src import ChannelTaxRulesData
from src import EstiBaseWater
from src import EstiBaseReport


class EstiBaseService(object):
    def __init__(self):
        self.msg_set = set()
        self.sett_month = ''
        self.sett_month6 = ''
        self.ou_info_dict: Dict[str, OUInfoData] = {}
        self.plt_info_dict: Dict[str, PltInfoData] = {}
        self.country_info_dict: Dict[str, CountryInfoData] = {}
        self.tax_rules_dict: Dict[str, ChannelTaxRulesData] = {}
        self.exchange_rate_dict: Dict[str, float] = {}
        self.channel_rules_dict: Dict[str, ChannelRulesData] = {}
        self.merchant_rules_dict: Dict[str, MerchantRulesData] = {}
        self.merchant_mapper_dict: Dict[str, MerchantMapperData] = {}

    def init(self, sett_month):
        self.msg_set = set()
        self.sett_month = sett_month
        self.sett_month6 = str(sett_month).replace("-", "")
        self.ou_info_dict = OUInfoData.get_ou_info_dict(db_midas_merchant)
        self.plt_info_dict = PltInfoData.get_plt_info_dict(db_sett)
        self.country_info_dict = CountryInfoData.get_country_info_dict(db_sett)
        self.merchant_mapper_dict = MerchantMapperData.get_data_dict(db_midas_merchant)
        self.tax_rules_dict = ChannelTaxRulesData.get_channel_tax_rules_dict(db_midas_merchant, self.sett_month)
        self.exchange_rate_dict = XeExchangeData.get_xe_exchange_dict_last_day(
            db_sett, self.sett_month)

        flag, msg_set, self.channel_rules_dict = ChannelRulesData.get_channel_rules_dict(
            db_midas_merchant, self.sett_month, self.ou_info_dict, self.plt_info_dict)
        self.msg_set.update(msg_set)

        flag, msg_set, self.merchant_rules_dict = MerchantRulesData.get_merchant_rules_dict(
            db_midas_merchant, self.sett_month, self.ou_info_dict, self.plt_info_dict)
        self.msg_set.update(msg_set)

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> message info: {}".format(self.msg_set))
            # 告警邮件
            mail_content_list = [
                MailContentData("message info", self.msg_set),
            ]
            mail_to = MailToConfig.get_mail_to(db_sett, __file__)
            mail_title = "【MPay月结_{}】流水暂估基础表_{}".format(sys_tag, self.sett_month6)
            MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def cal_data_list(self):
        data_list = []
        base_water_list = EstiBaseWater.get_data_list(db_sett, self.sett_month, self.country_info_dict)
        for base_water in base_water_list:
            # 代缴税
            flag, msg, tax_fee = TaxFeeData.cal_tax(base_water, self.tax_rules_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)

            # 渠道费
            flag, msg, channel_fee = ChannelFeeData.cal_channel_fee(base_water, tax_fee, self.channel_rules_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            # 商户费
            flag, msg, merchant_fee = MerchantFeeData.cal_merchant_fee(
                base_water, tax_fee, self.merchant_rules_dict, self.merchant_mapper_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            # 退款
            flag, msg, refund_fee = RefundFeeData.cal_refund_fee(
                base_water, channel_fee, merchant_fee, self.exchange_rate_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            # 流水基础表
            report_data = EstiBaseReport()
            report_data.update_period(self.sett_month)
            report_data.update_base_water(base_water)
            report_data.update_tax_fee(tax_fee)
            report_data.update_channel_fee(channel_fee)
            report_data.update_merchant_fee(merchant_fee)
            report_data.update_refund_fee(refund_fee)
            report_data.ori_plt_fee = merchant_fee.merchant_fee_total - channel_fee.channel_fee_total

            # 汇率转换
            flag, msg = report_data.cal_exchange(self.exchange_rate_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue

            data_list.append(report_data)
        # end for
        EstiBaseReport.batch_insert(db_sett, self.sett_month, data_list)

    def do_job(self, sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        self.init(sett_month)
        self.cal_data_list()
        self.finish()

    @staticmethod
    def task():
        sett_month = "2022-06"
        service = EstiBaseService()
        service.do_job(sett_month)


if __name__ == '__main__':
    EstiBaseService.task()

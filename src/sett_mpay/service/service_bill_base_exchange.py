"""
    综合汇率基础数据
    对账交集匹配XE按天汇率，计算USD、CNY金额
"""
import sys
from typing import List

from src import MailToConfig
from src import XeExchangeData
from src import BillBaseExchangeData
from src import ChannelRulesData


class BillBaseExchangeService(object):
    def __init__(self):
        self.msg_set = set()  # 邮件告警信息
        self.data_month = ""
        self.data_month6 = ""
        self.sett_currency_dict = {}
        self.xe_exchange_rate_dict = {}
        self.check_result_list = []  # 汇率对比结果

    def init(self, data_month):
        self.msg_set = set()
        self.data_month = data_month
        self.data_month6 = data_month.replace("-", "")
        self.sett_currency_dict = ChannelRulesData.get_sett_currency_dict(db_midas_merchant, logger)
        self.xe_exchange_rate_dict = XeExchangeData.get_xe_exchange_dict_by_month(db_sett, self.data_month)
        self.check_result_list = []

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> error message! {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData("error message", self.msg_set),
            MailContentData("check result", self.check_result_list, table_flag=True),
        ]
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        mail_title = "【MidasPay月结】收入综合汇率_{}".format(self.data_month6)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def cal_xe_amount(self):
        """
            使用XE汇率转换金额
        :return:
        """
        tdw_data_list: List[BillBaseExchangeData] = BillBaseExchangeData.get_tdw_data(db_sett, self.data_month)

        data_list = []
        for data in tdw_data_list:
            flag, msg = data.update_exchange(self.xe_exchange_rate_dict, self.sett_currency_dict)
            if msg != "SUCCESS":
                self.msg_set.add(msg)
            if not flag:
                continue
            data_list.append(data)
        # end for
        BillBaseExchangeData.batch_insert(db_sett, self.data_month, data_list)

    def check_rate(self):
        bill_base_exchange_rate_dict = BillBaseExchangeData.get_bill_base_exchange_rate_dict(db_sett, self.data_month)
        for key, value in bill_base_exchange_rate_dict.items():
            data_type, data_month, currency_ori, currency_dst = Xutil.split(key)

            xe_exchange_key = Xutil.link_words("{}-01".format(data_month), currency_ori, currency_dst)
            if currency_ori == currency_dst:
                continue
            else:
                if xe_exchange_key not in self.xe_exchange_rate_dict or self.xe_exchange_rate_dict[xe_exchange_key] == 0:
                    self.msg_set.add(">> missing xe exchange rate: {}".format(xe_exchange_key))
                    continue
                xe_exchange_rate = self.xe_exchange_rate_dict[xe_exchange_key]
            check_data = {
                "data_type": data_type,
                "data_month": data_month,
                "currency_ori": currency_ori,
                "currency_dst": currency_dst,
                "base_rate": "{:.8f}".format(value),
                "xe_rate": "{:.8f}".format(xe_exchange_rate),
                "diff_rate": "{:.2%}".format(value / xe_exchange_rate - 1)
            }
            self.check_result_list.append(check_data)
        # end for

    def upload2cos(self):
        """
            MidasPay汇率数据上传到COS
        :return:
        """
        bill_base_exchange_rate_list = BillBaseExchangeData.get_bill_base_exchange_rate_list(db_sett, self.data_month)
        data_path = "{}/data/".format(sys_path)
        file_path = "{}/bill_base_exchange_rate_{}.xlsx".format(data_path, self.data_month6)
        FileUtil.mk_dirs(data_path)
        ExcelUtil.write_excel(bill_base_exchange_rate_list, file_path)
        cos_key = "gss/bill_base_exchange_rate/{}".format(self.data_month6)
        cos_client.upload_file(cos_key, file_path)

    def do_job(self, sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        data_month = Xutil.get_month_before(sett_month)

        self.init(data_month)
        self.cal_xe_amount()
        self.check_rate()
        self.upload2cos()
        self.finish()

    @staticmethod
    def task():
        usage_example = "Usage Example: *.py [data_month: YYYY-MM]"

        data_month = ""
        # data_month = "2022-05"
        if len(sys.argv) == 2:
            data_month = sys.argv[1]
        if Xutil.is_invalid_date(data_month, date_format="%Y-%m"):
            print("Invalid Param! {}".format(usage_example))
            exit()

        obj = BillBaseExchangeService()
        obj.do_job(data_month)


if "__main__" == __name__:
    BillBaseExchangeService.task()

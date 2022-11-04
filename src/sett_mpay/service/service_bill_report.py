"""
    账单报表
    1. 代收账单
    2. 平台费账单
    3. BOSS账单：平台费 + 内部商户
"""
import sys
from src import PltBillReportData
from src import BossBillReportData
from src import AgencyBillReportData
from src import ChannelBillBaseData
from src import MerchantBillBaseData


class BillReportService(object):
    @staticmethod
    def gen_agency_report(sett_month):
        merchant_base_bill_list = MerchantBillBaseData.get_base_bill_list(db_sett, sett_month)

        data_list = []
        for merchant_bill in merchant_base_bill_list:
            report_data = AgencyBillReportData()
            report_data.update_merchant_base_bill(merchant_bill)
            data_list.append(report_data)
        # end for
        # save data
        AgencyBillReportData.batch_insert(db_sett, sett_month, data_list)

    @staticmethod
    def gen_plt_report(sett_month):
        merchant_base_bill_list = MerchantBillBaseData.get_base_bill_list(db_sett, sett_month)

        data_list = []
        for merchant_bill in merchant_base_bill_list:
            report_data = PltBillReportData()
            report_data.update_merchant_base_bill(merchant_bill)
            data_list.append(report_data)
        # end for
        # save data
        PltBillReportData.batch_insert(db_sett, sett_month, "MERCHANT", data_list)

    @staticmethod
    def gen_plt_diff_report(sett_month):
        channel_base_bill_list = ChannelBillBaseData.get_base_bill_list(db_sett, sett_month)
        merchant_base_bill_list = MerchantBillBaseData.get_base_bill_list(db_sett, sett_month)

        data_list = []
        for channel_bill in channel_base_bill_list:
            report_data = PltBillReportData()
            report_data.cal_plt_diff_channel(channel_bill)
            data_list.append(report_data)
        # end for
        for merchant_bill in merchant_base_bill_list:
            report_data = PltBillReportData()
            report_data.cal_plt_diff_merchant(merchant_bill)
            data_list.append(report_data)
        # end for
        # save data
        PltBillReportData.batch_insert(db_sett, sett_month, "CHANNEL_DIFF", data_list)

    @staticmethod
    def gen_boss_report(sett_month):
        plt_bill_list = PltBillReportData.get_bill_list(db_sett, sett_month)

        data_list = []
        for plt_bill in plt_bill_list:
            report_data = BossBillReportData()
            report_data.cal_plt_bill(plt_bill)
            data_list.append(report_data)
        # end for
        # save data
        BossBillReportData.batch_insert(db_sett, sett_month, "PLATFORM", data_list)

        # upload to cos
        data_month6 = str(sett_month).replace("-", "")
        data_path = "{}/data/{}/".format(sys_path, sys_tag)
        file_path = "{}/report_boss_bill_{}.xlsx".format(data_path, data_month6)
        FileUtil.mk_dirs(data_path)
        ExcelUtil.write_excel(data_list, file_path)
        cos_key = "{}/report_boss_bill/{}".format(sys_tag, data_month6)
        cos_client.upload_file(cos_key, file_path)

    @staticmethod
    def do_job(sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        BillReportService.gen_agency_report(sett_month)
        BillReportService.gen_plt_report(sett_month)
        BillReportService.gen_plt_diff_report(sett_month)
        BillReportService.gen_boss_report(sett_month)

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

        BillReportService.do_job(sett_month)


if "__main__" == __name__:
    BillReportService.task()

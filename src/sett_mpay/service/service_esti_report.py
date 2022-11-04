"""
    账单报表
    1. 代收账单
    2. 平台费账单
    3. BOSS账单：平台费 + 内部商户
"""
import sys
from src import PltEstiReportData
from src import AgencyEstiReportData
from src import BossEstiReportData
from src import EstiBaseReport


class EstiReportService(object):
    @staticmethod
    def gen_agency_report(sett_month):
        base_data_list = EstiBaseReport.get_data_list(db_sett, sett_month)

        data_list = []
        for base_data in base_data_list:
            report_data = AgencyEstiReportData()
            report_data.update_merchant_base_bill(base_data)
            data_list.append(report_data)
        # end for
        # save data
        AgencyEstiReportData.batch_insert(db_sett, sett_month, data_list)

    @staticmethod
    def gen_plt_report(sett_month):
        base_data_list = EstiBaseReport.get_data_list(db_sett, sett_month)

        data_list = []
        for base_data in base_data_list:
            report_data = PltEstiReportData()
            report_data.update_merchant_base_bill(base_data)
            data_list.append(report_data)
        # end for
        # save data
        PltEstiReportData.batch_insert(db_sett, sett_month, "MERCHANT", data_list)

    @staticmethod
    def gen_boss_report(sett_month):
        base_data_list = PltEstiReportData.get_bill_list(db_sett, sett_month)

        data_list = []
        for base_data in base_data_list:
            report_data = BossEstiReportData()
            report_data.cal_plt_bill(base_data)
            data_list.append(report_data)
        # end for
        # save data
        BossEstiReportData.batch_insert(db_sett, sett_month, "PLATFORM", data_list)

        # upload to cos
        data_month6 = str(sett_month).replace("-", "")
        data_path = "{}/data/{}/".format(sys_path, sys_tag)
        file_path = "{}/report_boss_esti_{}.xlsx".format(data_path, data_month6)
        FileUtil.mk_dirs(data_path)
        ExcelUtil.write_excel(data_list, file_path)
        cos_key = "{}/report_boss_esti/{}".format(sys_tag, data_month6)
        cos_client.upload_file(cos_key, file_path)

    @staticmethod
    def do_job(sett_month):
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=4)[0:7]
        EstiReportService.gen_agency_report(sett_month)
        EstiReportService.gen_plt_report(sett_month)
        EstiReportService.gen_boss_report(sett_month)

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

        EstiReportService.do_job(sett_month)


if "__main__" == __name__:
    EstiReportService.task()

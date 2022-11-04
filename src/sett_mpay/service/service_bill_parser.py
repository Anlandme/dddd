"""
    PSP 账单下载服务
"""
from sett_sdk_base.xutil import Xutil
from src import BillMolService
from src import BillUnipinService


class BillParserService(object):
    @staticmethod
    def download_bill(channel, sett_month, force=False):
        if str(force).upper() in ["Y", "TRUE"]:
            force = True
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            sett_month = Xutil.get_date_before(before_count=35)[0:7]
        bill_month = Xutil.get_month_before(sett_month)

        msg = "SUCCESS"
        if channel in ['unipin', 'os_unipin']:
            service = BillUnipinService()
            service.do_job(bill_month, force)
        elif channel in ['mol', 'razer']:
            service = BillMolService()
            service.do_job(bill_month, force)
        else:
            msg = "service not found: {}".format(channel)

        return msg

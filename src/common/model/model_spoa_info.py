"""
    业务代码信息：SPOA
"""
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.mysql_client import MySQLClient


class SpoaInfoData(object):
    def __init__(self):
        # 业务代码、结算组、应用组、部门等信息
        self.spoa_id = ""
        self.spoa_name = ""
        self.sett_group = ""
        self.sett_group_name = ""
        self.busi_group = ""
        self.busi_group_name = ""
        self.dept = ""
        self.dept_name = ""

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    @staticmethod
    def get_spoa_buy():
        spoa_info = SpoaInfoData()
        spoa_info.spoa_id = "-APP105470"
        spoa_info.spoa_name = "midasbuy手续费_android(diamond)"
        spoa_info.sett_group = "127669"
        spoa_info.sett_group_name = "midasbuy_bilateral"
        spoa_info.busi_group = "10356"
        spoa_info.busi_group_name = "Midasbuy"
        spoa_info.dept = "37628"
        spoa_info.dept_name = "IEG海外计费联合项目组（虚拟组织）"
        return spoa_info

    @staticmethod
    def get_spoa_pay():
        spoa_info = SpoaInfoData()
        spoa_info.spoa_id = "-SXCART200002"
        spoa_info.spoa_name = "midaspay_bilateral"
        spoa_info.sett_group = "127670"
        spoa_info.sett_group_name = "midaspay_bilateral"
        spoa_info.busi_group = "10674"
        spoa_info.busi_group_name = "MidasPay"
        spoa_info.dept = "37628"
        spoa_info.dept_name = "IEG海外计费联合项目组（虚拟组织）"
        return spoa_info

    @staticmethod
    def get_spoa_reseller():
        spoa_info = SpoaInfoData()
        spoa_info.spoa_id = "-SXCART1000001"
        spoa_info.spoa_name = "MidasReseller_CD"
        spoa_info.sett_group = "1000047"
        spoa_info.sett_group_name = "MidasReseller_CD"
        spoa_info.busi_group = "100037"
        spoa_info.busi_group_name = "MidasReseller"
        spoa_info.dept = "37628"
        spoa_info.dept_name = "IEG海外计费联合项目组（虚拟组织）"
        return spoa_info

    @staticmethod
    def get_spoa_info_dict(db_sett: MySQLClient):
        """
            获取业务代码的相关信息
        :return:
        """
        sql = '''
            SELECT Fvalue, Fname, Fcode_type
            FROM db_spoa.t_code
            WHERE Fcode_type IN ('SETT_GROUP', 'BUSI_GROUP', 'DEPT_NO', 'FEE_TYPE')
        '''
        db_ret = db_sett.query(sql)

        sett_group_name_dict = {}
        busi_group_name_dict = {}
        dept_name_dict = {}
        fee_type_name_dict = {}
        for line in db_ret.data:
            code_type = line["Fcode_type"]
            if code_type == 'SETT_GROUP':
                sett_group_name_dict[line["Fvalue"]] = Xutil.recode_str(line["Fname"])
            elif code_type == 'BUSI_GROUP':
                busi_group_name_dict[line["Fvalue"]] = Xutil.recode_str(line["Fname"])
            elif code_type == 'DEPT_NO':
                dept_name_dict[line["Fvalue"]] = Xutil.recode_str(line["Fname"])
            elif code_type == 'FEE_TYPE':
                fee_type_name_dict[line["Fvalue"]] = Xutil.recode_str(line["Fname"])

        sql = '''
            SELECT Foss_sid, Fservice_name, Fsett_group, Fbusi_group, Fdept, Ffee_type, Ffee_value
            FROM db_spoa.t_oss_sid
            WHERE Fsett_group <> '' AND Fstatus = 1
        '''
        db_ret = db_sett.query(sql)

        spoa_info_dict = {}
        for line in db_ret.data:
            spoa_info = SpoaInfoData()
            spoa_info.spoa_id = line["Foss_sid"]
            spoa_info.spoa_name = Xutil.recode_str(line["Fservice_name"])
            spoa_info.sett_group = line["Fsett_group"]
            spoa_info.busi_group = line["Fbusi_group"]
            spoa_info.dept = str(line["Fdept"])
            spoa_info.fee_type = str(line["Ffee_type"])
            spoa_info.fee_value = int(line["Ffee_value"])

            if spoa_info.sett_group in sett_group_name_dict:
                spoa_info.sett_group_name = sett_group_name_dict[spoa_info.sett_group]
            if spoa_info.busi_group in busi_group_name_dict:
                spoa_info.busi_group_name = busi_group_name_dict[spoa_info.busi_group]
            if spoa_info.dept in dept_name_dict:
                spoa_info.dept_name = dept_name_dict[spoa_info.dept]
            if spoa_info.fee_type in fee_type_name_dict:
                spoa_info.fee_type_name = fee_type_name_dict[spoa_info.fee_type]
            spoa_info_dict[spoa_info.spoa_id] = spoa_info
        # end for

        # 补充 midasbuy spoa信息
        spoa_info_buy = SpoaInfoData.get_spoa_buy()
        spoa_info_dict[spoa_info_buy.spoa_id] = spoa_info_buy

        # 补充 midaspay spoa信息
        spoa_info_pay = SpoaInfoData.get_spoa_pay()
        spoa_info_dict[spoa_info_pay.spoa_id] = spoa_info_pay

        # 补充 reseller spoa信息
        spoa_info_reseller = SpoaInfoData.get_spoa_reseller()
        spoa_info_dict[spoa_info_reseller.spoa_id] = spoa_info_reseller
        return spoa_info_dict

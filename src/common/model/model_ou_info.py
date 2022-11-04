from sett_sdk_base.mysql_client import MySQLClient


class OUInfoData(object):
    """
        OU字段表
        sett_conf.t_ou_list
    """
    def __init__(self):
        self.FOuID = ''
        self.FOuName = ''
        self.FOuType = ''
        self.FOu = ''
        self.FOuFullName = ''
        self.FBeginDate = ''
        self.FEndDate = ''
        self.FCompanyCode = ''
        self.FAbbrCompanyName = ''
        self.FStatus = ''

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    @staticmethod
    def parse_dict(data_dict: dict):
        if data_dict is None:
            return None
        if type(data_dict) != dict:
            data_dict = data_dict.__dict__
        if len(data_dict) == 0:
            return None

        if "create_time" in data_dict:
            data_dict["create_time"] = str(data_dict["create_time"])
        if "update_time" in data_dict:
            data_dict["update_time"] = str(data_dict["update_time"])

        data = OUInfoData()
        data.__dict__ = data_dict
        return data

    @staticmethod
    def parse_list(data_list: list):
        if data_list is None or len(data_list) == 0:
            return None

        new_list = []
        for data_dict in data_list:
            data = OUInfoData.parse_dict(data_dict)
            new_list.append(data)
        # end for
        return new_list

    @staticmethod
    def parse_db_ret(db_ret):
        if db_ret is None or db_ret.data is None:
            return db_ret
        db_ret.data = OUInfoData.parse_list(db_ret.data)
        return db_ret

    @staticmethod
    def get_ou_info_dict(db_midas_merchant: MySQLClient):
        sql = '''
            SELECT *
            FROM sett_conf.t_ou_list
            WHERE FStatus = 1
        '''
        db_ret = db_midas_merchant.query(sql)

        data_dict = {}
        for line in db_ret.data:
            ou_info = OUInfoData.parse_dict(line)
            data_dict[ou_info.FOuID] = ou_info
            data_dict[ou_info.FOuName] = ou_info
            data_dict[ou_info.FOuFullName] = ou_info
        # end for
        return data_dict

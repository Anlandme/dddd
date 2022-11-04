from src import logger
from sett_sdk_base.mysql_client import MySQLClient, MySQLUtil


class CountryInfoData(object):
    # db_gss_config.t_country_info
    DB_NAME = "db_gss_config"
    TB_NAME = "t_country_info"

    def __init__(self):
        self.id = 0
        self.country_desc = ''
        self.country_name = ''
        self.country_name_cn = ''
        self.country_code = ''
        self.country_code3 = ''
        self.country_number = ''
        self.status = 'Y'
        self.create_time = ''
        self.update_time = ''

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

        data = CountryInfoData()
        data.__dict__ = data_dict
        return data

    @staticmethod
    def parse_list(data_list: list):
        if data_list is None or len(data_list) == 0:
            return None

        new_list = []
        for data_dict in data_list:
            data = CountryInfoData.parse_dict(data_dict)
            new_list.append(data)
        # end for
        return new_list

    @staticmethod
    def parse_db_ret(db_ret):
        if db_ret is None or db_ret.data is None:
            return db_ret
        db_ret.data = CountryInfoData.parse_list(db_ret.data)
        return db_ret

    @staticmethod
    def list(db_sett: MySQLClient, key=None, page=None, size=None):
        sql = '''
            select * from {db_name}.{tb_name} where status = 'Y'
        '''.format(db_name=CountryInfoData.DB_NAME, tb_name=CountryInfoData.TB_NAME)
        if key:
            sql += '''
                 and (country_desc like '%{key}%' 
                    or country_name like '%{key}%'
                    or country_name_cn like '%{key}%'
                    or country_code = '{key}'
                )
            '''.format(key=key)

        db_ret = db_sett.query_page(sql, page, size)
        return CountryInfoData.parse_db_ret(db_ret)

    @staticmethod
    def batch_insert(db_sett: MySQLClient, data_list: list):
        if data_list is None or len(data_list) == 0:
            logger.info("[batch_insert] no data to insert!", __file__)
            return
        db_sett.batch_insert(data_list, CountryInfoData.DB_NAME, CountryInfoData.TB_NAME)

    @staticmethod
    def update(db_sett: MySQLClient, data_dict):
        if data_dict is None or len(data_dict) == 0:
            return
        if type(data_dict) == CountryInfoData:
            data_dict = data_dict.__dict__
        if "id" not in data_dict:
            logger.info("[update] no data to update!", __file__)
            return

        _where = " id={}".format(data_dict["id"])
        sql = MySQLUtil.gen_update_sql(
            CountryInfoData.DB_NAME,  CountryInfoData.TB_NAME, data_dict
            , where=_where, field_filter_list=["id", "update_time"]
        )
        db_sett.update(sql)

    @staticmethod
    def delete(db_sett: MySQLClient, _id):
        if not str(_id).isnumeric():
            logger.info("[delete] no data to delete!", __file__)
            return None

        _id = int(_id)
        sql = '''
            UPDATE {}.{} SET status = 'D' WHERE id = {}
        '''.format(
            CountryInfoData.DB_NAME, CountryInfoData.TB_NAME, _id
        )
        db_sett.update(sql)

    @staticmethod
    def get_country_info_dict(db_sett: MySQLClient):
        # 通过国家名称、国家代码查询国别信息
        sql = '''
            select * from {db_name}.{tb_name} where status = 'Y'
        '''.format(db_name=CountryInfoData.DB_NAME, tb_name=CountryInfoData.TB_NAME)
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            country_info = CountryInfoData.parse_dict(line)
            data_dict[country_info.country_desc] = country_info
            data_dict[country_info.country_name] = country_info
            data_dict[country_info.country_name_cn] = country_info
            data_dict[country_info.country_code] = country_info
            data_dict[country_info.country_code3] = country_info
            data_dict[country_info.country_number] = country_info
        # end for

        return data_dict


if __name__ == '__main__':
    pass

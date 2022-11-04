import re
from src import logger
from src import Xutil
from src import MySQLClient, MySQLUtil


class ApiAuthData(object):
    DB_NAME = "db_gss_auth"
    TB_NAME = "t_api_auth"

    def __init__(self):
        self.id = 0
        self.secret_id = ''
        self.secret_key = ''
        self.host = ''
        self.system_provider = ''
        self.system_consumer = ''
        self.status = 'Y'
        self.create_time = ''
        self.update_time = ''

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    def check_auth(self, secret_id, host):
        if Xutil.is_empty(secret_id) or Xutil.is_empty(host):
            return False
        if re.match(r'^\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}$', host) is None:
            return False
        if secret_id == self.secret_id and self.host.find(host) >= 0:
            return True
        return False

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

        data = ApiAuthData()
        data.__dict__ = data_dict
        return data

    @staticmethod
    def parse_list(data_list: list):
        if data_list is None or len(data_list) == 0:
            return None

        new_list = []
        for data_dict in data_list:
            data = ApiAuthData.parse_dict(data_dict)
            new_list.append(data)
        # end for
        return new_list

    @staticmethod
    def parse_db_ret(db_ret):
        if db_ret is None or db_ret.data is None:
            return db_ret
        db_ret.data = ApiAuthData.parse_list(db_ret.data)
        return db_ret

    @staticmethod
    def get(db_sett: MySQLClient, secret_id):
        sql = '''
            select * from {db_name}.{tb_name} where status = 'Y' and secret_id = '{secret_id}'
        '''.format(db_name=ApiAuthData.DB_NAME, tb_name=ApiAuthData.TB_NAME, secret_id=secret_id)
        db_ret = db_sett.query(sql)
        return ApiAuthData.parse_db_ret(db_ret)

    @staticmethod
    def list(db_sett: MySQLClient, key=None, page=None, size=None):
        sql = '''
            select * from {db_name}.{tb_name} where status = 'Y'
        '''.format(db_name=ApiAuthData.DB_NAME, tb_name=ApiAuthData.TB_NAME)
        if key:
            sql += '''
                 and (country_desc like '%{key}%' 
                    or country_name like '%{key}%'
                    or country_name_cn like '%{key}%'
                    or country_code = '{key}'
                )
            '''.format(key=key)

        db_ret = db_sett.query_page(sql, page, size)
        return ApiAuthData.parse_db_ret(db_ret)

    @staticmethod
    def batch_insert(db_sett: MySQLClient, data_list: list):
        if data_list is None or len(data_list) == 0:
            logger.info("[batch_insert] no data to insert!", __file__)
            return
        db_sett.batch_insert(data_list, ApiAuthData.DB_NAME, ApiAuthData.TB_NAME)

    @staticmethod
    def update(db_sett: MySQLClient, data_dict):
        if data_dict is None or len(data_dict) == 0:
            return
        if type(data_dict) == ApiAuthData:
            data_dict = data_dict.__dict__
        if "id" not in data_dict:
            logger.info("[update] no data to update!", __file__)
            return

        _where = " id={}".format(data_dict["id"])
        sql = MySQLUtil.gen_update_sql(
            ApiAuthData.DB_NAME, ApiAuthData.TB_NAME, data_dict
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
            ApiAuthData.DB_NAME, ApiAuthData.TB_NAME, _id
        )
        db_sett.update(sql)


if __name__ == '__main__':
    pass

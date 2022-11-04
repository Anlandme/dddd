from src import conf_sys
from src import ApiAuthData


class ApiAuthService(object):
    def __init__(self):
        self.db = db_sett

    def check_auth(self, secret_id, host):
        if not eval(conf_sys.get("sys_info", "sys_auth")):
            # 系统未开启鉴权要求
            return True
        if host == "127.0.0.1":
            return True

        db_ret = ApiAuthData.get(self.db, secret_id)
        if db_ret is None or db_ret.data is None or len(db_ret.data) == 0:
            return False
        auth_data = ApiAuthData.parse_dict(db_ret.data[0])
        return auth_data.check_auth(secret_id, host)

    def get(self, secret_id):
        db_ret = ApiAuthData.get(self.db, secret_id)
        if db_ret is None or db_ret.data is None or len(db_ret.data) == 0:
            return None
        return db_ret.data[0]

    def list(self, key=None, page=None, size=None):
        return ApiAuthData.list(self.db, key, page, size)

    def add(self, data_list):
        if type(data_list) == dict:
            data_list = [data_list]
        country_info_list = ApiAuthData.parse_list(data_list)
        return ApiAuthData.batch_insert(self.db, country_info_list)

    def update(self, data_dict: dict):
        country_info = ApiAuthData.parse_dict(data_dict)
        return ApiAuthData.update(self.db, country_info)

    def delete(self, _id):
        return ApiAuthData.delete(self.db, _id)

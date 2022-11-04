from src import db_sett
from src import CountryInfoData


class CountryInfoService(object):
    def __init__(self):
        self.db = db_sett

    def finish(self):
        if self.db:
            self.db.close()

    def list(self, key=None, page=None, size=None):
        return CountryInfoData.list(self.db, key, page, size)

    def add(self, data_list):
        if type(data_list) == dict:
            data_list = [data_list]
        country_info_list = CountryInfoData.parse_list(data_list)
        return CountryInfoData.batch_insert(self.db, country_info_list)

    def update(self, data_dict: dict):
        country_info = CountryInfoData.parse_dict(data_dict)
        return CountryInfoData.update(self.db, country_info)

    def delete(self, _id):
        return CountryInfoData.delete(self.db, _id)

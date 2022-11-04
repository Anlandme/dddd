from src import Xutil
from sett_sdk_base.mysql_client import MySQLClient


class XeExchangeData(object):
    # db_gss_config.t_exchange_rate_daily
    DB_NAME = "db_gss_config"
    TB_NAME = "t_exchange_rate_daily"

    def __init__(self):
        self.data_date = ''
        self.data_type = ''
        self.currency_base = ''
        self.currency_target = ''
        self.exchange_rate = 0

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    def parse_dict(self, data_dict: dict):
        if "id" in data_dict:
            del data_dict["id"]
        if "create_time" in data_dict:
            data_dict["create_time"] = str(data_dict["create_time"])
        if "update_time" in data_dict:
            data_dict["update_time"] = str(data_dict["update_time"])
        data_dict["exchange_rate"] = float(data_dict["exchange_rate"])

        self.__dict__ = data_dict
        return self

    @staticmethod
    def get_xe_exchange_dict(db_sett: MySQLClient, date_begin, date_end=None):
        if date_end is None:
            date_end = date_begin
        sql = '''
            select * from db_gss_config.t_exchange_rate_daily
            where data_type = 'EX' and data_date between '{}' and '{}'
        '''.format(date_begin, date_end)
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            data = XeExchangeData().parse_dict(line)
            data_date = data.data_date
            currency_ori = data.currency_base
            currency_dst = data.currency_target
            exchange_rate = data.exchange_rate
            if exchange_rate == 0:
                continue
            data_dict[Xutil.link_words(data_date, currency_ori, currency_dst)] = exchange_rate
        # end for
        return data_dict

    @staticmethod
    def get_xe_exchange_dict_by_month(db_sett: MySQLClient, data_month):
        date_begin, date_end = Xutil.get_month_date_first_and_last(data_month)
        return XeExchangeData.get_xe_exchange_dict(db_sett, date_begin, date_end)

    @staticmethod
    def get_xe_exchange_dict_last_day(db_sett: MySQLClient, data_month):
        date_last = Xutil.get_month_last_day(data_month)
        date_current = Xutil.get_date_before(before_count=2)
        if date_current < date_last:
            # 未到月底最后1天，取2天前的日期
            date_last = date_current
        sql = '''
            select * from db_gss_config.t_exchange_rate_daily
            where data_type = 'EX' and data_date = '{}'
        '''.format(date_last)
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            data = XeExchangeData().parse_dict(line)
            currency_ori = data.currency_base
            currency_dst = data.currency_target
            exchange_rate = data.exchange_rate
            if exchange_rate == 0:
                continue
            data_dict[Xutil.link_words(currency_ori, currency_dst)] = exchange_rate
        # end for
        return data_dict


if __name__ == '__main__':
    pass

"""
    渠道代缴税
    sett_conf_v2.t_oversea_channel_tax_rule
"""
from typing import List

from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean, BeanUtil
from sett_sdk_base.mysql_client import MySQLClient


class ChannelTaxRulesData(BaseBean):
    def __init__(self):
        self.channel = ''
        self.cid = ''
        self.ou_id = ''
        self.date_begin = ''
        self.date_end = ''
        self.country = ''
        self.province = ''
        self.city = ''
        self.tax_category = ''
        self.withhold_from_channel = ''
        self.channel_tax_rate = ''
        self.status = ''

    @staticmethod
    def get_channel_tax_rules_dict(db_sett: MySQLClient, data_month):
        last_date = Xutil.get_month_last_day(data_month)
        sql = '''
            select FMainChannel as channel
                , FChannelID as cid
                , FOuID as ou_id
                , FBeginDate as date_begin
                , FEndDate as date_end
                , FCountryCode as country
                , FProvince as province
                , FCity as city
                , FTaxCategory as tax_category
                , FWithholdFromChannel as withhold_from_channel
                , FChannelTaxRate as channel_tax_rate
                , FStatus as status
            from sett_conf_v2.t_oversea_channel_tax_rule
            where FStatus = 1 and FBeginDate <= '{data_date}' and FEndDate >= '{data_date}'
        '''.format(data_date=last_date)
        db_ret = db_sett.query(sql, cls=ChannelTaxRulesData)
        data_list: List[ChannelTaxRulesData] = db_ret.data

        data_dict = {}
        for data in data_list:
            data.country = str(data.country).upper()
            data_dict[Xutil.link_words(data.cid, data.country)] = data
        # end for
        return data_dict

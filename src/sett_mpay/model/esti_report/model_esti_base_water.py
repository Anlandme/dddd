"""
    TDW基础流水
    db_tdw_data.t_ssb_midaspay_sum
    db_tdw_data.t_ssb_midaspay_sum_midasbuy (HM + HS 模式的流水)
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import CountryInfoData


class EstiBaseWater(BaseBean):
    def __init__(self):
        self.data_date = ''
        self.data_month = ''
        self.ou_id = ''
        self.merchant_ou_id = ''
        self.merchant_id = ''
        self.sub_merchant_id = ''
        self.channel = ''
        self.cid = ''
        self.mcid = ''
        self.sub_channel = ''
        self.midas_country_code = ''
        self.midas_country_name = ''
        self.channel_country_code = ''
        self.channel_country_name = ''
        self.tran_type = ''
        self.tran_currency = ''
        self.tran_amount = 0.0
        self.tran_numbers = 0.0

    def update_country_info(self, country_info_dict: Dict[str, CountryInfoData]):
        if self.channel in ['os_unipin', 'unipin']:
            self.channel_country_code = self.tran_currency[0: 2]
            self.channel_country_name = self.tran_currency[0: 2]
        if self.channel in ['mol', 'razer']:
            self.channel_country_code = self.midas_country_code
            self.channel_country_name = self.midas_country_name
            if Xutil.is_empty(self.channel_country_code) or self.channel_country_code in ['None']:
                self.channel_country_code = self.tran_currency[0: 2]
                self.channel_country_name = self.tran_currency[0: 2]

        if self.midas_country_code in country_info_dict:
            midas_country = country_info_dict[self.midas_country_code]
            self.midas_country_code = midas_country.country_code
            self.midas_country_name = midas_country.country_name
        if self.channel_country_code in country_info_dict:
            channel_country = country_info_dict[self.channel_country_code]
            self.channel_country_code = channel_country.country_code
            self.channel_country_name = channel_country.country_name

    @staticmethod
    def get_data_list(
            db_sett: MySQLClient
            , data_month
            , country_info_dict: Dict[str, CountryInfoData]
    ):
        data_month6 = str(data_month).replace("-", "")[0:6]
        sql = '''
            select data_date
                , data_month
                , ou_id
                , merchant_ou_id
                , merchant_id
                , sub_merchant_id
                , channel
                , cid
                , mcid
                , sub_channel
                , pay_country as midas_country_code
                , psp_country as channel_country_code
                , tran_type
                , tran_currency
                , sum(tran_amount) as tran_amount
                , sum(tran_numbers) as tran_numbers
            from db_tdw_data.t_ssb_midaspay_sum
            where data_month = '{data_month6}'
                and check_result = 'SUCCESS'
                and tran_status in ('CAPTURED', 'COMPLETED')
                and (merchant_ou_id is not null and merchant_ou_id <> '756') 
            group by data_date, data_month, ou_id, merchant_ou_id
                , merchant_id, sub_merchant_id, channel, sub_channel
                , cid, mcid, pay_country, psp_country, tran_type, tran_currency
                
            union all
            select data_date
                , data_month
                , '' as ou_id
                , '' as merchant_ou_id
                , pay_mch_id as merchant_id
                , pay_sub_mch_id as sub_merchant_id
                , psp_channel as channel
                , pay_cid as cid
                , pay_mcid as mcid
                , psp_sub_channel as sub_channel
                , pay_country as midas_country_code
                , psp_country as channel_country_code
                , tran_type
                , currency as tran_currency
                , sum(currency_amount) as tran_amount
                , sum(pay_count) as tran_numbers
            from db_tdw_data.t_ssb_midaspay_sum_midasbuy
            where data_month = '{data_month6}'
                and check_result_rsb = 'SUCCESS'
                and check_result_rri = 'SUCCESS'
            group by data_date, data_month, ou_id, merchant_ou_id
                , merchant_id, sub_merchant_id, channel, sub_channel
                , cid, mcid, pay_country, psp_country, tran_type, tran_currency
        '''.format(data_month6=data_month6)
        db_ret = db_sett.query(sql, cls=EstiBaseWater)
        data_list: List[EstiBaseWater] = db_ret.data

        for data in data_list:
            data.data_month = Xutil.format_date(data.data_month, format_input="%Y%m", format_output="%Y-%m")
            data.data_date = Xutil.format_date(data.data_date, format_input="%Y%m%d", format_output="%Y-%m-%d")
            data.update_country_info(country_info_dict)
        # end for
        return data_list


if __name__ == '__main__':
    from src import db_sett
    country_info_dict = CountryInfoData.get_country_info_dict(db_sett)
    EstiBaseWater.get_data_list(db_sett, "2022-06", country_info_dict)

"""
    主数据CID、MCID映射表
    sett_conf_v2.t_channel_mapping
    sett_conf_v2.t_merchant_channel_mapping
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient


class SubChannelMappingData(BaseBean):
    def __init__(self):
        self.channel = ''  # 子渠道 cid
        self.sub_channel_midas = ''
        self.sub_channel_daily = ''
        self.sub_channel_month = ''
        self.sub_channel_contract = ''
        self.cid = ''
        self.mcid = ''

    @staticmethod
    def get_sub_channel_mapping_dict(db_sett: MySQLClient):
        sql = '''
            select A.FMainChannel as channel
                , A.FMidasWaterSubChannel as sub_channel_midas
                , A.FDailySubChannelList as sub_channel_daily
                , A.FMonthSubChannelList as sub_channel_month
                , A.FContractSubChannelList as sub_channel_contract
                , A.FChannelID as cid
                , B.FMidasChannelID as mcid
            from sett_conf_v2.t_channel_mapping A
            left join sett_conf_v2.t_merchant_channel_mapping B
                on A.FChannelID = B.FChannelID
            where A.FStatus = 1 
        '''
        db_ret = db_sett.query(sql, cls=SubChannelMappingData)
        data_list: List[SubChannelMappingData] = db_ret.data

        data_dict = {}
        for data in data_list:
            channel = data.channel
            data_dict[Xutil.link_words(channel, Xutil.clean_str(data.sub_channel_midas))] = data
            data_dict[Xutil.link_words(channel, Xutil.clean_str(data.sub_channel_daily))] = data
            data_dict[Xutil.link_words(channel, Xutil.clean_str(data.sub_channel_month))] = data
            data_dict[Xutil.link_words(channel, data.cid)] = data
            data_dict[Xutil.link_words(data.cid)] = data
        # end for
        return data_dict

    @staticmethod
    def get_sub_channel_info(db_sett: MySQLClient, channel, sub_channel):
        sql = '''
            select A.FMainChannel as chanel
                , A.FMidasWaterSubChannel as sub_channel_midas
                , A.FDailySubChannelList as sub_channel_daily
                , A.FMonthSubChannelList as sub_channel_month
                , A.FContractSubChannelList as sub_channel_contract
                , A.FChannelID as cid
                , B.FMidasChannelID as mcid
            from sett_conf_v2.t_channel_mapping A
            left join sett_conf_v2.t_merchant_channel_mapping B
                on A.FChannelID = B.FChannelID
            where A.FStatus = 1 AND A.FMainChannel = '{channel}' and (
                    A.FDailySubChannelList like '%{sub_channel}%' 
                    or A.FMonthSubChannelList like '%{sub_channel}%' 
                )
        '''.format(channel=channel, sub_channel=sub_channel)
        db_ret = db_sett.query(sql, cls=SubChannelMappingData)
        data_list: List[SubChannelMappingData] = db_ret.data

        if data_list is None or len(data_list) != 1:
            return None
        return data_list[0]

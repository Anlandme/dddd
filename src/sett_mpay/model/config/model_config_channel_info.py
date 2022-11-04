"""
    渠道信息
    sett_conf_v2.t_channel_merchant_info
"""
from typing import List, Dict
from sett_sdk_base.xutil import Xutil
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient
from src import PltInfoData


class ChannelInfoData(BaseBean):
    def __init__(self):
        self.channel = ''
        self.channel_mdm_id = ''
        self.channel_mdm_name = ''
        self.plt_type = ''
        self.plt_ou_id = ''
        self.plt_ou_name = ''
        self.plt_ou_short = ''
        self.plt_mdm_id = ''
        self.plt_mdm_name = ''
        self.plt_coa_no = ''
        self.plt_coa_name = ''
        self.plt_cost_no = ''
        self.plt_cost_name = ''
        self.contract_no = ''
        self.date_begin = ''
        self.date_end = ''

    def update_plt_info(self, plt_info: PltInfoData):
        self.plt_type = plt_info.plt_type
        self.plt_ou_id = plt_info.plt_ou_id
        self.plt_ou_name = plt_info.plt_ou_name
        self.plt_ou_short = plt_info.plt_ou_short
        self.plt_mdm_id = plt_info.plt_mdm_id
        self.plt_mdm_name = plt_info.plt_mdm_name
        self.plt_coa_no = plt_info.plt_coa_no
        self.plt_coa_name = plt_info.plt_coa_name
        self.plt_cost_no = plt_info.plt_cost_no
        self.plt_cost_name = plt_info.plt_cost_name

    @staticmethod
    def get_channel_info_dict(
            db_midas_merchant: MySQLClient
            , data_month
            , plt_info_dict: Dict[str, PltInfoData]
    ):
        last_date = Xutil.get_month_last_day(data_month)
        sql = '''
            select FOuID as plt_ou_id
                , FMdmID as channel_mdm_id
                , FMdmName as channel_mdm_name
                , FBeginDate as date_begin
                , FEndDate as date_end
            from sett_conf_v2.t_channel_merchant_info
            where FStatus = 1 and FBeginDate <= '{data_date}' and FEndDate >= '{data_date}'
        '''.format(data_date=last_date)
        db_ret = db_midas_merchant.query(sql, cls=ChannelInfoData)
        data_list: List[ChannelInfoData] = db_ret.data

        msg_set = set()
        data_dict = {}
        for data in data_list:
            if data.plt_ou_id not in plt_info_dict:
                msg_set.add("missing plt info: {}".format(data.plt_ou_id))
                continue
            plt_info = plt_info_dict[data.plt_ou_id]
            data.update_plt_info(plt_info)

            data_dict[data.channel] = data
        # edn for
        return data_dict

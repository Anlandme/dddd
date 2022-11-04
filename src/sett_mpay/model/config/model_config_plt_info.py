"""
    商户rule_id
    db_mpay_config.t_mpay_plt_info
"""
from typing import List, Dict
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient


class PltInfoData(BaseBean):
    def __init__(self):
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
        self.status = ''

    @staticmethod
    def get_plt_info_dict(db_sett: MySQLClient):
        sql = '''
            select * 
            from db_gss_config.t_mpay_plt_info
            where status = 'Y'
        '''
        db_ret = db_sett.query(sql, cls=PltInfoData)
        data_list: List[PltInfoData] = db_ret.data

        data_dict = {}
        for data in data_list:
            data_dict[data.plt_ou_id] = data
        # end for
        return data_dict

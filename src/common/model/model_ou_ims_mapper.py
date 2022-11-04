"""
    IMS OU 映射表
    db_sett_oversea_config.t_sett_oversea_ou_ims
"""
from typing import Dict
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.mysql_client import MySQLClient


class ImsOuMapperData(BaseBean):
    REGION_CN = "CN"  # 默认区域为CN

    def __init__(self):
        self.ou_code = ''
        self.enable_flag = ''
        self.start_date_active = ''
        self.end_date_active = ''
        self.region_code = ''
        self.ebs_ou_id = ''
        self.fusion_ou_id = ''

    @staticmethod
    def get_ims_ou_mapper_dict(db_sett: MySQLClient):
        sql = '''
            SELECT *
            FROM db_sett_oversea_config.t_sett_oversea_ou_ims
            WHERE enable_flag = 'Y'
        '''
        db_ret = db_sett.query(sql, cls=ImsOuMapperData)

        data_dict: Dict[str, ImsOuMapperData] = {}
        for line in db_ret.data:
            data: ImsOuMapperData = line
            data_dict[data.ebs_ou_id] = data
            data_dict[data.fusion_ou_id] = data
        # end for
        return data_dict

    @staticmethod
    def batch_replace(db_sett: MySQLClient, data_list):
        db_sett.foreach_replace(data_list, "db_sett_oversea_config", "t_sett_oversea_ou_ims")

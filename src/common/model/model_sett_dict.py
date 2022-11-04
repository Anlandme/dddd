from sett_sdk_base.xutil import Xutil
from sett_sdk_base.mysql_client import MySQLClient


"""
-- db_gss_config.t_sett_dict | 结算字典表
USE db_gss_config;
DROP TABLE IF EXISTS t_sett_dict;
CREATE TABLE `t_sett_dict` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `para_type` varchar(64) NOT NULL COMMENT '类型',
  `para_type_desc` varchar(128) NOT NULL DEFAULT '' COMMENT '类型描述',
  `para_key` varchar(64) NOT NULL COMMENT '匹配主键',
  `para_key_desc` varchar(128) NOT NULL DEFAULT '' COMMENT '匹配主键描述',
  `para_code` varchar(64) NOT NULL COMMENT '匹配编号',
  `para_value` varchar(256) NOT NULL COMMENT '匹配结果',
  `para_status` varchar(8) NOT NULL COMMENT '状态(Y:有效，N:无效)',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE_KEY` (`para_type`, `para_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='结算字典表'
;
"""


class SettDictData(object):
    # db_gss_config.t_sett_dict | 结算字典表
    DB_NAME = "db_gss_config"
    TB_NAME = "t_sett_dict"

    TYPE_SETT_CHANNEL = "SETT_CHANNEL"  # 结算渠道 | key:米大师支付渠道，code:结算渠道编号(推送IMS)，value:结算渠道名称(推送IMS)
    TYPE_IMS_CHANNEL = "IMS_CHANNEL"  # IMS渠道 | key:业务场景，code:IMS渠道编号，value:IMS渠道名称

    def __init__(self):
        self.para_type = ''
        self.para_type_desc = ''
        self.para_key = ''
        self.para_key_desc = ''
        self.para_code = ''
        self.para_value = ''
        self.para_status = ''

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

        self.__dict__ = data_dict
        return self

    @staticmethod
    def get_sett_dict(db_sett: MySQLClient, para_type=None):
        sql = '''
            SELECT para_type
                , para_type_desc
                , para_key
                , para_key_desc
                , para_code
                , para_value
                , para_status
            FROM db_gss_config.t_sett_dict
            WHERE para_status = 'Y'
        '''
        if para_type and str(para_type).strip() != "":
            sql += " AND para_type = '{}'".format(para_type)
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            data = SettDictData().parse_dict(line)

            data_key = Xutil.link_words(data.para_type, data.para_key)
            data_dict[data_key] = data
        # end for
        return data_dict


if __name__ == '__main__':
    from src import db_sett
    sett_dict = SettDictData.get_sett_dict(db_sett, para_type="IMS_SETT_TYPE")
    sett_dict = SettDictData.get_sett_dict(db_sett, para_type="SETT_CHANNEL")
    for key, value in sett_dict.items():
        print(key, value)

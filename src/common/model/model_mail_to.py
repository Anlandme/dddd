import os
from typing import List
from sett_sdk_base.bean_util import BaseBean
from sett_sdk_base.file_util import FileUtil
from sett_sdk_base.mysql_client import MySQLClient


class MailToConfig(BaseBean):
    def __init__(self):
        self.mail_key = ''
        self.mail_to = ''
        self.status = ''

    @staticmethod
    def get_mail_to_dict(db_sett: MySQLClient):
        sql = '''
            select * from db_gss_config.t_config_mail_to
        '''
        db_ret = db_sett.query(sql, cls=MailToConfig)
        data_list: List[MailToConfig] = db_ret.data

        data_dict = {}
        for data in data_list:
            data_dict[data.mail_key] = data.mail_to
        # end for
        return data_dict

    @staticmethod
    def get_mail_default(db_sett: MySQLClient):
        sql = '''
                select * 
                from db_gss_config.t_config_mail_to 
                where status = 'Y' and mail_key = 'DEFAULT'
            '''
        db_ret = db_sett.query(sql, cls=MailToConfig)
        data_list: List[MailToConfig] = db_ret.data
        if data_list is not None and len(data_list) > 0:
            data = data_list[0]
            return data.mail_to
        return "sett_oversea;"

    @staticmethod
    def get_mail_to(db_sett: MySQLClient, mail_key):
        if os.path.isfile(mail_key):
            mail_key = FileUtil.get_file_name(mail_key)
        sql = '''
            select * 
            from db_gss_config.t_config_mail_to 
            where status = 'Y' and mail_key = '{}'
        '''.format(mail_key)
        db_ret = db_sett.query(sql, cls=MailToConfig)
        data_list: List[MailToConfig] = db_ret.data
        if data_list is not None and len(data_list) > 0:
            data = data_list[0]
            return data.mail_to
        return MailToConfig.get_mail_default(db_sett)


if __name__ == '__main__':
    pass

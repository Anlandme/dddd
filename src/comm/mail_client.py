import os
import json
import base64
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ses.v20201002 import ses_client, models
from tencentcloud.ses.v20201002.models import Simple
from typing import List

from .xlog import Xlog
from .xutil import Xutil
from .file_util import FileUtil
from .template import HtmlTemplate
from .config_reader import ConfigReader


class MailConfig(object):
    def __init__(self
                 , secret_id=None
                 , secret_key=None
                 , end_point=None
                 , region=None
                 , mail_from=None
                 , mail_to_dict=None):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.end_point = end_point
        self.region = region
        self.mail_from = mail_from
        self.mail_to_dict = mail_to_dict

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", "")

    def get_mail_to(self, key, default="jiantaowu"):
        if key in self.mail_to_dict:
            return self.mail_to_dict[key]
        return default

    @staticmethod
    def get_config(conf_file, conf_section="mail_tcloud"):
        config_reader = ConfigReader.get_instance(conf_file)
        secret_id = config_reader.get(conf_section, "secret_id")
        secret_key = config_reader.get(conf_section, "secret_key")
        region = config_reader.get(conf_section, "region")
        end_point = config_reader.get(conf_section, "end_point")
        mail_from = config_reader.get(conf_section, "mail_from")
        mail_to_dict = config_reader.get_section_dict("mail_to")

        mail_conf = MailConfig(
            secret_id, secret_key, end_point, region, mail_from, mail_to_dict
        )
        return mail_conf

    @staticmethod
    def get_config_default(
            secret_id
            , secret_key
            , region="ap-hongkong"
            , end_point="ses.tencentcloudapi.com"
            , mail_from="teg_gss@txc.qq.com"
            , mail_to_dict=None
    ):
        if mail_to_dict is None:
            mail_to_dict = {}
        mail_conf = MailConfig(
            secret_id, secret_key, end_point, region, mail_from, mail_to_dict
        )
        return mail_conf


class MailAccountData(object):
    def __init__(self, user, password):
        self.user = user             # 用户邮箱
        self.password = password     # smtp 授权码，非邮箱登陆密码
        self.smtp_server = "smtp.qq.com"
        self.smtp_port = 465

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__)

    @staticmethod
    def get_default_account():
        default_account_list = [
            MailAccountData("sett_oversea_01@qq.com", "cgerdidfjahlbhed"),
            MailAccountData("sett_oversea_02@qq.com", "mwnaidnhhqahdhbi"),
            MailAccountData("sett_oversea_03@qq.com", "fibumfpdtbigbgjh"),
            MailAccountData("sett_oversea_04@qq.com", "glawjolvtnvtbdjj"),
        ]
        idx = random.randint(0, len(default_account_list) - 1)
        mail_account = default_account_list[idx]
        return mail_account


class MailContentData(object):
    def __init__(self, title, data, table_flag=False):
        """
        :param title: 内容描述
        :param data: 具体内容
        :param table_flag: 是否生成表格（如果要生成表格，data 必须是字典列表）
        """
        self.title = title
        self.data = data
        self.table_flag = table_flag

    @staticmethod
    def get_mail_content(mail_content_list):
        if mail_content_list is None or len(mail_content_list) == 0:
            return HtmlTemplate.get_html("")
        if type(mail_content_list) == MailContentData:
            mail_content_list = [mail_content_list]
        if type(mail_content_list) != list:
            return HtmlTemplate.get_html(str(mail_content_list))

        content = ""
        other_data_list = []
        for mail_content_data in mail_content_list:
            if type(mail_content_data) != MailContentData:
                # 非 MailContentData 类型的数据
                other_data_list.append(mail_content_data)
                continue

            # MailContentData 类型的数据
            content_div = ""
            title = "<b>{}:</b>".format(mail_content_data.title)
            data = mail_content_data.data
            table_flag = mail_content_data.table_flag

            content_div += "</br>{}<br>".format(title)
            if table_flag:
                table = HtmlTemplate.get_table(data)
                content_div += table
            else:
                if type(data) in (list, set):
                    data_sorted = sorted(data)
                    for line in data_sorted:
                        content_div += "{}</br>".format(line)
                else:
                    content_div += "{}</br>".format(data)
            content += "<div style='clear:both;'>{}</div></br>".format(content_div)
        # end for

        # 非 MailContentData 类型的数据
        for data in other_data_list:
            if type(data) in (set, list, tuple):
                for line in data:
                    content += "{}</br>".format(line)
            else:
                content += "{}</br>".format(data)
        # end for
        return HtmlTemplate.get_html(content)


class MailClient(object):
    @staticmethod
    def get_receiver_list(receiver_list, suffix="@tencent.com"):
        if type(receiver_list) == str:
            receiver_list = receiver_list.split(";")

        temp_list = []
        for receiver in receiver_list:
            if Xutil.is_empty(receiver):
                continue
            if Xutil.is_not_empty(suffix) and not receiver.endswith(suffix):
                receiver = "{}{}".format(receiver, suffix)
            temp_list.append(receiver)
        # end for
        receiver_list = temp_list
        return receiver_list

    @staticmethod
    def send_mail_v2(
            mail_title
            , mail_to
            , mail_content_list: List[MailContentData] = None
            , attach_file_list: List[str] = None
            , mail_config: MailConfig = None
            , logger = Xlog.get_default_logger()):
        """
            发送 MailContentData 列表，HTML 格式
        :param mail_title: mail_subject
        :param mail_to:
        :param mail_content_list: [MailContentData， MailContentData]
        :param attach_file_list: [file1, file2]
        :param mail_config: MailConfig 使用腾讯云发送邮件时需要提共账号配置信息
        :return:
        """
        try:
            mail_content = MailContentData.get_mail_content(mail_content_list)
            if mail_config:
                # mail tcloud
                try:
                    MailClient.send_mail_tcloud(
                        mail_title, mail_to, mail_config, mail_content, attach_file_list, logger)
                except Exception:
                    MailClient.send_mail_smtp(mail_title, mail_to, mail_content, attach_file_list, logger)
            else:
                # mail qq
                MailClient.send_mail_smtp(mail_title, mail_to, mail_content, attach_file_list, logger)
        except Exception as error:
            logger.warn("fail to send mail! {}".format(error))
            logger.exception(error)

    @staticmethod
    def send_mail_smtp(
            mail_title
            , mail_to
            , mail_content
            , attach_file_list
            , logger=Xlog.get_default_logger()):
        receiver_list = MailClient.get_receiver_list(mail_to)

        # 创建一个带附件的实例
        mail_account = MailAccountData.get_default_account()
        message = MIMEMultipart()
        message['From'] = mail_account.user
        message['To'] = ",".join(receiver_list)
        message['Subject'] = Header(mail_title, 'utf-8')
    
        # 邮件正文内容
        message.attach(MIMEText(mail_content, 'HTML', 'utf-8'))
    
        # 附件1（附件为TXT格式的文本）
        if attach_file_list and len(attach_file_list) > 0:
            for attach_file in attach_file_list:
                if os.path.exists(attach_file):
                    attach_file_name = FileUtil.get_file_name(attach_file)
                    att1 = MIMEText(open(attach_file, 'rb').read(), 'base64', 'utf-8')
                    att1["Content-Type"] = 'application/octet-stream'
                    att1["Content-Disposition"] = 'attachment; filename={}'.format(attach_file_name)
                    message.attach(att1)
            # end for
        # end if
    
        try:
            smtp = smtplib.SMTP_SSL(mail_account.smtp_server, mail_account.smtp_port)
            smtp.set_debuglevel(0)
            smtp.ehlo(mail_account.smtp_server)
            smtp.login(mail_account.user, mail_account.password)   # smtp 授权码登陆
            smtp.sendmail(mail_account.user, receiver_list, message.as_string())
            smtp.quit()
            logger.info("send mail success!")
        except smtplib.SMTPException as e:
            logger.warn("send mail failed!")
            logger.exception(e)

    @staticmethod
    def send_mail_tcloud(
            mail_title
            , mail_to
            , mail_config: MailConfig
            , mail_content
            , attach_file_list=None
            , logger=Xlog.get_default_logger()):
        """
        :param mail_title:
        :param mail_to:
        :param mail_config:
        :param mail_content:
        :param attach_file_list: [file1, file2] # 只支持普通文本格式
        :param logger:
        :return:
        """

        secret_id = mail_config.secret_id
        secret_key = mail_config.secret_key
        end_point = mail_config.end_point
        region = mail_config.region
        mail_from = mail_config.mail_from

        receiver_list = MailClient.get_receiver_list(mail_to)

        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = end_point

            cred = credential.Credential(secret_id, secret_key)
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ses_client.SesClient(cred, region, clientProfile)

            content = Simple()
            content.Html = base64.b64encode(str(mail_content).strip().encode('utf-8')).decode('utf-8')

            params = {
                "FromEmailAddress": mail_from,
                "Destination": receiver_list,
                "Subject": mail_title,
                "Simple": content.__dict__,
                # "Attachments": attach_file_list
            }

            attach_data_list = []
            if attach_file_list is not None and len(attach_file_list) > 0:
                for attach_file in attach_file_list:
                    if not os.path.exists(attach_file) or not os.path.isfile(attach_file):
                        continue
                    file_name = FileUtil.get_file_name(attach_file)
                    file_content = FileUtil.get_file_content(attach_file)
                    file_content = base64.b64encode(str(file_content).strip().encode('utf-8')).decode('utf-8')
                    attach_data = {
                        "FileName": file_name,
                        "Content": file_content,
                    }
                    attach_data_list.append(attach_data)
                # end for
            params["Attachments"] = attach_data_list

            req = models.SendEmailRequest()
            req.from_json_string(json.dumps(params))
            result = client.SendEmail(req)
            logger.info(">> send send_mail_tcloud result: {}".format(result))
        except Exception as err:
            logger.warn("send mail failed!")
            logger.exception(err)


if __name__ == "__main__":
    pass

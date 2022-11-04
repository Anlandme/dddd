"""
    数据接入JM(集团账务系统)，通过IMS转发
    凭证汇总生成JM数据
"""
from src import MailToConfig
from src import HttpInvokeErp
from src import BookkeepingJMData
from src import BookkeepingTemplateData


class AcctJMService(object):
    def __init__(self):
        self.msg_set = set()
        self.period = ""
        self.period6 = ""

    def init(self, period):
        self.msg_set = set()
        self.period = period
        self.period6 = str(period).replace("-", "")

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> message info: {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData(">> message info", self.msg_set),
        ]
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        mail_title = "【MPay月结_{}】JM数据_{}".format(sys_tag, self.period6)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def gen_report(self, period, template_type=None, period_type=None):
        self.init(period)
        template_dict = BookkeepingTemplateData.get_bookkeeping_template_dict(
            db_sett, template_type=template_type, period_type=period_type)
        if template_dict is None or len(template_dict) == 0:
            self.msg_set.add(">> template not found! template_type: {}, period_type: {}".format(
                template_type, period_type
            ))
            return
        for key, value in template_dict.items():
            BookkeepingJMData.gen_jm_data_report(db_sett, period, value.template_no, value.template_type)
        # end for
        self.finish()

    def push2jm(self, period, template_type):
        self.init(period)
        template_dict = BookkeepingTemplateData.get_bookkeeping_template_dict(
            db_sett, template_type=template_type)
        if template_dict is None or len(template_dict) == 0:
            self.msg_set.add(">> template not found! template_type: {}".format(template_type))
            return

        jm_data_list = []
        for key, value in template_dict.items():
            jm_data_list.extend(BookkeepingJMData.get_jm_data_list(db_sett, period, value.template_no))
        # end for

        for data in jm_data_list:
            system_pk_id = data["sourceSystemPkId"]
            try:
                result = HttpInvokeErp.send_accounting_data([data])
                logger.info(">> result: {}".format(result))
                if "returnCode" in result and str(result["returnCode"]) == "0":
                    BookkeepingJMData.update_push_status(db_sett, system_pk_id)
                elif "{}已经导入".format(system_pk_id) in str(result):
                    BookkeepingJMData.update_push_status(db_sett, system_pk_id)
                else:
                    self.msg_set.add(">> pushed: {} | result: {}".format(
                        system_pk_id, result))
            except Exception as err:
                self.msg_set.add(">> fail to push jm data: {} | {}".format(system_pk_id, err))
                logger.error(">> fail to push jm data: {}".format(data))
                logger.exception(err)
        # end for
        self.finish()

    @staticmethod
    def push2cos(period):
        period6 = str(period).replace("-", '')
        data_list = BookkeepingJMData.get_data_list(db_sett, period)
        data_path = "{}/data/{}/".format(sys_path, sys_tag)
        file_path = "{}/report_jm_{}.xlsx".format(data_path, period6)
        FileUtil.mk_dirs(data_path)
        ExcelUtil.write_excel(data_list, file_path)
        cos_key = "{}/report_jm/{}".format(sys_tag, period6)
        cos_client.upload_file(cos_key, file_path)

    @staticmethod
    def task():
        usage_example = "Usage Example: *.py [period: YYYY-MM]"

        period = ""
        if len(sys.argv) == 2:
            period = sys.argv[1]
        if Xutil.is_invalid_date(period, date_format="%Y-%m"):
            print("Invalid Param! {}".format(usage_example))
            exit()

        # sett_month = "2022-04"
        obj = AcctJMService()
        obj.push2cos(period)


if "__main__" == __name__:
    AcctJMService.task()

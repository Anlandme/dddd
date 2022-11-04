"""
    MPAY 渠道账单解析-MOL DETAIL
"""
import re
import sys
import copy
from src import MailToConfig


class BillMolService(object):
    def __init__(self):
        self.channel = "razer"
        self.file_key = "007_mol_global"
        self.bill_month = ""
        self.bill_month6 = ""
        self.msg_set = set()

    def init(self, bill_month):
        self.bill_month = bill_month
        self.bill_month6 = bill_month.replace("-", "")
        self.msg_set = set()

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error("message info: {}".format(self.msg_set))

            mail_content_list = [
                MailContentData("message info", self.msg_set),
            ]
            mail_title = "【MPAY账单解析】{}_{}".format(self.channel, self.bill_month6)
            mail_to = MailToConfig.get_mail_to(db_sett, __file__)
            MailClient.send_mail_v2(mail_title, mail_to, mail_content_list=mail_content_list)

    @staticmethod
    def get_base_path(bill_month6):
        base_path = "{}/data/download_settlement/{}".format(sys_path, bill_month6)
        FileUtil.mk_dirs(base_path)
        return base_path

    def download_file(self):
        base_path = BillMolService.get_base_path(self.bill_month6)
        file_name = "{}_{}.tar.gz".format(self.bill_month6, self.file_key)
        local_file = "{}/{}".format(base_path, file_name)
        if base_path.count("/") > 3 and len(base_path) > 64:
            # 清理数据，防止误清理
            cmd_clean = "rm -rf {}/*{}*".format(base_path, self.file_key)
            os.popen(cmd_clean).readlines()

        # 下载文件
        cos_key = Xutil.link_words('channel_bill', self.bill_month6, file_name, link_str="/")
        cos_client.download_file(cos_key, local_file)

        # 解压文件
        cmd_untar = "cd {}; tar -zxvf {}".format(base_path, file_name)
        os.popen(cmd_untar).readlines()

    def parse_file(self, data_path):
        file_list = FileUtil.get_file_list(data_path, child=True)
        field_list = [
            'serial_no', 'merchant_name', 'order_id', 'merchant_reference_id', 'payment_ref_id', 'origin_order_id',
            'commission_territory', 'description', 'transaction_type', 'channel', 'merchant_trans_currency',
            'merchant_trans_amount', 'payment_term', 'commission_rate', 'commission_amount', 'transaction_datetime',
            'payment_currency_code', 'payment_amount', 'service_charge_rate', 'service_charge_amount', 'vat_gst_rate',
            'vat_gst_amount', 'gross_end_user_price'
        ]
        re_order = re.compile(r'^MPO\d{8,12}$')  # 匹配订单号

        data_list = []
        for file_path in file_list:
            file_md5 = FileUtil.get_file_md5(file_path)
            file_name = FileUtil.get_file_name(file_path)
            if file_name.startswith(".") or file_name.startswith("~"):
                continue
            if file_name.endswith(".tar") or file_name.endswith(".tar.gz"):
                continue
            if file_path.lower().find("/hs/") < 0:
                continue

            # 解析内容
            try:
                file_content = ExcelUtil.read_excel_xlrd(file_path, field_list)
                for line in file_content:
                    try:
                        if not re_order.match(str(line["order_id"])):
                            continue

                        # 原始字段
                        merchant_name = str(line["merchant_name"])
                        commission_territory = str(line["commission_territory"])
                        sub_channel = str(line["channel"])
                        merchant_trans_currency = str(line["merchant_trans_currency"])
                        merchant_trans_amount = float(line["merchant_trans_amount"])
                        commission_amount = float(line["commission_amount"])

                        # 结果数据
                        data = copy.deepcopy(line)
                        data["bill_type"] = "HS"
                        data["bill_month"] = self.bill_month
                        data["due_month"] = Xutil.get_month_next(self.bill_month)
                        data["due_date"] = Xutil.get_month_last_day(data["due_month"])
                        data["channel"] = self.channel
                        data["channel_product_no"] = ""
                        data["channel_product_name"] = merchant_name
                        data["sub_channel"] = sub_channel
                        data["country"] = commission_territory
                        data["tran_type"] = "PAY"
                        data["tran_currency"] = merchant_trans_currency
                        data["tran_amount"] = merchant_trans_amount
                        data["tran_numbers"] = 1
                        data["ori_currency"] = merchant_trans_currency
                        data["ori_income"] = merchant_trans_amount
                        data["ori_channel_fee"] = commission_amount
                        data["ori_settlement"] = merchant_trans_amount - commission_amount
                        data["sett_currency"] = "USD"
                        data["file_md5"] = file_md5
                        data["file_name"] = file_name
                        data["remark"] = ''
                        data["special_note"] = ''

                        data_list.append(data)
                    except Exception as err2:
                        logger.error(">> fail to parse line! {} | {} | {}".format(self.channel, err2, line))
                # end for
            except Exception as err1:
                logger.error(">> fail to parse file! {} | {} | {}".format(self.channel, err1, file_name))
        # end for

        # save data
        sql = '''
            DELETE FROM db_mpay_channel.t_bill_settlement_mol_detail WHERE bill_month = '{}'
        '''.format(self.bill_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_channel", "t_bill_settlement_mol_detail")

    def do_job(self, bill_month, force=False):
        self.init(bill_month)
        self.download_file()

        data_path = "{}/{}".format(BillMolService.get_base_path(self.bill_month6), self.file_key)
        if force or not FileUtil.check_local_md5(data_path):
            self.parse_file(data_path)
            FileUtil.update_local_md5(data_path)

            self.msg_set.add("账单解析入库已完成： {} | {}".format(self.channel, self.bill_month6))
        else:
            logger.info("文件未变更，不需要解析：{}".format(data_path))

        self.finish()

    @staticmethod
    def task():
        usage_example = "Usage Example: *.py [data_month: YYYY-MM]"

        bill_month = Xutil.get_date_before(before_count=35, date_format='%Y-%m-%d')[0:7]
        if len(sys.argv) == 2:
            bill_month = sys.argv[1]
        if Xutil.is_invalid_date(bill_month, date_format="%Y-%m"):
            print("Invalid param! {}".format(usage_example))
            exit()

        # bill_month = "2022-05"
        flag_force = False
        obj = BillMolService()
        obj.do_job(bill_month, flag_force)


if "__main__" == __name__:
    BillMolService.task()

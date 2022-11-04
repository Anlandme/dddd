"""
    MPAY 渠道账单解析-UniPin
"""
import sys
from src import MailToConfig


class BillUnipinService(object):
    def __init__(self):
        self.channel = "unipin"
        self.file_key = "009_unipin"
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

    def save_data(self, data_list):
        sql = '''
            DELETE FROM db_mpay_channel.t_bill_settlement_unipin WHERE bill_month = '{}'
        '''.format(self.bill_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_channel", "t_bill_settlement_unipin")

    @staticmethod
    def get_base_path(bill_month6):
        base_path = "{}/data/download_settlement/{}".format(sys_path, bill_month6)
        FileUtil.mk_dirs(base_path)
        return base_path

    def download_file(self):
        base_path = BillUnipinService.get_base_path(self.bill_month6)
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

    def parse_file_base(self, data_path, sheet_name, currency):
        file_list = FileUtil.get_file_list(data_path, child=True, file_name_suffix=".xlsx")
        field_list = [
            'description', 'country', 'sub_merchant', 'sub_channel', 'currency', 'amount_charged_to_end_users',
            'vat_rate', 'vat_amount', 'amount_excluding_tax', 'percent_fee_rate', 'percent_fee_total',
            'per_transaction_fee', 'transaction_numbers', 'per_transaction_fee_total', 'payout_to_merchant_local',
            'exchange_rate', 'payout_to_merchant_usd'
        ]

        bill_type = "HS"
        data_list = []
        for file_path in file_list:
            file_md5 = FileUtil.get_file_md5(file_path)
            file_name = FileUtil.get_file_name(file_path)
            if file_name.startswith(".") or file_name.startswith("~"):
                continue
            if file_path.lower().find("/hs/") < 0:
                continue

            # 解析内容
            try:
                file_content = ExcelUtil.read_excel_xlrd(file_path, field_list, sheet_name=sheet_name)
                for line in file_content:
                    try:
                        description = str(line["description"]).strip().lower()
                        if not description.endswith("report"):
                            continue

                        # 原始字段
                        country = str(line["country"])
                        sub_merchant = str(line["sub_merchant"])
                        sub_channel = str(line["sub_channel"])
                        currency = str(line["currency"])
                        amount_charged_to_end_users = float(line["amount_charged_to_end_users"])
                        vat_rate = Xutil.parse_to_float(line["vat_rate"])
                        vat_amount = Xutil.parse_to_float(line["vat_amount"])
                        amount_excluding_tax = float(line["amount_excluding_tax"])
                        percent_fee_rate = float(line["percent_fee_rate"])
                        percent_fee_total = float(line["percent_fee_total"])
                        per_transaction_fee = Xutil.parse_to_float(line["per_transaction_fee"])
                        transaction_numbers = Xutil.parse_to_float(line["transaction_numbers"])
                        per_transaction_fee_total = Xutil.parse_to_float(line["per_transaction_fee_total"])
                        payout_to_merchant_local = float(line["payout_to_merchant_local"])
                        exchange_rate = float(line["exchange_rate"])
                        payout_to_merchant_usd = float(line["payout_to_merchant_usd"])

                        # 结果字段
                        data = {}
                        data["bill_type"] = bill_type
                        data["bill_month"] = self.bill_month
                        data["due_month"] = Xutil.get_month_next(self.bill_month)
                        data["due_date"] = Xutil.get_month_last_day(data["due_month"])
                        data["channel"] = self.channel
                        data["channel_product_no"] = ""
                        data["channel_product_name"] = "MidasPay"

                        data["sub_channel"] = sub_channel
                        data["country"] = currency[0:2]
                        data["tran_type"] = "PAY"
                        data["tran_currency"] = currency
                        data["tran_amount"] = amount_charged_to_end_users
                        data["tran_numbers"] = transaction_numbers
                        data["ori_currency"] = currency
                        data["ori_income"] = amount_charged_to_end_users
                        data["ori_channel_tax"] = vat_amount
                        data["ori_channel_fee"] = percent_fee_total + per_transaction_fee_total
                        data["ori_settlement"] = payout_to_merchant_local
                        data["sett_currency"] = "USD"

                        data["description"] = description
                        data["country"] = country
                        data["sub_merchant"] = sub_merchant
                        data["sub_channel"] = sub_channel
                        data["currency"] = currency
                        data["amount_charged_to_end_users"] = amount_charged_to_end_users
                        data["vat_rate"] = vat_rate
                        data["vat_amount"] = vat_amount
                        data["amount_excluding_tax"] = amount_excluding_tax
                        data["percent_fee_rate"] = percent_fee_rate
                        data["percent_fee_total"] = percent_fee_total
                        data["per_transaction_fee"] = per_transaction_fee
                        data["transaction_numbers"] = transaction_numbers
                        data["per_transaction_fee_total"] = per_transaction_fee_total
                        data["payout_to_merchant_local"] = payout_to_merchant_local
                        data["payout_to_merchant_usd"] = payout_to_merchant_usd
                        data["exchange_rate"] = exchange_rate

                        data["file_md5"] = file_md5
                        data["file_name"] = file_name
                        data["remark"] = ""
                        data["special_note"] = ""

                        data_list.append(data)
                    except Exception as err2:
                        logger.warn(">> fail to parse line! {} | {} | {}".format(self.channel, err2, line))
                # end for
            except Exception as err1:
                logger.error(">> fail to parse file! {} | {} | {}".format(self.channel, err1, file_path))
        # end for
        return data_list

    def do_job(self, bill_month, force=False):
        self.init(bill_month)
        self.download_file()

        data_path = "{}/{}".format(BillUnipinService.get_base_path(self.bill_month6), self.file_key)
        if force or not FileUtil.check_local_md5(data_path):
            data_list = []
            data_list.extend(self.parse_file_base(data_path, "ID", "IDR"))
            data_list.extend(self.parse_file_base(data_path, "MY", "MYR"))
            data_list.extend(self.parse_file_base(data_path, "TH", "THB"))
            self.save_data(data_list)
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
        obj = BillUnipinService()
        obj.do_job(bill_month, flag_force)


if "__main__" == __name__:
    BillUnipinService.task()

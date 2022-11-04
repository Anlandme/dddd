"""
    应收单
"""
from src import MailToConfig
from src import SpoaInfoData


class ReceivableService(object):
    def __init__(self):
        self.msg_set = set()
        self.sett_month = ''
        self.sett_month6 = ''
        self.bill_month = ''
        self.bill_month6 = ''
        self.spoa_info_dict: Dict[str, SpoaInfoData] = {}

    def init(self, sett_month):
        self.msg_set = set()
        self.sett_month = sett_month
        self.sett_month6 = sett_month.replace("-", "")
        self.bill_month = Xutil.get_month_before(self.sett_month)
        self.bill_month6 = self.bill_month.replace("-", "")
        self.spoa_info_dict = SpoaInfoData.get_spoa_info_dict(db_sett)

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> message info: {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData(">> message info", self.msg_set),
        ]
        mail_title = "【MPay月结】应收明细&应收单_{}".format(self.sett_month6)
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def gen_receivable_detail(self):
        """
            应收明细
        """
        sql = '''
            SELECT 'PLATFORM_FEE' AS Freceivable_type
                , Fsett_month
                , Fbill_month
                , Fdue_month
                , Fdue_date
                , Fchannel_id
                , Fchannel_name
                , Fchannel_ims
                , Fsubchannel_id
                , Fsubchannel_name
                , Fsett_type
                , Fbilling_type
                , Fplt_fee_type
                , Fmdm_id
                , Fmdm_name
                , Fchannel_mdm_id
                , Fchannel_mdm_name
                , Fmerchant_type
                , Fmerchant_mdm_id
                , Fmerchant_mdm_name
                , Fbiz_customer_no
                , Fbiz_customer_name
                , Ficp_code
                , Ficp_name
                , Fou_id
                , Fou_name
                , Fou_name_short
                , Fproduct_no
                , Fproduct_name
                , Foffer_id
                , Foffer_name
                , Fspoa_id
                , Fspoa_name
                , Fsett_group
                , Fsett_group_name
                , Fbusi_group
                , Fbusi_group_name
                , Fdept
                , Fdept_name
                , Fcountry
                , Fori_currency
                , Fori_income
                , Fori_settlement
                , Fori_sett_currency_rate
                , Fsett_currency
                , Fsett_income
                , Fsett_settlement
                , Fchannel_contract_no
                , Fmerchant_contract_no
                , Fdata_source_no
                , Fdata_source_name
            FROM db_sett_oversea.t_channel_month_plt_bill
            WHERE Fsett_month = '{}'

            UNION ALL
            SELECT 'COLLECTION' AS Freceivable_type
                , Fsett_month
                , Fbill_month
                , Fdue_month
                , Fdue_date
                , Fchannel_id
                , Fchannel_name
                , Fchannel_ims
                , Fsubchannel_id
                , Fsubchannel_name
                , Fsett_type
                , Fbilling_type
                , '' AS Fplt_fee_type
                , Fmdm_id
                , Fmdm_name
                , Fchannel_mdm_id
                , Fchannel_mdm_name
                , Fmerchant_type
                , Fmerchant_mdm_id
                , Fmerchant_mdm_name
                , Fbiz_customer_no
                , Fbiz_customer_name
                , Ficp_code
                , Ficp_name
                , Fou_id
                , Fou_name
                , Fou_name_short
                , Fproduct_no
                , Fproduct_name
                , Foffer_id
                , Foffer_name
                , Fspoa_id
                , Fspoa_name
                , Fsett_group
                , Fsett_group_name
                , Fbusi_group
                , Fbusi_group_name
                , Fdept
                , Fdept_name
                , Fcountry
                , Fori_currency
                , Fori_income
                , Fori_settlement
                , Fori_sett_currency_rate
                , Fsett_currency
                , Fsett_income
                , Fsett_settlement
                , Fchannel_contract_no
                , Fmerchant_contract_no
                , Fdata_source_no
                , Fdata_source_name
            FROM db_sett_oversea.t_channel_month_agency_bill
            WHERE Fsett_month = '{}'
        '''.format(self.sett_month, self.sett_month)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            biz_type = "MidasPay"
            due_date = line["Fdue_date"]
            due_month = line["Fdue_month"]
            sett_type = str(line["Fsett_type"])
            plt_fee_type = line["Fplt_fee_type"]
            receivable_type = line["Freceivable_type"]

            # 账期
            period_type = "M1"
            if sett_type == "coda_60":
                period_type = "M2"
            elif sett_type == "coda_90":
                period_type = "M3"

            receivable_detail_no = Xutil.md5_str(
                Xutil.link_words(
                    biz_type, period_type, receivable_type, plt_fee_type, due_date, due_month
                    , line["Fsett_month"], line["Fbill_month"], line["Fchannel_name"], line["Fsubchannel_name"]
                    , line["Fchannel_mdm_id"], line["Fbiz_customer_no"], line["Fou_id"], line["Fproduct_no"]
                    , line["Fsett_group"], line["Fcountry"], line["Fori_currency"], line["Fsett_currency"]
                    , line["Fchannel_contract_no"], line["Fmerchant_contract_no"]
                ), case="UPPER"
            )
            receivable_detail_no = "RCD{}".format(receivable_detail_no)

            receivable_no = Xutil.md5_str(
                Xutil.link_words(
                    biz_type, period_type, receivable_type, plt_fee_type, due_date, due_month
                    , line["Fsett_month"], line["Fbill_month"], line["Fchannel_name"], line["Fchannel_mdm_id"]
                    , line["Fbiz_customer_no"], line["Fou_id"], line["Fproduct_no"], line["Fsett_group"]
                    , line["Fsett_currency"], line["Fchannel_contract_no"], line["Fmerchant_contract_no"]
                ), case="UPPER"
            )
            receivable_no = "RCM{}".format(receivable_no)

            data = {}
            data["receivable_detail_no"] = receivable_detail_no
            data["receivable_no"] = receivable_no
            data["sett_month"] = line["Fsett_month"]
            data["bill_month"] = line["Fbill_month"]
            data["due_month"] = line["Fdue_month"]
            data["due_date"] = line["Fdue_date"]
            data["channel_id"] = line["Fchannel_id"]
            data["channel_name"] = line["Fchannel_name"]
            data["subchannel_id"] = line["Fsubchannel_id"]
            data["subchannel_name"] = line["Fsubchannel_name"]
            data["biz_type"] = biz_type
            data["period_type"] = period_type
            data["receivable_type"] = receivable_type
            data["plt_fee_type"] = plt_fee_type
            data["mdm_id"] = line["Fchannel_mdm_id"]
            data["mdm_name"] = line["Fchannel_mdm_name"]
            data["biz_customer_no"] = line["Fbiz_customer_no"]
            data["biz_customer_name"] = line["Fbiz_customer_name"]
            data["merchant_type"] = line["Fmerchant_type"]
            data["merchant_mdm_id"] = line["Fmerchant_mdm_id"]
            data["merchant_mdm_name"] = line["Fmerchant_mdm_name"]
            data["icp_code"] = line["Ficp_code"]
            data["icp_name"] = line["Ficp_name"]
            data["ou_id"] = line["Fou_id"]
            data["ou_name"] = line["Fou_name"]
            data["ou_name_short"] = line["Fou_name_short"]
            data["product_no"] = line["Fproduct_no"]
            data["product_name"] = line["Fproduct_name"]
            data["offer_id"] = line["Foffer_id"]
            data["offer_name"] = line["Foffer_name"]
            data["spoa_id"] = line["Fspoa_id"]
            data["spoa_name"] = line["Fspoa_name"]
            data["sett_group"] = line["Fsett_group"]
            data["sett_group_name"] = line["Fsett_group_name"]
            data["busi_group"] = line["Fbusi_group"]
            data["busi_group_name"] = line["Fbusi_group_name"]
            data["dept"] = line["Fdept"]
            data["dept_name"] = line["Fdept_name"]
            data["country"] = line["Fcountry"]
            data["ori_currency"] = line["Fori_currency"]
            data["ori_income"] = line["Fori_income"]
            data["ori_settlement"] = line["Fori_settlement"]
            data["ori_sett_currency_rate"] = line["Fori_sett_currency_rate"]
            data["sett_currency"] = line["Fsett_currency"]
            data["sett_income"] = line["Fsett_income"]
            data["sett_settlement"] = line["Fsett_settlement"]
            data["channel_contract_no"] = line["Fchannel_contract_no"]
            data["merchant_contract_no"] = line["Fmerchant_contract_no"]
            data["data_source_no"] = line["Fdata_source_no"]
            data["data_source_name"] = line["Fdata_source_name"]

            data_list.append(data)
        # end for

        # save data
        sql = '''
            delete from db_sett_oversea_accounts.t_receivable_detail where sett_month = '{}'
        '''.format(self.sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea_accounts", "t_receivable_detail")

    def gen_receivable_info(self):
        """
            应收单
        """
        sql = '''
            SELECT receivable_no
                , sett_month
                , bill_month
                , due_month
                , due_date
                , receivable_type
                , plt_fee_type
                , product_no
                , product_name
                , offer_id
                , offer_name
                , sett_group
                , sett_group_name
                , channel_name as channel
                , biz_type
                , period_type
                , ou_id
                , ou_name
                , ou_name_short
                , mdm_id
                , mdm_name
                , merchant_type
                , merchant_mdm_id
                , merchant_mdm_name
                , icp_code
                , icp_name
                , biz_customer_no
                , biz_customer_name
                , channel_contract_no
                , merchant_contract_no
                , sett_currency as currency
                , sum(sett_settlement) as receivable_amount
                , sum(sett_settlement) as receivable_balance
                , sum(exchange_difference_settlement) as exchange_difference
            FROM db_sett_oversea_accounts.t_receivable_detail
            WHERE sett_month = '{}'
            GROUP BY receivable_no
        '''.format(self.sett_month)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            data = {}
            data["receivable_no"] = line["receivable_no"]
            data["sett_month"] = line["sett_month"]
            data["bill_month"] = line["bill_month"]
            data["due_month"] = line["due_month"]
            data["due_date"] = line["due_date"]
            data["receivable_type"] = line["receivable_type"]
            data["plt_fee_type"] = line["plt_fee_type"]
            data["status"] = "NEW"
            data["channel"] = line["channel"]
            data["biz_type"] = line["biz_type"]
            data["period_type"] = line["period_type"]
            data["ou_id"] = line["ou_id"]
            data["ou_name"] = line["ou_name"]
            data["ou_name_short"] = line["ou_name_short"]
            data["product_no"] = line["product_no"]
            data["product_name"] = line["product_name"]
            data["offer_id"] = line["offer_id"]
            data["offer_name"] = line["offer_name"]
            data["sett_group"] = line["sett_group"]
            data["sett_group_name"] = line["sett_group_name"]
            data["mdm_id"] = line["mdm_id"]
            data["mdm_name"] = line["mdm_name"]
            data["merchant_type"] = line["merchant_type"]
            data["merchant_mdm_id"] = line["merchant_mdm_id"]
            data["merchant_mdm_name"] = line["merchant_mdm_name"]
            data["icp_code"] = line["icp_code"]
            data["icp_name"] = line["icp_name"]
            data["data_date"] = Xutil.get_month_last_day(line["bill_month"])
            data["work_date"] = Xutil.get_date_current(date_format="%Y-%m-%d")
            data["work_type"] = ""
            data["currency"] = line["currency"]
            data["receivable_amount"] = line["receivable_amount"]
            data["receivable_balance"] = line["receivable_balance"]
            data["exchange_difference_flag"] = "Y"
            data["exchange_difference"] = line["exchange_difference"]
            data["other_spoilage"] = 0
            data["biz_order_no"] = ""
            data["biz_customer_no"] = line["biz_customer_no"]
            data["biz_customer_name"] = line["biz_customer_name"]
            data["channel_contract_no"] = line["channel_contract_no"]
            data["merchant_contract_no"] = line["merchant_contract_no"]
            data["remark"] = ""
            data["create_person"] = "SYSTEM"
            data["update_person"] = "SYSTEM"

            data_list.append(data)
        # end for
        sql = '''
            delete from db_sett_oversea_accounts.t_receivable_info where sett_month = '{}'
        '''.format(self.sett_month)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea_accounts", "t_receivable_info")

    def do_job(self, sett_month):
        self.init(sett_month)
        self.gen_receivable_detail()
        self.gen_receivable_info()
        self.finish()

    @staticmethod
    def task():
        usage_example = "Usage Example: *.py [sett_month: YYYY-MM]"

        sett_month = ""
        if len(sys.argv) == 2:
            sett_month = sys.argv[1]
        if Xutil.is_invalid_date(sett_month, date_format="%Y-%m"):
            print("Invalid Param! {}".format(usage_example))
            exit()

        # target_month = Xutil.get_date_before(before_count=12)[0:7]
        # if sett_month != target_month and ConfigReader.is_prod():
        #     print("Invalid Period! sett_month: {}, target_month: {}".format(sett_month, target_month))
        #     exit()

        obj = ReceivableService()
        obj.do_job(sett_month)


if "__main__" == __name__:
    ReceivableService.task()

"""
    记账凭证：HM代收付模式引入的部分场景集团IMS不支持账务处理，需要业务侧（Midas）解决

    AR BP01001	【流水期间】代收-暂估应收

    AR BP01012  【核销期间】代收-汇兑损益
    AR BP01013  【核销期间】代收-核销结果
    AP BP02008	【核销期间】应收应付互抵（内部商户）

    AR BP01004	【账单期间】代收-暂估冲销
    AR BP01005	【账单期间】代收-账单应收
    AP BP02007	【账单期间】成本确认（内部商户）
"""
from src import OUInfoData
from src import MailToConfig
from src import BookkeepingVoucherData
from src import BookkeepingTemplateData
from src import MerchantInfoData


class AcctBookkeepingService(object):
    def __init__(self):
        self.msg_set = set()
        self.bookkeeping_period = ''
        self.bookkeeping_period6 = ''
        self.ou_info_dict: Dict[str, OUInfoData] = {}
        self.merchant_info_dict: Dict[str, MerchantInfoData] = {}
        self.bookkeeping_template_dict: Dict[str, BookkeepingTemplateData] = {}

    def init(self, bookkeeping_period):
        self.msg_set = set()
        self.bookkeeping_period = bookkeeping_period
        self.bookkeeping_period6 = str(bookkeeping_period).replace('-', '')
        self.ou_info_dict = OUInfoData.get_ou_info_dict(db_midas_merchant)
        self.bookkeeping_template_dict = BookkeepingTemplateData.get_bookkeeping_template_dict(db_sett)

        flag, msg, self.merchant_info_dict = MerchantInfoData.get_merchant_rules_dict(
            db_midas_merchant, self.ou_info_dict)
        self.msg_set.update(msg)

    def finish(self):
        if len(self.msg_set) > 0:
            logger.error(">> message info! {}".format(self.msg_set))

        # 告警邮件
        mail_content_list = [
            MailContentData("message info", self.msg_set)
        ]
        mail_to = MailToConfig.get_mail_to(db_sett, __file__)
        mail_title = "【MPay月结_{}】记账凭证_{}".format(sys_tag, self.bookkeeping_period6)
        MailClient.send_mail_v2(mail_title, mail_to=mail_to, mail_content_list=mail_content_list)

    def save_data(self, template_no, data_list):
        sql = '''
            delete from db_sett_oversea.t_bookkeeping_voucher 
            where bookkeeping_period = '{}' and process_no = '{}'
        '''.format(self.bookkeeping_period, template_no)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_sett_oversea", "t_bookkeeping_voucher")

    # AR BP01001	【流水期间】代收-暂估应收
    def bookkeeping_esti_1001(self):
        """
            BP01001	代收-暂估应收
        """
        template_no = "BP01001"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        sql = '''
            select sett_month, data_month, bill_month, merchant_id, merchant_name
                , channel_mdm_id, channel_mdm_name, channel_contract_no
                , merchant_type, merchant_mdm_id, merchant_mdm_name, merchant_ou_id
                , merchant_ou_name, merchant_ou_short, merchant_contract_no, sett_currency
                , sum(sett_income) as sett_income
                , sum(sett_refund) as sett_refund
                , 0 as sett_plt_tax_amount
                , sum(sett_channel_tax) as sett_channel_tax_amount
                , sum(sett_channel_fee) as sett_channel_fee_total
                , sum(sett_merchant_fee) as sett_merchant_fee_total
                , sum(sett_plt_fee) as sett_plt_fee_total
            from db_mpay_income.t_mpay_esti_base
            where sett_month = '{}'
            group by sett_month, data_month, bill_month, merchant_id, merchant_name
                , channel_mdm_id, channel_mdm_name, channel_contract_no
                , merchant_type, merchant_mdm_id, merchant_mdm_name, merchant_ou_id
                , merchant_ou_name, merchant_ou_short, merchant_contract_no, sett_currency
        '''.format(self.bookkeeping_period)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            sett_income = float(line["sett_income"])
            sett_refund = float(line["sett_refund"])
            sett_channel_tax_amount = float(line["sett_channel_tax_amount"])
            sett_channel_fee_total = float(line["sett_channel_fee_total"])
            sett_plt_fee_total = float(line["sett_plt_fee_total"])
            sett_settlement = \
                sett_income - sett_refund - sett_channel_tax_amount - sett_channel_fee_total - sett_plt_fee_total

            data = BookkeepingVoucherData()
            data.update_template_info(bookkeeping_template_info)

            data.bookkeeping_date = Xutil.get_date_current(date_format="%Y-%m-%d")
            data.bookkeeping_period = self.bookkeeping_period
            data.sett_currency = line["sett_currency"]
            data.sett_amount_dr = sett_settlement
            data.sett_amount_cr = sett_settlement

            data.sett_month = self.bookkeeping_period
            data.data_month = line["data_month"]
            data.bill_month = line["bill_month"]
            data.product_id = line["merchant_id"]
            data.product_name = line["merchant_name"]
            data.channel_mdm_id = line["channel_mdm_id"]
            data.channel_mdm_name = line["channel_mdm_name"]
            data.channel_contract_no = line["channel_contract_no"]
            data.merchant_type = line["merchant_type"]
            data.merchant_mdm_id = line["merchant_mdm_id"]
            data.merchant_mdm_name = line["merchant_mdm_name"]
            data.merchant_contract_no = line["merchant_contract_no"]

            data_list.append(data)
        # end for

        # save data
        self.save_data(template_no, data_list)
        return True, "SUCCESS"

    # AR BP01004	【账单期间】代收-暂估冲销
    def bookkeeping_bill_1004(self):
        """
            BP01004	代收-暂估冲销 (记负值)
            BP01001	代收-暂估应收（更新状态）
        """
        template_no = "BP01004"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        charge_off_date_begin = Xutil.get_date_before(before_count=10)
        sql = '''
            select * from db_sett_oversea.t_bookkeeping_voucher
            WHERE process_no = 'BP01001' AND bill_month <= '{}' 
                AND (charge_off_status = '' OR charge_off_date >= '{}')
        '''.format(self.bookkeeping_period, charge_off_date_begin)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            del line["id"]
            del line["modify_time"]

            line["sett_month"] = self.bookkeeping_period
            line["bookkeeping_date"] = Xutil.get_date_current(date_format="%Y-%m-%d")
            line["bookkeeping_period"] = self.bookkeeping_period

            line["voucher_no"] = BookkeepingVoucherData.get_voucher_no_v2()
            line["process_no"] = bookkeeping_template_info.template_no
            line["process_name"] = bookkeeping_template_info.template_name
            line["finance_type"] = bookkeeping_template_info.template_type
            line["voucher_type"] = bookkeeping_template_info.voucher_type
            line["org_name"] = bookkeeping_template_info.org_name
            line["business_category"] = bookkeeping_template_info.business_category
            line["business_type"] = bookkeeping_template_info.business_type

            line["dr_cost_center_no"] = bookkeeping_template_info.dr_cost_center_no
            line["dr_cost_center_name"] = bookkeeping_template_info.dr_cost_center_name
            line["dr_account_no"] = bookkeeping_template_info.dr_account_no
            line["dr_account_name"] = bookkeeping_template_info.dr_account_name
            line["dr_product_no"] = bookkeeping_template_info.dr_product_no
            line["dr_product_name"] = bookkeeping_template_info.dr_product_name
            line["cr_cost_center_no"] = bookkeeping_template_info.cr_cost_center_no
            line["cr_cost_center_name"] = bookkeeping_template_info.cr_cost_center_name
            line["cr_account_no"] = bookkeeping_template_info.cr_account_no
            line["cr_account_name"] = bookkeeping_template_info.cr_account_name
            line["cr_product_no"] = bookkeeping_template_info.cr_product_no
            line["cr_product_name"] = bookkeeping_template_info.cr_product_name
            line["mdm_id"] = bookkeeping_template_info.mdm_id
            line["mdm_name"] = bookkeeping_template_info.mdm_name

            line["sett_amount_dr"] = -float(line["sett_amount_dr"])
            line["sett_amount_cr"] = -float(line["sett_amount_cr"])
            line["operate_type"] = "CHARGE_OFF"
            line["charge_off_status"] = "Y"
            line["approval_status"] = "1"
            line["approval_reason"] = ""

            line["account_dr"] = bookkeeping_template_info.dr_account_name
            line["account_cr"] = bookkeeping_template_info.cr_account_name
            line["abstract"] = bookkeeping_template_info.template_name

            data_list.append(line)
        # end for
        self.save_data(template_no, data_list)

        # 更新冲销状态
        charge_off_date = Xutil.get_date_current(date_format="%Y-%m-%d")
        sql = '''
            UPDATE db_sett_oversea.t_bookkeeping_voucher
            SET operate_type = 'CHARGE_OFF', charge_off_status = 'Y', charge_off_date = '{}'
            WHERE process_no = 'BP01001' AND bill_month <= '{}' 
                AND (charge_off_status = '' OR charge_off_date >= '{}')
        '''.format(charge_off_date, self.bookkeeping_period, charge_off_date_begin)
        db_sett.update(sql)
        return True, "SUCCESS"

    # AR BP01005	【账单期间】代收-账单应收
    def bookkeeping_bill_1005(self):
        template_no = "BP01005"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        sql = '''
            select sett_month, bill_month, merchant_id, merchant_name
                , channel_mdm_id, channel_mdm_name, channel_contract_no
                , merchant_type, merchant_mdm_id, merchant_mdm_name, merchant_ou_id
                , merchant_ou_name, merchant_ou_short, merchant_contract_no, sett_currency
                , sum(sett_income) as sett_income
                , sum(sett_refund) as sett_refund
                , 0 as sett_plt_tax_amount
                , sum(sett_channel_tax) as sett_channel_tax_amount
                , sum(sett_channel_fee) as sett_channel_fee_total
                , sum(sett_merchant_fee) as sett_merchant_fee_total
                , sum(sett_plt_fee) as sett_plt_fee_total
            from db_mpay_income.t_mpay_bill_base_merchant
            where sett_month = '{}'
            group by sett_month, bill_month, merchant_id, merchant_name
                , channel_mdm_id, channel_mdm_name, channel_contract_no
                , merchant_type, merchant_mdm_id, merchant_mdm_name, merchant_ou_id
                , merchant_ou_name, merchant_ou_short, merchant_contract_no, sett_currency
        '''.format(self.bookkeeping_period)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            sett_income = float(line["sett_income"])
            sett_refund = float(line["sett_refund"])
            sett_channel_tax_amount = float(line["sett_channel_tax_amount"])
            sett_channel_fee_total = float(line["sett_channel_fee_total"])
            sett_plt_fee_total = float(line["sett_plt_fee_total"])
            sett_settlement = \
                sett_income - sett_refund - sett_channel_tax_amount - sett_channel_fee_total - sett_plt_fee_total

            data = BookkeepingVoucherData()
            data.update_template_info(bookkeeping_template_info)

            data.bookkeeping_date = Xutil.get_date_current(date_format="%Y-%m-%d")
            data.bookkeeping_period = self.bookkeeping_period
            data.sett_currency = line["sett_currency"]
            data.sett_amount_dr = sett_settlement
            data.sett_amount_cr = sett_settlement

            data.sett_month = self.bookkeeping_period
            data.data_month = line["bill_month"]
            data.bill_month = line["bill_month"]
            data.product_id = line["merchant_id"]
            data.product_name = line["merchant_id"]
            data.channel_mdm_id = line["channel_mdm_id"]
            data.channel_mdm_name = line["channel_mdm_name"]
            data.channel_contract_no = line["channel_contract_no"]
            data.merchant_type = line["merchant_type"]
            data.merchant_mdm_id = line["merchant_mdm_id"]
            data.merchant_mdm_name = line["merchant_mdm_name"]
            data.merchant_contract_no = line["merchant_contract_no"]

            data_list.append(data)
        # end for

        # save data
        self.save_data(template_no, data_list)
        return True, "SUCCESS"

    # AP BP02007	【账单期间】内部商户-成本确认
    def bookkeeping_bill_2007(self):
        """
            内部商户付米大师平台手续费
        :return:
        """
        template_no = "BP02007"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        sql = '''
            select sett_month, bill_month, merchant_id, merchant_name
                , channel_mdm_id, channel_mdm_name, channel_contract_no
                , merchant_type, merchant_mdm_id, merchant_mdm_name, merchant_ou_id
                , merchant_ou_name, merchant_ou_short, merchant_contract_no, sett_currency
                , sum(sett_plt_fee) as sett_plt_fee_total
            from db_mpay_income.t_mpay_bill_base_merchant
            where sett_month = '{}' and merchant_type = 'INTERNAL'
            group by sett_month, bill_month, merchant_id, merchant_name
                , channel_mdm_id, channel_mdm_name, channel_contract_no
                , merchant_type, merchant_mdm_id, merchant_mdm_name, merchant_ou_id
                , merchant_ou_name, merchant_ou_short, merchant_contract_no, sett_currency
        '''.format(self.bookkeeping_period)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            # 商户信息
            merchant_contract_no = str(line["merchant_contract_no"]).strip()
            if merchant_contract_no in self.merchant_info_dict:
                merchant_info = self.merchant_info_dict[merchant_contract_no]
            else:
                self.msg_set.add(">> missing merchant info: {}".format(merchant_contract_no))
                continue

            data = BookkeepingVoucherData()
            data.update_template_info(bookkeeping_template_info)

            # org_name、cost_center、coa 取自商户；
            data.org_name = merchant_info.merchant_ou_short
            data.dr_product_no = merchant_info.merchant_coa_no
            data.dr_product_name = merchant_info.merchant_coa_name
            data.dr_cost_center_no = merchant_info.merchant_cost_no
            data.dr_cost_center_name = merchant_info.merchant_cost_name

            data.cr_product_no = merchant_info.merchant_coa_no
            data.cr_product_name = merchant_info.merchant_coa_name
            data.cr_cost_center_no = merchant_info.merchant_cost_no
            data.cr_cost_center_name = merchant_info.merchant_cost_name

            data.bookkeeping_date = Xutil.get_date_current(date_format="%Y-%m-%d")
            data.bookkeeping_period = self.bookkeeping_period
            data.sett_currency = line["sett_currency"]
            data.sett_amount_dr = float(line["sett_plt_fee_total"])
            data.sett_amount_cr = float(line["sett_plt_fee_total"])

            data.sett_month = self.bookkeeping_period
            data.data_month = line["bill_month"]
            data.bill_month = line["bill_month"]
            data.product_id = line["merchant_id"]
            data.product_name = line["merchant_name"]
            data.channel_mdm_id = line["channel_mdm_id"]
            data.channel_mdm_name = line["channel_mdm_name"]
            data.channel_contract_no = line["channel_contract_no"]
            data.merchant_type = line["merchant_type"]
            data.merchant_mdm_id = line["merchant_mdm_id"]
            data.merchant_mdm_name = line["merchant_mdm_name"]
            data.merchant_contract_no = line["merchant_contract_no"]

            data_list.append(data)
        # end for

        # save data
        self.save_data(template_no, data_list)
        return True, "SUCCESS"

    # AR BP01012  【核销期间】代收-汇兑损益
    def bookkeeping_writeoff_1012(self):
        """
            BP01012	代收-汇兑损益（核销结果表）
            取汇损金额
        """
        template_no = "BP01012"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        date_begin = "{}-04".format(self.bookkeeping_period)
        date_end = "{}-03".format(Xutil.get_month_next(self.bookkeeping_period))
        sql = '''
            SELECT A.write_off_no
                , A.receivable_no
                , A.write_off_currency
                , A.write_off_collection_amount
                , A.status
                , B.receivable_amount
                , B.exchange_difference
                , B.sett_month
                , B.bill_month
                , B.product_no
                , B.product_name
                , B.offer_id
                , B.offer_name
                , B.mdm_id as channel_mdm_id
                , B.mdm_name as channel_mdm_name
                , B.merchant_type
                , B.merchant_mdm_id
                , B.merchant_mdm_name
                , B.channel_contract_no
                , B.merchant_contract_no
            FROM db_sett_oversea_accounts.t_write_off_info A
            LEFT JOIN db_sett_oversea_accounts.t_receivable_info B
                ON A.receivable_no = B.receivable_no
            WHERE B.receivable_type = 'COLLECTION' AND A.write_off_date BETWEEN '{}' AND '{}'
        '''.format(date_begin, date_end)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            write_off_no = line["write_off_no"]
            receivable_amount = float(line["receivable_amount"])
            exchange_difference = float(line["exchange_difference"])
            write_off_amount = float(line["write_off_collection_amount"])
            if (receivable_amount + exchange_difference) == 0:
                self.msg_set.add(">> 应收金额未0，无法拆分汇损: {}".format(write_off_no))
                bookkeeping_amount = exchange_difference
            else:
                bookkeeping_amount = exchange_difference * write_off_amount / (receivable_amount + exchange_difference)

            data = BookkeepingVoucherData()
            data.update_template_info(bookkeeping_template_info)

            data.bookkeeping_date = Xutil.get_date_current(date_format="%Y-%m-%d")
            data.bookkeeping_period = self.bookkeeping_period
            data.sett_currency = line["write_off_currency"]
            data.sett_amount_dr = bookkeeping_amount
            data.sett_amount_cr = bookkeeping_amount

            data.sett_month = self.bookkeeping_period
            data.data_month = line["bill_month"]
            data.bill_month = line["bill_month"]
            data.offer_id = line["offer_id"]
            data.offer_name = line["offer_name"]
            data.product_id = line["product_no"]
            data.product_name = line["product_name"]
            data.channel_mdm_id = line["channel_mdm_id"]
            data.channel_mdm_name = line["channel_mdm_name"]
            data.channel_contract_no = line["channel_contract_no"]
            data.merchant_type = line["merchant_type"]
            data.merchant_mdm_id = line["merchant_mdm_id"]
            data.merchant_mdm_name = line["merchant_mdm_name"]
            data.merchant_contract_no = line["merchant_contract_no"]
            data.data_source_no = line["write_off_no"]

            data_list.append(data)
        # end for

        # save data
        self.save_data(template_no, data_list)
        return True, "SUCCESS"

    # AR BP01013  【核销期间】代收-核销结果
    def bookkeeping_writeoff_1013(self):
        """
            BP01013	代收-核销（核销结果表）
            取核销金额
        """
        template_no = "BP01013"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        date_begin = "{}-04".format(self.bookkeeping_period)
        date_end = "{}-03".format(Xutil.get_month_next(self.bookkeeping_period))
        sql = '''
            SELECT A.write_off_no
                , A.receivable_no
                , A.write_off_currency
                , A.write_off_collection_amount
                , A.status
                , B.receivable_amount
                , B.exchange_difference
                , B.sett_month
                , B.bill_month
                , B.product_no
                , B.product_name
                , B.offer_id
                , B.offer_name
                , B.mdm_id as channel_mdm_id
                , B.mdm_name as channel_mdm_name
                , B.merchant_type
                , B.merchant_mdm_id
                , B.merchant_mdm_name
                , B.channel_contract_no
                , B.merchant_contract_no
            FROM db_sett_oversea_accounts.t_write_off_info A
            LEFT JOIN db_sett_oversea_accounts.t_receivable_info B
                ON A.receivable_no = B.receivable_no
            WHERE B.receivable_type = 'COLLECTION' AND A.write_off_date BETWEEN '{}' AND '{}'
        '''.format(date_begin, date_end)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            bookkeeping_amount = float(line["write_off_collection_amount"])

            data = BookkeepingVoucherData()
            data.update_template_info(bookkeeping_template_info)

            data.bookkeeping_date = Xutil.get_date_current(date_format="%Y-%m-%d")
            data.bookkeeping_period = self.bookkeeping_period
            data.sett_currency = line["write_off_currency"]
            data.sett_amount_dr = bookkeeping_amount
            data.sett_amount_cr = bookkeeping_amount

            data.sett_month = self.bookkeeping_period
            data.data_month = line["bill_month"]
            data.bill_month = line["bill_month"]
            data.offer_id = line["offer_id"]
            data.offer_name = line["offer_name"]
            data.product_id = line["product_no"]
            data.product_name = line["product_name"]
            data.channel_mdm_id = line["channel_mdm_id"]
            data.channel_mdm_name = line["channel_mdm_name"]
            data.channel_contract_no = line["channel_contract_no"]
            data.merchant_type = line["merchant_type"]
            data.merchant_mdm_id = line["merchant_mdm_id"]
            data.merchant_mdm_name = line["merchant_mdm_name"]
            data.merchant_contract_no = line["merchant_contract_no"]
            data.data_source_no = line["write_off_no"]

            data_list.append(data)
        # end for

        # save data
        self.save_data(template_no, data_list)
        return True, "SUCCESS"

    # AP BP02008	【核销期间】内部商户-应收应付互抵
    def bookkeeping_writeoff_2008(self):
        """
            BP02008	内部商户-应收应付互抵(核销的平台费)
            核销金额 - 汇损金额
        """
        template_no = "BP02008"
        if template_no not in self.bookkeeping_template_dict:
            message = ">> missing bookkeeping template info: {}".format(template_no)
            self.msg_set.add(message)
            return False, message
        bookkeeping_template_info = self.bookkeeping_template_dict[template_no]

        date_begin = "{}-04".format(self.bookkeeping_period)
        date_end = "{}-03".format(Xutil.get_month_next(self.bookkeeping_period))
        sql = '''
            SELECT A.write_off_no
                , A.receivable_no
                , A.write_off_currency
                , A.write_off_collection_amount
                , A.status
                , B.receivable_amount
                , B.exchange_difference
                , B.sett_month
                , B.bill_month
                , B.product_no
                , B.product_name
                , B.offer_id
                , B.offer_name
                , B.mdm_id as channel_mdm_id
                , B.mdm_name as channel_mdm_name
                , B.merchant_type
                , B.merchant_mdm_id
                , B.merchant_mdm_name
                , B.channel_contract_no
                , B.merchant_contract_no
            FROM db_sett_oversea_accounts.t_write_off_info A
            LEFT JOIN db_sett_oversea_accounts.t_receivable_info B
                ON A.receivable_no = B.receivable_no
            WHERE A.write_off_date BETWEEN '{}' AND '{}'
                AND B.receivable_type = 'PLATFORM_FEE' AND B.merchant_type = 'INTERNAL'
                AND (biz_customer_no <> '' or plt_fee_type = 'CHANNEL')
        '''.format(date_begin, date_end)
        db_ret = db_sett.query(sql)

        data_list = []
        for line in db_ret.data:
            # 商户信息
            merchant_contract_no = str(line["merchant_contract_no"]).strip()
            if merchant_contract_no in self.merchant_info_dict:
                merchant_info = self.merchant_info_dict[merchant_contract_no]
            else:
                self.msg_set.add(">> missing merchant info: {}".format(merchant_contract_no))
                continue

            # 记账金额
            write_off_no = line["write_off_no"]
            write_off_amount = float(line["write_off_collection_amount"])
            receivable_amount = float(line["receivable_amount"])
            exchange_difference = float(line["exchange_difference"])
            if (receivable_amount + exchange_difference) == 0:
                self.msg_set.add(">> 应收金额未0，无法拆分汇损: {}".format(write_off_no))
                bookkeeping_amount = -exchange_difference
            else:
                bookkeeping_amount = write_off_amount - \
                                     exchange_difference * write_off_amount / (receivable_amount + exchange_difference)

            data = BookkeepingVoucherData()
            data.update_template_info(bookkeeping_template_info)

            # org_name、cost_center 取自商户；
            data.org_name = merchant_info.merchant_ou_short
            data.dr_cost_center_no = merchant_info.merchant_cost_no
            data.dr_cost_center_name = merchant_info.merchant_cost_name
            data.cr_cost_center_no = merchant_info.merchant_cost_no
            data.cr_cost_center_name = merchant_info.merchant_cost_name

            # 基础字段
            data.bookkeeping_date = Xutil.get_date_current(date_format="%Y-%m-%d")
            data.bookkeeping_period = self.bookkeeping_period
            data.sett_currency = line["write_off_currency"]
            data.sett_amount_dr = bookkeeping_amount
            data.sett_amount_cr = bookkeeping_amount
            data.sett_month = self.bookkeeping_period
            data.data_month = line["bill_month"]
            data.bill_month = line["bill_month"]
            data.offer_id = line["offer_id"]
            data.offer_name = line["offer_name"]
            data.product_id = line["product_no"]
            data.product_name = line["product_name"]
            data.channel_mdm_id = line["channel_mdm_id"]
            data.channel_mdm_name = line["channel_mdm_name"]
            data.channel_contract_no = line["channel_contract_no"]
            data.merchant_type = line["merchant_type"]
            data.merchant_mdm_id = line["merchant_mdm_id"]
            data.merchant_mdm_name = line["merchant_mdm_name"]
            data.merchant_contract_no = line["merchant_contract_no"]
            data.data_source_no = line["write_off_no"]

            data_list.append(data)
        # end for

        # save data
        self.save_data(template_no, data_list)
        return True, "SUCCESS"

    def do_job_writeoff(self, bookkeeping_period):
        self.init(bookkeeping_period)
        self.bookkeeping_writeoff_1012()
        self.bookkeeping_writeoff_1013()
        self.bookkeeping_writeoff_2008()
        self.finish()

    def do_job(self, sett_month, acct_type=None):
        """
        :param sett_month: 月结月份｜YYYY-MM
        :param acct_type: 账务类型（ESTIMATE、BILL、WRITE_OFF）
        """
        acct_type = str(acct_type).upper()
        self.init(sett_month)
        if acct_type == "ESTIMATE":
            self.bookkeeping_esti_1001()
        elif acct_type == "BILL":
            self.bookkeeping_bill_1004()
            self.bookkeeping_bill_1005()
            self.bookkeeping_bill_2007()
        elif acct_type == "WRITE_OFF":
            self.bookkeeping_writeoff_1012()
            self.bookkeeping_writeoff_1013()
            self.bookkeeping_writeoff_2008()
        else:
            self.bookkeeping_esti_1001()
            self.bookkeeping_bill_1004()
            self.bookkeeping_bill_1005()
            self.bookkeeping_bill_2007()
            self.bookkeeping_writeoff_1012()
            self.bookkeeping_writeoff_1013()
            self.bookkeeping_writeoff_2008()
        self.finish()

    @staticmethod
    def task():
        sett_month = "2022-06"
        if len(sys.argv) == 2:
            sett_month = sys.argv[1]
        obj = AcctBookkeepingService()
        obj.do_job_writeoff(sett_month)


if "__main__" == __name__:
    # AcctBookkeepingService.task()
    cos_client.list_files(prefix="HS")


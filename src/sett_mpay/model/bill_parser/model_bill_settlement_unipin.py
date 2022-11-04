"""
    渠道账单-unipin
"""
from src import CountryInfoData
from src import SubChannelMappingData
from src import BillSettlementBaseData


class BillSettlementUnipinData(BaseBean):
    def __init__(self):
        self.bill_type = ''
        self.bill_month = ''
        self.due_month = ''
        self.due_date = ''
        self.channel = ''
        self.channel_product_no = ''
        self.channel_product_name = ''
        self.sub_channel = ''
        self.country = ''
        self.tran_type = ''
        self.tran_currency = ''
        self.tran_amount = 0.0
        self.tran_numbers = 0.0
        self.ori_currency = ''
        self.ori_income = 0.0
        self.ori_refund = 0.0
        self.ori_channel_tax = 0.0
        self.ori_channel_fee = 0.0
        self.ori_settlement = 0.0
        self.sett_currency = ''
        self.description = ''
        self.sub_merchant = ''
        self.currency = ''
        self.amount_charged_to_end_users = 0.0
        self.vat_rate = 0.0
        self.vat_amount = 0.0
        self.amount_excluding_tax = 0.0
        self.percent_fee_rate = 0.0
        self.percent_fee_total = 0.0
        self.per_transaction_fee = 0.0
        self.per_transaction_fee_total = 0.0
        self.transaction_numbers = 0.0
        self.payout_to_merchant_local = 0.0
        self.payout_to_merchant_usd = 0.0
        self.exchange_rate = 0.0
        self.file_md5 = ''
        self.file_name = ''
        self.remark = ''
        self.special_note = ''

    def get_uniq_no(self):
        uniq_no = Xutil.md5_str(self.__str__, case="UPPER")
        return uniq_no

    def get_base_bill(
            self
            , country_info_dict: Dict[str, CountryInfoData]
            , sub_channel_dict: Dict[str, SubChannelMappingData]
            , sett_currency_dict: Dict[str, str]
            , default_cid_dict: Dict[str, dict]
    ):
        msg = 'SUCCESS'
        # country info
        channel_country_code = self.country
        channel_country_name = self.country
        if channel_country_name in country_info_dict:
            country_info = country_info_dict[channel_country_name]
            channel_country_code = country_info.country_code
            channel_country_name = country_info.country_name

        # cid、mcid
        cid = ""
        mcid = ""
        channel = self.channel
        sub_channel = self.sub_channel
        key_sub_channel1 = Xutil.link_words(channel, Xutil.clean_str(sub_channel))
        key_sub_channel2 = Xutil.link_words(
            self.channel, Xutil.clean_str("{}&&{}".format(channel_country_code, sub_channel)))
        if key_sub_channel1 in sub_channel_dict:
            sub_channel_info = sub_channel_dict[key_sub_channel1]
            cid = sub_channel_info.cid
            mcid = sub_channel_info.mcid
        elif key_sub_channel2 in sub_channel_dict:
            sub_channel_info = sub_channel_dict[key_sub_channel2]
            cid = sub_channel_info.cid
            mcid = sub_channel_info.mcid
        else:
            sub_channel_info = SubChannelMappingData.get_sub_channel_info(db_midas_merchant, channel, sub_channel)
            if sub_channel_info:
                cid = sub_channel_info.cid
                mcid = sub_channel_info.mcid
        if Xutil.is_empty(cid) or Xutil.is_empty(mcid):
            if channel in default_cid_dict:
                default_cid_info = default_cid_dict[channel]
                cid = default_cid_info["cid"]
                mcid = default_cid_info["mcid"]
            else:
                msg = "missing sub_channel mapping: {}".format(Xutil.link_words(channel, sub_channel))
                return False, msg, None

        # 结算币种
        if cid in sett_currency_dict:
            sett_currency = sett_currency_dict[cid]
        else:
            sett_currency = "USD"
            msg = "missing sett_currency, use USD as default: {}".format(Xutil.link_words(channel, cid, sub_channel))

        base_bill = BillSettlementBaseData()
        base_bill.uniq_no = self.get_uniq_no()
        base_bill.bill_type = self.bill_type
        base_bill.bill_month = self.bill_month
        base_bill.data_month = self.bill_month
        base_bill.data_date = Xutil.get_month_last_day(self.bill_month)
        base_bill.due_month = Xutil.get_month_next(self.bill_month)
        base_bill.due_date = Xutil.get_month_last_day(base_bill.due_month)
        base_bill.product_no = self.channel_product_no
        base_bill.product_name = self.channel_product_name
        base_bill.channel = channel
        base_bill.cid = cid
        base_bill.mcid = mcid
        base_bill.sub_channel = self.sub_channel
        base_bill.channel_country_code = channel_country_code
        base_bill.channel_country_name = channel_country_name
        base_bill.midas_country_code = ''
        base_bill.midas_country_name = ''
        base_bill.tran_type = self.tran_type
        base_bill.tran_currency = self.tran_currency
        base_bill.tran_amount = self.tran_amount
        base_bill.tran_numbers = self.tran_numbers
        base_bill.ori_currency = self.ori_currency
        base_bill.ori_income = self.ori_income
        base_bill.ori_refund = self.ori_refund
        base_bill.ori_channel_tax = self.ori_channel_tax
        base_bill.ori_channel_fee = self.ori_channel_fee
        base_bill.ori_channel_settlement = self.ori_settlement
        base_bill.sett_currency = sett_currency
        return True, msg, base_bill

    @staticmethod
    def batch_insert(db_sett: MySQLClient, bill_month, channel, data_list):
        sql = '''
            delete from db_mpay_channel.t_bill_settlement_unipin
            where bill_month = '{}' and channel = '{}'
        '''.format(bill_month, channel)
        db_sett.update(sql)
        db_sett.batch_insert(data_list, "db_mpay_channel", "t_bill_settlement_unipin")

    @staticmethod
    def get_bill_list(db_sett: MySQLClient, bill_month):
        sql = '''
            select * from db_mpay_channel.t_bill_settlement_unipin where bill_month = '{}'
        '''.format(bill_month)
        db_ret = db_sett.query(sql, cls=BillSettlementUnipinData)
        data_list: List[BillSettlementUnipinData] = db_ret.data
        return data_list

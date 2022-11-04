"""
    渠道规则
    sett_conf_v2.t_channel_merchant_info
    sett_conf_v2.t_channel_rate_info
"""
from src import List, Dict
from src import Xlog, Xutil, BaseBean, MySQLClient
from src import OUInfoData
from src import PltInfoData


class ChannelRulesData(BaseBean):
    def __init__(self):
        self.contract_no = ''
        self.channel = ''
        self.cid = ''
        self.country = ''
        self.province = ''
        self.city = ''
        self.percent_fee_rate = ''
        self.per_transaction_fee = ''
        self.per_transaction_fee_currency = ''
        self.had_special_rules = ''
        self.special_rules = ''
        self.tax_fee_order = ''
        self.payment_period = ''
        self.sett_currency = ''
        self.channel_mdm_id = ''
        self.channel_mdm_name = ''

        self.plt_type = ''
        self.plt_ou_id = ''
        self.plt_ou_name = ''
        self.plt_ou_short = ''
        self.plt_mdm_id = ''
        self.plt_mdm_name = ''
        self.plt_coa_no = ''
        self.plt_coa_name = ''
        self.plt_cost_no = ''
        self.plt_cost_name = ''
        self.main_date_begin = ''
        self.main_date_end = ''
        self.sub_date_begin = ''
        self.sub_date_end = ''

    @staticmethod
    def get_channel_rules_dict(
            db_midas_merchant: MySQLClient
            , data_month
            , ou_info_dict: Dict[str, OUInfoData]
            , plt_info_dict: Dict[str, PltInfoData]
    ):
        last_date = Xutil.get_month_last_day(data_month)
        sql = '''
            select A.FContractNo as contract_no
                , A.FMainChannel as channel
                , A.FChannelID as cid
                , A.FCountryCode as country
                , A.FProvince as province
                , A.FCity as city
                , A.FChannelRate as percent_fee_rate
                , A.FPerTransactionFee as per_transaction_fee
                , A.FPerTransactionFeeCurrencyType as per_transaction_fee_currency
                , A.FHadSpecialRules as had_special_rules
                , A.FSpecialRules as special_rules
                , A.FTaxFeeOrder as tax_fee_order
                , A.FPaymentPeriod as payment_period
                , A.FPayCurrencyType as sett_currency
                , B.FOuID as plt_ou_id
                , B.FMdmID as channel_mdm_id
                , B.FMdmName as channel_mdm_name
                , B.FBeginDate as main_date_begin
                , B.FEndDate as main_date_end
                , A.FBeginDate as sub_date_begin
                , A.FEndDate as sub_date_end
            from sett_conf_v2.t_channel_rate_info A
            left join sett_conf_v2.t_channel_merchant_info B
                on A.FMainChannel = B.FMainChannel and A.FContractNo = B.FContractNo    
            where A.FStatus = 1 and A.FBeginDate <= '{data_date}' and A.FEndDate >= '{data_date}'
                and B.FStatus = 1 and B.FBeginDate <= '{data_date}' and B.FEndDate >= '{data_date}'
        '''.format(data_date=last_date)
        db_ret = db_midas_merchant.query(sql, cls=ChannelRulesData)
        data_list: List[ChannelRulesData] = db_ret.data

        msg_set = set()
        data_dict = {}
        for data in data_list:
            if data.plt_ou_id not in plt_info_dict:
                msg_set.add("missing plt info: {}".format(data.plt_ou_id))
                continue
            if data.plt_ou_id not in ou_info_dict:
                msg_set.add("missing ou info: {}".format(data.plt_ou_id))
                continue
            plt_ou_info = ou_info_dict[data.plt_ou_id]
            plt_info = plt_info_dict[data.plt_ou_id]
            data.plt_type = plt_info.plt_type
            data.plt_ou_id = plt_ou_info.FOuID
            data.plt_ou_name = plt_ou_info.FOuFullName
            data.plt_ou_short = plt_ou_info.FOuName
            data.plt_mdm_id = plt_info.plt_mdm_id
            data.plt_mdm_name = plt_info.plt_mdm_name
            data.plt_coa_no = plt_info.plt_coa_no
            data.plt_coa_name = plt_info.plt_coa_no
            data.plt_cost_no = plt_info.plt_cost_no
            data.plt_cost_name = plt_info.plt_cost_name

            # 当前都是USD，出现多币种时需要主数据维护准确
            data.sett_currency = "USD"
            data.country = str(data.country).upper()

            key = Xutil.link_words(data.cid, data.country)
            if key not in data_dict:
                data_dict[key] = data
            else:
                msg_set.add("duplicate channel rule: {}".format(key))
        # end for
        return True, msg_set, data_dict

    @staticmethod
    def get_sett_currency_dict(db_sett: MySQLClient, logger=Xlog.get_default_logger()):
        sql = '''
            select distinct FChannelID as cid
                , FPayCurrencyType as sett_currency
            from sett_conf_v2.t_channel_rate_info
            where FStatus = 1
        '''
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            cid = str(line["cid"])
            sett_currency = str(line["sett_currency"])
            if sett_currency != "USD":
                logger.warn("sett_currency != USD: {}".format(cid))
                sett_currency = "USD"
            data_dict[cid] = sett_currency
        # end for
        return data_dict

    @staticmethod
    def get_default_cid_mapper(db_sett: MySQLClient, sett_month):
        """
            获取主渠道出现过的cid、mcid
            此方式获取的cid、mcid不参与计算，主要是匹配渠道mdm信息
        """
        sql = '''
            select distinct channel, cid, mcid 
            from db_mpay_income.t_mpay_esti_base
            where sett_month = '{}'
        '''.format(sett_month)
        db_ret = db_sett.query(sql)

        data_dict = {}
        for line in db_ret.data:
            channel = line["channel"]
            cid = line["cid"]
            mcid = line["mcid"]
            if channel not in data_dict:
                data_dict[channel] = line
        # end for
        return data_dict

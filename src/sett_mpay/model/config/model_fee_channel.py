"""
    计算模型-渠道费
"""
from typing import Dict
from sett_sdk_base.xutil import Xutil
from src import TaxFeeData
from src import ChannelRulesData
from src import EstiBaseWater


class ChannelFeeData(object):
    def __init__(self):
        self.cid = ""
        self.country = ""
        self.currency = ''
        self.amount = 0
        self.order_count = 0
        self.tax_fee_order = ""  # FirstFeeThenTax:先费后税; FirstTaxThenFee:先税后费；
        self.channel_fee_total = 0
        self.channel_percent_fee_rate = 0
        self.channel_percent_fee_amount = 0
        self.channel_per_transaction_fee = 0
        self.channel_per_transaction_fee_amount = 0
        self.channel_contract_no = ""
        self.channel_rule: ChannelRulesData = ChannelRulesData()

    @staticmethod
    def cal_channel_fee(
            base_data: EstiBaseWater
            , tax_fee: TaxFeeData
            , channel_rules_dict: Dict[str, ChannelRulesData]
    ):
        msg = "SUCCESS"

        channel = base_data.channel
        cid = base_data.cid
        country = base_data.channel_country_code
        currency = base_data.tran_currency
        amount = float(base_data.tran_amount)
        order_count = float(base_data.tran_numbers)

        key_channel_rule1 = Xutil.link_words(cid, country)
        key_channel_rule2 = Xutil.link_words(cid, "GLOBAL")
        key_channel_rule3 = Xutil.link_words(cid, "*")
        if key_channel_rule1 in channel_rules_dict:
            channel_rule = channel_rules_dict[key_channel_rule1]
        elif key_channel_rule2 in channel_rules_dict:
            channel_rule = channel_rules_dict[key_channel_rule2]
        elif key_channel_rule3 in channel_rules_dict:
            channel_rule = channel_rules_dict[key_channel_rule3]
        else:
            msg = "missing channel rate: {}".format(Xutil.link_words(
                base_data.channel, base_data.cid, base_data.mcid, base_data.channel_country_code, base_data.merchant_id
            ))
            return False, msg, None
        if channel == "adyen":
            return ChannelFeeData.cal_channel_fee_adyen(base_data, channel_rule)

        percent_fee_rate = Xutil.parse_to_float(channel_rule.percent_fee_rate)
        per_transaction_fee = Xutil.parse_to_float(channel_rule.per_transaction_fee)
        tax_fee_order = channel_rule.tax_fee_order
        if tax_fee_order == "FirstFeeThenTax":
            percent_fee_amount = amount * percent_fee_rate
            per_transaction_fee_amount = order_count * per_transaction_fee
            channel_fee_total = percent_fee_amount + per_transaction_fee_amount
        elif tax_fee_order == "FirstTaxThenFee":
            tax_amount = tax_fee.tax_amount
            percent_fee_amount = (amount - tax_amount) * percent_fee_rate
            per_transaction_fee_amount = order_count * per_transaction_fee
            channel_fee_total = percent_fee_amount + per_transaction_fee_amount
        else:
            msg = "new tax_fee_order: {} | {}".format(tax_fee_order, Xutil.link_words(
                base_data.channel, base_data.cid, base_data.mcid, base_data.midas_country_code, base_data.merchant_id
            ))
            return False, msg, None

        data = ChannelFeeData()
        data.cid = cid
        data.country = country
        data.currency = currency
        data.amount = amount
        data.order_count = order_count
        data.tax_fee_order = tax_fee_order  # FirstFeeThenTax:先费后税; FirstTaxThenFee:先税后费；
        data.channel_fee_total = channel_fee_total
        data.channel_percent_fee_rate = percent_fee_rate
        data.channel_percent_fee_amount = percent_fee_amount
        data.channel_per_transaction_fee = per_transaction_fee
        data.channel_per_transaction_fee_amount = per_transaction_fee_amount
        data.channel_contract_no = channel_rule.contract_no
        data.channel_rule = channel_rule
        return True, msg, data

    @staticmethod
    def cal_channel_fee_adyen(base_data: EstiBaseWater, channel_rule: ChannelRulesData):
        cid = base_data.cid
        country = base_data.channel_country_code
        currency = base_data.tran_currency
        amount = float(base_data.tran_amount)
        order_count = float(base_data.tran_numbers)

        # adyen 使用账单平均费率
        percent_fee_rate = 0.0438
        percent_fee_amount = percent_fee_rate * amount
        channel_fee_total = percent_fee_amount

        data = ChannelFeeData()
        data.cid = cid
        data.country = country
        data.currency = currency
        data.amount = amount
        data.order_count = order_count
        data.tax_fee_order = ""
        data.channel_fee_total = channel_fee_total
        data.channel_percent_fee_rate = percent_fee_rate
        data.channel_percent_fee_amount = percent_fee_amount
        data.channel_contract_no = channel_rule.contract_no
        data.channel_rule = channel_rule
        return True, "SUCCESS", data

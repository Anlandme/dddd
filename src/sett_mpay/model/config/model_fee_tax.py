"""
    费用模型-代缴税
"""
from typing import Dict
from sett_sdk_base.xutil import Xutil
from src import EstiBaseWater
from src import ChannelTaxRulesData


class TaxFeeData(object):
    def __init__(self):
        self.cid = ""
        self.country = ""
        self.currency = ''
        self.amount = 0
        self.tax_withhold = ""
        self.tax_country = ""
        self.tax_rate = 0
        self.tax_amount = 0

    @staticmethod
    def cal_tax(
            base_data: EstiBaseWater
            , tax_rules_dict: Dict[str, ChannelTaxRulesData]
    ):
        msg = "SUCCESS"
        cid = base_data.cid
        country = base_data.channel_country_code
        currency = base_data.tran_currency
        amount = float(base_data.tran_amount)

        tax_withhold = "N"
        tax_country = ""
        tax_rate = 0
        tax_amount = 0

        key_tax = Xutil.link_words(cid, country)
        if key_tax in tax_rules_dict:
            tax_rule_info: ChannelTaxRulesData = tax_rules_dict[key_tax]
            tax_rate = Xutil.parse_to_float(tax_rule_info.channel_tax_rate)
            if tax_rate > 0.0001:
                tax_withhold = "CHANNEL"
                tax_country = country
                tax_amount = amount * tax_rate / (1 + tax_rate)
            # end if
        # end if

        data = TaxFeeData()
        data.cid = cid
        data.country = country
        data.currency = currency
        data.amount = amount
        data.tax_withhold = tax_withhold
        data.tax_country = tax_country
        data.tax_rate = tax_rate
        data.tax_amount = tax_amount
        return True, msg, data

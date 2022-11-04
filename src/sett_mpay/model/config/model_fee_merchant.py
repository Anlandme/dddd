"""
    计算模型-商户费
"""
from typing import Dict
from sett_sdk_base.xutil import Xutil
from src import TaxFeeData
from src import MerchantMapperData
from src import MerchantRulesData
from src import EstiBaseWater


class MerchantFeeData(object):
    def __init__(self):
        self.rule_id = ""
        self.merchant_id = ""
        self.merchant_name = ""
        self.mcid = ""
        self.country = ""
        self.currency = ''
        self.amount = 0
        self.order_count = 0
        self.merchant_fee_total = 0
        self.merchant_percent_fee_rate = 0
        self.merchant_percent_fee_amount = 0
        self.merchant_per_transaction_fee = 0
        self.merchant_per_transaction_fee_amount = 0
        self.merchant_contract_no = ""
        self.merchant_rule: MerchantRulesData = MerchantRulesData()

    @staticmethod
    def cal_merchant_fee(
            base_data: EstiBaseWater
            , tax_fee: TaxFeeData
            , merchant_rules_dict: Dict[str, MerchantRulesData]
            , merchant_mapper_dict: Dict[str, MerchantMapperData]
    ):
        msg = "SUCCESS"
        merchant_id = base_data.merchant_id
        mcid = base_data.mcid
        country = base_data.midas_country_code
        currency = base_data.tran_currency
        amount = float(base_data.tran_amount)
        order_count = float(base_data.tran_numbers)
        tax_amount = tax_fee.tax_amount

        # 业务信息
        if merchant_id not in merchant_mapper_dict:
            msg = "missing rule_id: {}".format(merchant_id)
            return False, msg, None
        merchant_biz_info = merchant_mapper_dict[merchant_id]
        rule_id = merchant_biz_info.rule_id
        merchant_name = merchant_biz_info.merchant_name

        # 规则信息
        key_merchant_rule1 = Xutil.link_words(rule_id, mcid, country)
        key_merchant_rule2 = Xutil.link_words(rule_id, mcid, "GLOBAL")
        key_merchant_rule3 = Xutil.link_words(rule_id, mcid, "*")
        if key_merchant_rule1 in merchant_rules_dict:
            merchant_rule = merchant_rules_dict[key_merchant_rule1]
        elif key_merchant_rule2 in merchant_mapper_dict:
            merchant_rule = merchant_rules_dict[key_merchant_rule2]
        elif key_merchant_rule3 in merchant_mapper_dict:
            merchant_rule = merchant_rules_dict[key_merchant_rule3]
        else:
            msg = "missing merchant rate: {}".format(Xutil.link_words(
                key_merchant_rule1, merchant_name
            ))
            return False, msg, None
        percent_fee_rate = Xutil.parse_to_float(merchant_rule.percent_fee_rate)
        per_transaction_fee = Xutil.parse_to_float(merchant_rule.per_transaction_fee)
        percent_fee_amount = (amount - tax_amount) * percent_fee_rate  # 商户侧合同都是"先税后费"
        per_transaction_fee_amount = order_count * per_transaction_fee
        merchant_fee_total = percent_fee_amount + per_transaction_fee_amount

        data = MerchantFeeData()
        data.rule_id = rule_id
        data.merchant_id = merchant_id
        data.merchant_name = merchant_name
        data.mcid = mcid
        data.country = country
        data.currency = currency
        data.amount = amount
        data.order_count = order_count
        data.merchant_fee_total = merchant_fee_total
        data.merchant_percent_fee_rate = percent_fee_rate
        data.merchant_percent_fee_amount = percent_fee_amount
        data.merchant_per_transaction_fee = per_transaction_fee
        data.merchant_per_transaction_fee_amount = per_transaction_fee_amount
        data.merchant_contract_no = merchant_rule.contract_no
        data.merchant_rule = merchant_rule
        return True, msg, data

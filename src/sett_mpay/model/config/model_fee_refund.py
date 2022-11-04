"""
    计算模型-退款
"""
import json
from typing import Dict
from sett_sdk_base.xutil import Xutil
from src import MerchantRulesData
from src import ChannelFeeData
from src import MerchantFeeData

from src import EstiBaseWater



class RefundFeeData(object):
    def __init__(self):
        self.currency = ''
        self.amount = 0.0
        self.order_count = 0
        self.channe_refund_fee_total = 0.0
        self.channe_refund_percent_fee_rate = 0.0
        self.channe_refund_per_transaction_fee = 0.0
        self.merchant_refund_fee_total = 0.0
        self.merchant_refund_percent_fee_rate = 0.0
        self.merchant_refund_per_transaction_fee = 0.0
        self.channel_fee: ChannelFeeData = ChannelFeeData()
        self.merchant_rule: MerchantRulesData = MerchantRulesData()

    @staticmethod
    def cal_refund_fee(base_data: EstiBaseWater,
    channel_fee:  ChannelFeeData,
    merchant_fee: MerchantFeeData,
    exchange_rate_dict: Dict[str, float]):
        msg = "SUCCESS"
        refund_data = RefundFeeData()

        # 不是退款类型，忽略
        if "TRADE_TYPE_REFUND" != base_data.tran_type and "refund" != base_data.tran_type:
            return True, msg, refund_data

        refund_data.currency = base_data.tran_currency
        refund_data.amount = float(base_data.tran_amount)
        refund_data.order_count = float(base_data.tran_numbers)
        refund_data.merchant_rule = merchant_fee.merchant_rule
        refund_data.channel_rule = channel_fee.channel_rule

        # 退款费用收取有两种类型:1、 每笔退款收取比例费用； 2、每笔退款收取固定手续费
        flag, msg = refund_data.parse_special_rule(exchange_rate_dict)
        if not flag:
            return False, msg, None

        # 计算渠道侧
        channel_refund_percent_fee_amount = refund_data.amount * refund_data.channel_refund_percent_fee_rate
        channel_refund_per_transaction_fee_amount = refund_data.order_count * refund_data.channel_refund_per_transaction_fee
        refund_data.channel_refund_fee_total = (channel_refund_percent_fee_amount + channel_refund_per_transaction_fee_amount) * -1

        # 计算商户侧
        merchant_refund_percent_fee_amount = refund_data.amount * refund_data.merchant_refund_percent_fee_rate
        merchant_refund_per_transaction_fee_amount = refund_data.order_count * refund_data.merchant_refund_per_transaction_fee
        refund_data.merchant_refund_fee_total = (merchant_refund_percent_fee_amount + merchant_refund_per_transaction_fee_amount) * -1

        return True, msg, refund_data

    def parse_special_rule(self, exchange_rate_dict: Dict[str, float]):
        msg = "SUCCESS"
        # 没有special rule
        if "Y" != self.channel_rule.had_special_rules or "Y" != self.merchant_rule.had_special_rules:
            msg = "missing special rules: {}".format(Xutil.link_words(
                self.channel, self.cid, self.mcid, self.channel_country_code, self.merchant_id
            ))
            return False, msg

        #part1：计算渠道规则
        flag, msg, channel_refund_percent_fee_rate, channel_refund_per_transaction_fee = RefundFeeData.parse_json(self.channel_rule.special_rules, self.currency, exchange_rate_dict)
        if not flag:
                return False, msg

        #part2：计算商户规则
        flag, msg, merchant_refund_percent_fee_rate, merchant_refund_per_transaction_fee = RefundFeeData.parse_json(self.merchant_rule.special_rules, self.currency, exchange_rate_dict)
        if not flag:
                return False, msg

        self.channel_refund_per_transaction_fee = channel_refund_per_transaction_fee
        self.channel_refund_percent_fee_rate = channel_refund_percent_fee_rate

        self.merchant_refund_per_transaction_fee = merchant_refund_per_transaction_fee
        self.merchant_refund_percent_fee_rate = merchant_refund_percent_fee_rate

        return True, msg

    # 几个渠道示例，后期可能会新增，结构上也会有所不同，是否有某一个渠道，存在两种规则呢？
    # mycard：{"Refund":{"TieredFixedRate":{"CurrencyType":"TWD","RangeList":{"2":{"Range":"0~max","Rate":"0.03"}}}},"FXRule":{"Order":{"FixedValue":"FirstFeeThenFX"}}}
    # gash ： {"Refund":{"NumberRefund":{"NumberRefundRate":"0.01~max","PerTransactionFee":"10","PerTransactionFeeCurrencyType":"USD"}},"FXRule":{"Order":{"FixedValue":"FirstFeeThenFX"}}}

    def parse_json(special_rule, targrt_currency, exchange_rate_dict: Dict[str, float]):
        msg = "SUCCESS"

        # 这里的解析有很大的问题：1、json格式不固定;2、不知道用什么策略？按比例还是固定？只好都尝试一下，取的字段不存在就会有异常

        # 第一次try,尝试取按比例收费的规则
        try:
            can_get_fee_rate = True
            special_rule = json.loads(special_rule)
            refund_percent_fee_rate = special_rule["Refund"]["TieredFixedRate"]["RangeList"]["2"]["Rate"]
        except Exception as e:
            can_get_fee_rate = False
            pass

        if can_get_fee_rate:
            return True, msg, float(refund_percent_fee_rate), 0.0

        # 第二次try,尝试取固定收费的规则
        try:
            can_get_transaction_fee = True
            refund_per_transaction_fee = special_rule["Refund"]["NumberRefund"]["PerTransactionFee"]
            refund_currency = special_rule["Refund"]["NumberRefund"]["PerTransactionFeeCurrencyType"]
        except Exception as e:
            can_get_transaction_fee = False
            pass

        if can_get_transaction_fee:
            # 这里还需要换汇，因为special rule里面的币种和交易币种不一定
            key = Xutil.link_words(refund_currency, targrt_currency)
            if refund_currency == targrt_currency:
                exchange_currency_rate = 1.0
            elif key in exchange_rate_dict:
                exchange_currency_rate = float(exchange_rate_dict[key])
            else:
                msg = "missing currency rate: {}".format(key)
                return False, msg, 0.0, 0.0

            return True, msg, 0.0, float(refund_per_transaction_fee) * exchange_currency_rate

        msg = "special rule is invalid: {}".format(special_rule)
        return False, msg, 0.0, 0.0
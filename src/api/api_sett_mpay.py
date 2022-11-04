"""
    MidasPay结算API
"""
from flask import request
from flask import Blueprint
from src import ApiResult, api_auth
from src import check_sett_month
from src import BillReportService
from src import BillGatherService
from src import BillParserService
from src import ChannelBillService
from src import MerchantBillService
from src import BillBaseExchangeService
from src import EstiBaseService
from src import EstiReportService
from src import AcctBookkeepingService
from src import AcctJMService
from src import ReceivableService
from src import CostConfirmService
from src import CostWithholdingService

api = Blueprint(__file__, __name__, url_prefix='/api/v1/mpay')
service_bill_gather = BillGatherService()
service_bill_base_exchange = BillBaseExchangeService()
service_bill_base_channel = ChannelBillService()
service_bill_base_merchant = MerchantBillService()
service_acct_jm = AcctJMService()
service_acct_bookkeeping = AcctBookkeepingService()
service_esti_base = EstiBaseService()
service_receivable = ReceivableService()
service_cost_confirm = CostConfirmService()
service_cost_withholding = CostWithholdingService()


# 账单解析入库
@api.route("/bill_parser", methods=["POST", "GET"])
@api.route("/bill_parser/", methods=["POST", "GET"])
@api_auth
def bill_parser():
    channel = request.args.get("channel")
    sett_month = request.args.get("period")
    force_flag = request.args.get("force_flag")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    msg = BillParserService.download_bill(channel, sett_month, force_flag)
    return ApiResult.success(message=msg)


# 账单聚合汇总
@api.route("/bill_gather", methods=["POST", "GET"])
@api.route("/bill_gather/", methods=["POST", "GET"])
@api_auth
def bill_gather():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_bill_gather.do_job(sett_month)
    return ApiResult.success()


# 基础汇率
@api.route("/bill_base_exchange", methods=["POST", "GET"])
@api.route("/bill_base_exchange/", methods=["POST", "GET"])
@api_auth
def bill_base_exchange():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_bill_base_exchange.do_job(sett_month)
    return ApiResult.success()


# 渠道基础账单
@api.route("/bill_base_channel", methods=["POST", "GET"])
@api.route("/bill_base_channel/", methods=["POST", "GET"])
@api_auth
def bill_base_channel():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_bill_base_channel.do_job(sett_month)
    return ApiResult.success()


# 商户基础账单
@api.route("/bill_base_merchant", methods=["POST", "GET"])
@api.route("/bill_base_merchant/", methods=["POST", "GET"])
@api_auth
def bill_base_merchant():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_bill_base_merchant.do_job(sett_month)
    return ApiResult.success()


# 账单财务报表
@api.route("/bill_report", methods=["POST", "GET"])
@api.route("/bill_report/", methods=["POST", "GET"])
@api_auth
def bill_report():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    BillReportService.do_job(sett_month)
    return ApiResult.success()


# 暂估基础报表
@api.route("/esti_base", methods=["POST", "GET"])
@api.route("/esti_base/", methods=["POST", "GET"])
@api_auth
def esti_base():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_esti_base.do_job(sett_month)
    return ApiResult.success()


# 暂估财务报表
@api.route("/esti_report", methods=["POST", "GET"])
@api.route("/esti_report/", methods=["POST", "GET"])
@api_auth
def esti_report():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    EstiReportService.do_job(sett_month)
    return ApiResult.success()


# 应收单
@api.route("/receivable_report", methods=["POST", "GET"])
@api.route("/receivable_report/", methods=["POST", "GET"])
@api_auth
def receivable_report():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_receivable.do_job(sett_month)
    return ApiResult.success()


# 成本预提
@api.route("/cost_withholding", methods=["POST", "GET"])
@api.route("/cost_withholding/", methods=["POST", "GET"])
@api_auth
def cost_withholding():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_cost_withholding.do_job(sett_month)
    return ApiResult.success()


# 成本确认
@api.route("/cost_confirm", methods=["POST", "GET"])
@api.route("/cost_confirm/", methods=["POST", "GET"])
@api_auth
def cost_confirm():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_cost_confirm.do_job(sett_month)
    return ApiResult.success()


# 账务凭证
@api.route("/acct_report", methods=["POST", "GET"])
@api.route("/acct_report/", methods=["POST", "GET"])
@api_auth
def acct_report():
    sett_month = request.args.get("period")
    acct_type = request.args.get("acct_type")  # ESTIMATE、BILL、WRITE_OFF
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_acct_bookkeeping.do_job(sett_month, acct_type)  # 账务凭证
    service_acct_jm.gen_report(sett_month, period_type=acct_type)  # JM模版
    return ApiResult.success()


# 账务JM推送集团
@api.route("/acct_2jm", methods=["POST", "GET"])
@api.route("/acct_2jm/", methods=["POST", "GET"])
@api_auth
def acct_2jm():
    sett_month = request.args.get("period")
    template_type = request.args.get("template_type")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    service_acct_jm.push2jm(sett_month, template_type)
    return ApiResult.success()


# 账务JM上传COS
@api.route("/acct_2cos", methods=["POST", "GET"])
@api.route("/acct_2cos/", methods=["POST", "GET"])
@api_auth
def acct_2cos():
    sett_month = request.args.get("period")
    # 参数检查
    flag, message, sett_month = check_sett_month(sett_month)
    if not flag:
        return ApiResult.error(message=message)

    AcctJMService.push2cos(sett_month)
    return ApiResult.success()

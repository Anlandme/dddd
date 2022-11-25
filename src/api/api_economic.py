from flask import request
from flask import Blueprint
from src.api import ApiResult
from src.economic.service.macro_china import MacroChinaService

import json


import pandas as pd


api = Blueprint(__file__, __name__, url_prefix='/api/economic')

@api.route("/china/lpr", methods=["GET", "POST"])
def china_lpr():
    samples = int(request.args.get("samples"))

    lpr = MacroChinaService.lpr(samples)

    #https://blog.csdn.net/qq_42140717/article/details/124350979

    result = ApiResult.success(data=lpr)
    return result

@api.route("/china/shibor", methods=["GET", "POST"])
def china_shibor():
    macro_china_shibor_all = MacroChinaService.shibor()
    result = ApiResult.success(data=macro_china_shibor_all)
    return result

@api.route("/china/hk_market_info", methods=["GET", "POST"])
def china_hk_market_info():
    macro_china_hk_market_info = MacroChinaService.hk_market_info()
    result = ApiResult.success(data=macro_china_hk_market_info)
    return result

@api.route("/china/gdp", methods=["GET", "POST"])
def china_gdp():
    macro_china_gdp = MacroChinaService.gdp()
    result = ApiResult.success(data=macro_china_gdp)
    return result

@api.route("/china/gdp_yearly", methods=["GET", "POST"])
def china_gdp_yearly():
    macro_china_gdp_yearly = MacroChinaService.gdp_yearly()
    result = ApiResult.success(data=macro_china_gdp_yearly)
    return result

@api.route("/china/pmi", methods=["GET", "POST"])
def china_pmi():
    macro_china_pmi = MacroChinaService.pmi()
    result = ApiResult.success(data=macro_china_pmi)
    return result

@api.route("/china/cpi", methods=["GET", "POST"])
def china_cpi():
    macro_china_cpi = MacroChinaService.cpi()
    result = ApiResult.success(data=macro_china_cpi)
    return result

@api.route("/china/shrzgm", methods=["GET", "POST"])
def china_shrzgm():
    macro_china_shrzgm = MacroChinaService.shrzgm()
    result = ApiResult.success(data=macro_china_shrzgm)
    return result

@api.route("/china/money_supply", methods=["GET", "POST"])
def china_money_supply():
    macro_china_money_supply = MacroChinaService.money_supply()
    return ApiResult.success(data=macro_china_money_supply)

@api.route("/china/M2", methods=["GET", "POST"])
def china_M2():
    macro_china_m2_yearly = MacroChinaService.M2()
    return ApiResult.success(data=macro_china_m2_yearly)


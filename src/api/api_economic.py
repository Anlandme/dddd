from flask import request
from flask import Blueprint
from src.api import ApiResult
from src.economic.service.macro_china import MacroChinaService

import json


import pandas as pd


api = Blueprint(__file__, __name__, url_prefix='/api/economic')

@api.route("/china/qyspjg", methods=["GET", "POST"])
def china_qyspjg():
    resp = MacroChinaService.qyspjg()
    return ApiResult.success(data=resp)

@api.route("/china/gksccz", methods=["GET", "POST"])
def china_gksccz():
    samples = int(request.args.get("samples"))
    lpr = MacroChinaService.gksccz()
    result = ApiResult.success(data=lpr)
    return result



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
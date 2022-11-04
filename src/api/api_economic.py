from flask import request
from flask import Blueprint
from src.api import ApiResult
from src.economic.service.macro_china import MacroChinaService

import json


import pandas as pd


api = Blueprint(__file__, __name__, url_prefix='/api/economic')

@api.route("/china_gksccz", methods=["GET", "POST"])
def china_gksccz():
    samples = int(request.args.get("samples"))

    lpr = MacroChinaService.lpr(samples)

    print(lpr)
    #https://blog.csdn.net/qq_42140717/article/details/124350979

    result = ApiResult.success(data=lpr)
    return result
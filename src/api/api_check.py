from flask import request
from flask import Blueprint
from src.api import ApiResult


api = Blueprint(__file__, __name__, url_prefix='/api')

@api.route("/check", methods=["GET", "POST"])
def get():
    result = ApiResult.success()
    return result
    return result
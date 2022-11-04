from flask import request
from functools import wraps
import json


def api_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        host = request.remote_addr
        secret_id = request.headers.get("Secret-Id")
        if secret_id is None or secret_id == "":
            secret_id = request.headers.get("secret_id")
        else:
            return ApiResult.fail(message="No API Auth!")
    return wrapper


class ApiResult(object):
    def __init__(self):
        self.code = 0
        self.message = "SUCCESS"
        self.data = ""
        self.page_info = None

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    @staticmethod
    def error(code=-1, message="SYSTEM ERROR!", data=None):
        result = ApiResult()
        result.code = code
        result.message = message
        result.data = data
        return result.__dict__

    @staticmethod
    def fail(code=-1, message="SYSTEM ERROR!", data=None):
        result = ApiResult()
        result.code = code
        result.message = message
        result.data = data
        return result.__dict__

    @staticmethod
    def success(code=0, message="SUCCESS", data="", page_info=None):
        result = ApiResult()
        result.code = code
        result.message = message
        result.data = data

        return result.__dict__
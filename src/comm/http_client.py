import requests
from src import Xlog


class HttpError(UserWarning):
    """
        HTTP 响应异常
    """

    def __init__(self, code=-200, message=''):
        self.code = code
        self.message = message

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')


class HttpClient(object):
    HEADER_JSON = {"Content-Type": "application/json; charset=utf8"}
    HEADER_TEXT = {"Content-Type": "application/text; charset=utf8"}
    
    @staticmethod
    def do_get(url, params=None, headers=None, logger=Xlog.get_default_logger()):
        logger.debug("url:{}; params: {}; headers: {}".format(url, params, headers))
        response = requests.get(url, params=params, headers=headers, timeout=1000)
        logger.info("url:{}; response: {}".format(url, response.text))
        return HttpClient.parse_response(url, response)

    @staticmethod
    def do_post(url, params=None, headers=None, logger=Xlog.get_default_logger()):
        logger.debug("url:{}; params: {}; headers: {}".format(url, params, headers))
        response = requests.post(url, data=params, headers=headers, timeout=1000)
        logger.info("url:{}; response: {}".format(url, response.text))
        return HttpClient.parse_response(url, response)
    
    @staticmethod
    def parse_response(url, response):
        if response is None:
            return None
        if 200 != response.status_code:
            raise HttpError(message="HTTP接口响应异常：{} | {} | {}".format(url, response.status_code, response.reason))
        return response.text
        
    
if "__main__" == __name__:
    url = "https://www.baidu.com/"
    res = HttpClient.do_get(url)
    print(res)

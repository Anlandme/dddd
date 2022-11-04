import os
import re
import time
import datetime
import json
import arrow
from hashlib import md5


class Xutil(object):

    @staticmethod
    def md5_str(str_input, case="LOWER"):
        """
        MD5字符串
        :param str_input: 输入字符串
        :param case: 结果类型（LOWER：小写，UPPER：大写）
        :return: MD5字符串
        """
        ret = md5(str(str_input).strip().encode("utf-8")).hexdigest()
        if case == "UPPER":
            return ret.upper()
        elif case == "LOWER":
            return ret.lower()
        else:
            return ret

    @staticmethod
    def clean_str(str_input, case="LOWER"):
        """
        清除空格，不修改原始变量值
        :param str_input: 输入字符串
        :param case: 结果类型（LOWER：小写，UPPER：大写）
        :return: 去空格字符串
        """
        ret = str_input
        if ret is None:
            ret = ""
        ret = str(ret).replace(" ", "").strip()
        if case == "UPPER":
            return ret.upper()
        elif case == "LOWER":
            return ret.lower()
        else:
            return ret

    @staticmethod
    def simple_str(str_input):
        """
        简化字符串：移除换行、首尾空格，合并相邻空格
        :param str_input:
        :return: 简化字符串
        """
        if str_input is None:
            return ""
        str_simple = str(str_input).replace("\n", " ").strip()
        while str_simple.find("  ") >= 0:
            str_simple = str_simple.replace("  ", " ")
        return str_simple

    @staticmethod
    def link_words(*words, link_str=" | "):
        word_list = []
        for item in words:
            word_list.append(str(item))
        result = link_str.join(word_list)
        return result
    
    @staticmethod
    def split(str_input, link_str=" | "):
        return str_input.split(link_str)

    @staticmethod
    def format_date(date_input, format_input="%m %d %Y", format_output="%Y-%m-%d"):
        _date = datetime.datetime.strptime(str(date_input).strip(), format_input)
        return (_date).strftime(format_output)

    @staticmethod
    def format_datetime(datetime_input, format_output="YYYY-MM-DD HH:mm:ss"):
        if not datetime_input:
            return ""
        return arrow.get(datetime_input).format(format_output)

    @staticmethod
    def format_timestamp(timestamp, format_output="%Y-%m-%d"):
        timestamp = time.localtime(int(timestamp))
        return time.strftime(format_output, timestamp)

    @staticmethod
    def get_date_difference(date_begin, date_end):
        """
            计算2个日期相隔天数
        """
        # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
        date_begin = date_begin.replace("-", "").replace("/", "")[0:8]
        date_end = date_end.replace("-", "").replace("/", "")[0:8]

        date_begin = time.strptime(date_begin, "%Y%m%d")
        date_end = time.strptime(date_end, "%Y%m%d")

        date_begin = datetime.datetime(date_begin[0], date_begin[1], date_begin[2])
        date_end = datetime.datetime(date_end[0], date_end[1], date_end[2])

        date_difference = date_end - date_begin
        return date_difference.days

    @staticmethod
    def get_date_current(date_format="%Y-%m-%d %H:%M:%S"):
        """
            获取当天的日期
        :param date_format:
        :return:
        """
        return time.strftime(date_format, time.localtime(time.time()))

    @staticmethod
    def get_date_before(date_input=None, before_count=1, date_format="%Y-%m-%d"):
        """
            获取指定日期的前/后 N 天的日期
        :param before_count: int (>0: 前 N 天；<0: 后 N 天)
        :param date_input: 指定日期，None 取系统当天 "%Y-%m-%d %H:%M:%S"
        :param date_format: 日期格式
        :return:
        """
        if date_input is None:
            date_base = datetime.datetime.now()
        else:
            date_base = datetime.datetime.strptime(date_input, date_format)
            
        offset = datetime.timedelta(days=-before_count)
        re_date = (date_base + offset).strftime(date_format)
        return re_date

    @staticmethod
    def get_date_next(date_input=None, next_count=1, date_format="%Y-%m-%d"):
        """
            获取指定日期的前/后 N 天的日期
        :param before_count: int (>0: 前 N 天；<0: 后 N 天)
        :param date_input: 指定日期，None 取系统当天 "%Y-%m-%d %H:%M:%S"
        :param date_format: 日期格式
        :return:
        """
        if date_input is None:
            date_base = datetime.datetime.now()
        else:
            date_base = datetime.datetime.strptime(date_input, date_format)
    
        offset = datetime.timedelta(days=next_count)
        re_date = (date_base + offset).strftime(date_format)
        return re_date

    @staticmethod
    def get_date_between(date_begin, date_end, date_format="%Y-%m-%d"):
        """
            获取开始、结束日期间的所有日期(包含开始、结束日期)
        :param date_begin:
        :param date_end:
        :param date_format:
        :return:
        """
        if Xutil.is_empty(date_end):
            date_end = date_begin
        
        date_list = []
        date_begin = datetime.datetime.strptime(date_begin, date_format)
        date_end = datetime.datetime.strptime(date_end, date_format)
        while date_begin <= date_end:
            date_str = date_begin.strftime(date_format)
            date_list.append(date_str)
            date_begin += datetime.timedelta(days=1)
        return date_list

    @staticmethod
    def get_month_last_day(month_input):
        """
            获取开始、结束日期间的所有日期(包含开始、结束日期)
        :param month_input: YYYY-MM
        :return:
        """
        if str(month_input) == 6:
            month_input = "{}-{}".format(month_input[0:4], month_input[4:6])
        month_next = Xutil.get_month_next(month_input)
        date_temp = "{}-01".format(month_next)
        date_last = Xutil.get_date_before(date_temp)
        return date_last

    @staticmethod
    def get_month_date_first_and_last(month_input, date_format="%Y-%m-%d"):
        month_input = month_input.replace("-", "")
        year = month_input[0:4]
        month = month_input[4:6]
        return Xutil.get_month_date(year, month, date_format)
    
    @staticmethod
    def get_month_date(year, month, date_format="%Y-%m-%d"):
        year = int(year)
        month = int(month)
        
        date_first = (datetime.datetime(year, month, 1)).strftime(date_format)
        if 12 == month:
            dt_last = (datetime.datetime(year, month, 31)).strftime(date_format)
        else:
            dt_last = (datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)).strftime(date_format)
        return date_first, dt_last

    @staticmethod
    def get_month_before(month_input=None, before_count=1, month_format="YYYY-MM"):
        """
            获取指定月份的前/后 N 月的日期
            无参数是返回上月 | YYYY-MM
            依赖 arrow | pip install arrow
        :param month_input: 指定的月份，None 取系统当月
        :param before_count: int (>0: 前 N 月；<0: 后 N 月)
        :param month_format: 月份格式，默认 YYYY-MM
        :return:
        """
        if not month_input:
            month_input = arrow.now().format(month_format)
            
        a = arrow.get(month_input, month_format)
        b = a.shift(months=-before_count)
        return b.format(month_format)
    
    @staticmethod
    def get_month_between(month_begin, month_end, month_format="YYYY-MM"):
        """
            获取开始、结算月份间的所有月份(包含开始、结束月份)
        :param month_begin:
        :param month_end:
        :param month_format:
        :return:
        """
        month_list = []
        while month_begin <= month_end:
            month_list.append(month_begin)
            a = arrow.get(month_begin, month_format)
            b = a.shift(months=1)
            month_begin = b.format(month_format)
        return month_list
        
    @staticmethod
    def get_month_next(month_input=None, next_count=1, month_format="YYYY-MM"):
        """
            获取指定月份后 N 月的日期
            无参数时返回下月 | YYYY-MM
            依赖 arrow | pip install arrow
        :param month_input:
        :param next_count:
        :param month_format:
        :return:
        """
        if not month_input:
            month_input = arrow.now().format(month_format)

        a = arrow.get(month_input, month_format)
        b = a.shift(months=next_count)
        return b.format(month_format)

    @staticmethod
    def get_default_sett_month():
        default_month = Xutil.get_date_before(before_count=4)[0:7]
        return default_month

    @staticmethod
    def is_valid_date(date_input, date_format="%Y-%m-%d"):
        """
            判断是否是一个有效的日期字符串
        :param date_input:
        :param date_format:
        :return:
        """
        try:
            time.strptime(date_input, date_format)
            return True
        except TypeError as error:
            return False
        except ValueError as error:
            return False

    @staticmethod
    def is_invalid_date(date_input, date_format="%Y-%m-%d"):
        """
            判断是否是一个无效的日期字符串
        :param date_input:
        :param date_format:
        :return:
        """
        return not Xutil.is_valid_date(date_input, date_format)

    @staticmethod
    def recode_str(str_input, code_ori="latin1", code_new="gbk"):
        """
            写入时 DB 连接编码是 latin1，读取时 DB 连接编码是 utf8，调用此方法可解决中文乱码
        :param str_input:
        :param code_ori:
        :param code_new:
        :return:
        """
        result = None
        try:
            result = str_input.encode(code_ori, 'ignore').decode(code_new, 'ignore')
        except UnicodeEncodeError as error:
            print("fail to recode str：{} | {}".format(str_input, error))
        
        if result is None or result.strip() == "":
            result = str_input
        return result
    
    @staticmethod
    def contains_chinese(str_input):
        """
            判断字符串是否包含中文
        :param str_input:
        :return:
        """
        if str_input and type(str_input) == str:
            for _char in str_input:
                if '\u4e00' <= _char <= '\u9fa5':
                    return True
        return False
    
    @staticmethod
    def format_float(num_input, accuracy=4):
        """
            格式化 num 精度
        :param num_input:
        :param accuracy:
        :return:
        """
        if num_input in [None, "", "-"]:
            num_input = 0
            
        temp = str(num_input).replace(",", "").replace(" ", "")
        if temp.find("%") >= 0:
            temp = str(float(temp.replace("%", ""))/100)
        if temp.find(".") < 0:
            temp = temp + ".000000000000"
        else:
            temp = temp + "000000000000"
        
        if accuracy <= 0:
            accuracy = 0
        elif accuracy >= 16:
            accuracy = 16
        else:
            accuracy = accuracy + 1
        
        res = temp[:temp.find(".") + accuracy]
        return res
    
    @staticmethod
    def parse_to_float(str_input, ignore_error=True):
        result = 0.0
        try:
            result = float(str_input)
        except Exception as err:
            if not ignore_error:
                raise err
        return result
    
    @staticmethod
    def parse_to_json(str_input):
        """
            字符串转JSON
        :param str_input:
        :return:
        """
        res = json.loads(str_input)
        return res

    @staticmethod
    def parse_to_dict(input_str, split_outer="&", split_inner="="):
        """
            k1=v1&k2=v2&k3=&k4=v4 类型字符串解析为 dict
        :param input_str:
        :param split_outer:
        :param split_inner:
        :return: {'k1':'v1', 'k2':'v2', 'k3':'', 'k4':'v4'}
        """
        if input_str is None or len(input_str) == 0:
            return {}
    
        result_dict = {}
        input_split = input_str.split(split_outer)
        for item in input_split:
            idx = item.find(split_inner)
            key = item[0:idx]
            value = item[idx + 1:]
            result_dict[key] = value
        return result_dict
    
    @staticmethod
    def get_from_dict(input_dict, key, default=''):
        if input_dict is None or len(input_dict) == 0 or key not in input_dict:
            return default
        result = input_dict[key]
        if result is None:
            return default
        else:
            return result

    @staticmethod
    def get_float_from_dict(input_dict, key):
        if input_dict is None or len(input_dict) == 0 or key not in input_dict:
            return 0

        value = input_dict[key]
        if value is None or str(value).strip() == "":
            return 0
        return float(value)

    @staticmethod
    def is_empty(input_str):
        if input_str is None or str(input_str).strip() == "":
            return True
        return False

    @staticmethod
    def is_not_empty(input_str):
        return not Xutil.is_empty(input_str)
    

if __name__ == '__main__':
    # temp = "测试中文".encode("gbk").decode("latin1")
    # print(temp)
    # res = Xutil.recode_str(temp)
    # print(res)
    # print(">>>>>")
    # print(Xutil.recode_str("测试中文"))
    #
    # Xutil.format_float(None)

    print(Xutil.get_date_difference("2021-03-30", "2021-04-02"))

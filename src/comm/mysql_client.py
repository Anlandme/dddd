import time
import mysql.connector
import mysql.connector.errorcode

import pymysql
from dbutils.pooled_db import PooledDB

from .xlog import Xlog
from .xutil import Xutil
from .bean_util import BaseBean, BeanUtil
from .config_reader import ConfigReader


class DBError(UserWarning):
    def __init__(self, code=-100, message='DB_ERROR'):
        self.code = code
        self.message = message

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')


class DBResult(object):
    """
    {
        'code': 0,
        'msg': 'SUCCESS',
        'data': '[{'k1': 'v1'}, {'k2': 'v2'}]' # DB 查询结果集
    }
    """

    CODE_SUCCESS = 0
    CODE_FAILED = -1
    MESSAGE_SUCCESS = 'SUCCESS'
    MESSAGE_FAILED = 'FAILED'

    def __init__(self, code=CODE_SUCCESS, message=MESSAGE_SUCCESS, data=None):
        self.code = code
        self.message = message
        self.data = data
        self.page_info = None

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    def is_failed(self):
        return self.code == DBResult.CODE_FAILED

    def is_success(self):
        return self.code == DBResult.CODE_SUCCESS

    @staticmethod
    def fail():
        return DBResult(DBResult.CODE_FAILED, DBResult.MESSAGE_FAILED)

    @staticmethod
    def success():
        return DBResult(DBResult.CODE_SUCCESS, DBResult.MESSAGE_SUCCESS)


class PageUtil(object):
    def __init__(self, total, page=1, size=20):
        self.total = total     # 总数据量
        self.page = page       # 当前页数， page >= 1
        self.size = size       # 每页数量
        self.pages = 0         # 总页数
        self.has_prev = False  # 是否有上一页 False/True
        self.has_next = False  # 是否有下一页 False/True
        self.prev_page = 0     # 上页页数
        self.next_page = 0     # 下页页数
        self.reset()

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    def reset(self):
        # 基础信息
        if self.total is None or int(self.total) < 0:
            self.total = 0
        if self.page is None or int(self.page) < 1:
            self.page = 1
        if self.size is None or int(self.page) <= 0:
            self.size = 20
        self.total = int(self.total)
        self.page = int(self.page)
        self.size = int(self.size)

        # 计算信息
        if self.total % self.size == 0:
            self.pages = int(self.total / self.size)
        else:
            self.pages = int(self.total / self.size) + 1
        if self.page > 1:
            self.has_prev = True
            self.prev_page = self.page - 1
        else:
            self.has_prev = False
            self.prev_page = self.page
        if self.page < self.pages:
            self.has_next = True
            self.next_page = self.page + 1
        else:
            self.has_next = False
            self.next_page = self.page

    @staticmethod
    def get_total(db_instance, sql):
        sql_total = '''
            select count(*) as total from ({}) t 
        '''.format(sql)
        db_ret = db_instance.query(sql_total)

        total = 0
        if db_ret and len(db_ret.data) == 1:
            total = int(db_ret.data[0]["total"])
        return total


class MySQLConfig(object):
    def __init__(self, host='127.0.0.1'
                 , port=3305
                 , user='root'
                 , password='Root@1234'
                 , timeout=5000
                 , charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout
        self.charset = charset
        self.use_unicode = True
        self.use_pure = False

    @staticmethod
    def get_config(conf_file, conf_section):
        config_reader = ConfigReader.get_instance(conf_file)
        host = config_reader.get(conf_section, "host")
        port = config_reader.get_int(conf_section, "port")
        user = config_reader.get(conf_section, "user")
        password = config_reader.get(conf_section, "password")
        timeout = config_reader.get_int(conf_section, "timeout")
        db_config = MySQLConfig(host, port, user, password, timeout)
        return db_config

    @staticmethod
    def parse_dict(data_dict: dict):
        db_config = MySQLConfig()
        db_config.__dict__ = data_dict
        return db_config


class MySQLClient(object):
    """
        历史遗留：用 latin1 编码写入的中文用 utf8 读取后乱码，可调用 Xutil.recode_str(str_input) 处理
    """

    def __init__(self, mysql_config: MySQLConfig, logger=Xlog.get_default_logger()):
        self.logger = logger
        self.host = mysql_config.host
        self.port = mysql_config.port
        self.user = mysql_config.user
        self.password = mysql_config.password
        self.timeout = mysql_config.timeout
        self.charset = mysql_config.charset
        self.use_unicode = True
        self.use_pure = None
        self.pool = None
        self.connection = None
        self.cursor = None

        self.init()

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '')

    def init(self):
        try:
            # 连接池参数-使用默认值
            min_cached = 0   # 连接池中空闲连接的初始数量
            max_cached = 2   # 连接池中空闲连接的最大数量
            max_shared = 8   # 共享连接的最大数量
            max_connections = 32  # 最大连接数量
            max_usage = 100        # 单个连接的最大重复使用次数
            blocking = True       # 超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
            set_session = None     # 可选的SQL命令列表，可用于准备会话。(例如设置时区)
            reset = True

            self.pool = PooledDB(
                pymysql, min_cached, max_cached, max_shared, max_connections, blocking
                , max_usage, set_session, reset, host=self.host, port=self.port, user=self.user
                , passwd=self.password, charset=self.charset, cursorclass=pymysql.cursors.DictCursor
            )

            self.connection = self.pool.connection()
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            raise DBError(message=error)

    @staticmethod
    def get_instance(conf_file, conf_section="db", logger=None):
        db_config = MySQLConfig.get_config(conf_file, conf_section)
        db_instance = MySQLClient(db_config, logger)
        return db_instance

    def __execute(self, sql, need_fetch=False, auto_commit=False):
        """
            私有方法，禁止外部调用
        :param sql:
        :param need_fetch:
        :param auto_commit:
        :return:
        """
        db_ret = DBResult()
        try:
            try:
                self.cursor.execute(sql)
            except:
                time.sleep(1)
                self.cursor.execute(sql)
            if need_fetch:
                db_ret = DBResult(data=self.cursor.fetchall())
            if auto_commit:
                self.connection.commit()
        except Exception as error:
            self.logger.error("db exception: {} | {}".format(error, Xutil.simple_str(sql)))
            raise DBError(message=error)
        finally:
            pass
        return db_ret

    def query(self, sql, cls=None):
        self.logger.info(Xutil.simple_str(sql))

        # SQL 校验
        if sql.strip().lower().find("select") != 0:
            raise DBError(message="not select sql! {}".format(sql))
        # sql含有中文，DB链接为latin1编码时，对sql做一次转换
        if Xutil.contains_chinese(sql) and self.charset.lower() == "latin1":
            sql = sql.encode("gbk", "ignore")

        db_ret = self.__execute(sql, True)
        # 查询结果转换为 obj
        if cls and issubclass(cls, BaseBean):
            if db_ret and db_ret.data and len(db_ret.data) > 0:
                bean_list = BeanUtil.parse2bean_list(db_ret.data, cls)
                db_ret.data = bean_list
        # end if
        return db_ret

    def query_page(self, sql, page, size, cls=None):
        total = PageUtil.get_total(self, sql)
        if total == 0:
            return None

        page_info = PageUtil(total, page, size)
        index = (page_info.page - 1) * page_info.size
        sql_page = sql + " limit {}, {}".format(index, page_info.size)
        db_ret = self.query(sql_page, cls)
        db_ret.page_info = page_info
        return db_ret

    def update(self, sql, auto_commit=True):
        simple_sql = Xutil.simple_str(sql)
        if len(simple_sql) > 512:
            simple_sql = "{} ...".format(simple_sql[0:512])
        self.logger.info(simple_sql)
        # SQL 校验
        sql_lower = sql.strip().lower()
        if sql_lower.find("delete") != 0 \
                and sql_lower.find("insert") != 0 \
                and sql_lower.find("replace") != 0 \
                and sql_lower.find("update") != 0 \
                and sql_lower.find("set") != 0:
            raise DBError(message="not delete|insert|update|replace|set sql! {}".format(sql))

        # sql含有中文，DB链接为latin1编码时，对sql做一次转换
        if Xutil.contains_chinese(sql) and self.charset.lower() == "latin1":
            sql = sql.encode("gbk", "ignore")

        db_ret = self.__execute(sql, False, auto_commit)
        return db_ret

    def batch_insert(self, data_list, db_name, tb_name, batch_size=3000):
        """
            批量保存数据
        :param data_list: 字典列表/对象列表(对象可通过__dict__转字典)；
        :param db_name:
        :param tb_name:
        :param batch_size:
        :return:
        """
        if data_list is None or len(data_list) == 0:
            self.logger.info("[batch_insert] no data to insert! {}.{}".format(db_name, tb_name))
            return
        self.logger.info("[batch_insert] data size: {}".format(len(data_list)))

        # filed_list
        first = data_list[0]
        if type(first) != dict:
            first = first.__dict__
        field_list = list(first.keys())
        field_str = ""
        for field in field_list:
            field_str += "{},".format(field)
        field_str = field_str[:-1]
        sql_insert = "INSERT INTO {}.{}({}) values ".format(db_name, tb_name, field_str)

        # data_size、batch_size
        data_size = len(data_list)
        if batch_size is None or batch_size <= 0:
            batch_size = 3000

        idx = 0
        sql_batch = ""
        for data_dict in data_list:
            idx += 1
            if type(data_dict) != dict:
                data_dict = data_dict.__dict__

            sql_value = ""
            for key in field_list:
                value = data_dict[key]
                sql_value += ' "{}",'.format(str(value).strip().replace('"', '\\"'))
            # end for
            sql_value = "({}),".format(sql_value[:-1])
            sql_batch += sql_value

            if idx % batch_size == 0 or idx == data_size:
                # execute sql
                sql = sql_insert + sql_batch[:-1]
                self.update(sql)
                sql_batch = ""
        # end for

    def foreach_insert(self, data_list, db_name, tb_name, ignore_error=False):
        """
            功能说明：遍历列表保存数据，效率较低，异常数据可忽略
            适用场景：异常验证
        :param data_list:
        :param db_name:
        :param tb_name:
        :param ignore_error:
        :return:
        """
        if data_list is None or len(data_list) == 0:
            self.logger.info("[foreach_insert] no data to insert! {}.{}".format(db_name, tb_name))
            return
        self.logger.info("[foreach_insert] data size: {}".format(len(data_list)))
        if len(data_list) >= 50000:
            self.logger.warn("[foreach_insert] too much data to use this method! data size: {}".format(len(data_list)))

        sql_insert = "INSERT INTO {}.{} SET ".format(db_name, tb_name)
        for data_dict in data_list:
            if type(data_dict) != dict:
                data_dict = data_dict.__dict__

            sql_value = ""
            for key in data_dict:
                value = data_dict[key]
                sql_value += ' {} = "{}",'.format(key, str(value).strip().replace('"', '\\"'))
            # end for
            sql_value = sql_value[:-1] + ";"
            sql = sql_insert + sql_value

            try:
                self.update(sql)
            except BaseException as error:
                self.logger.error("[foreach_insert] fail to insert data! {} | {}".format(error, sql))
                if ignore_error:
                    continue
                else:
                    raise error
        # end for

    def foreach_replace(self, data_list, db_name, tb_name, ignore_error=False):
        """
            功能说明：遍历列表保存数据，存在是执行更新逻辑，效率较低
            适用场景：异常验证
        :param data_list:
        :param db_name:
        :param tb_name:
        :param ignore_error:
        :return:
        """
        if data_list is None or len(data_list) == 0:
            self.logger.warn("No data to replace! {}.{}".format(db_name, tb_name))
            return
        self.logger.info("[foreach_replace]data size: {}".format(len(data_list)))
        if len(data_list) >= 50000:
            self.logger.warn("[foreach_replace] too much data to use this method! data size: {}".format(len(data_list)))

        sql_insert = "REPLACE {}.{} SET ".format(db_name, tb_name)
        for dict_data in data_list:
            if type(dict_data) != dict:
                dict_data = dict_data.__dict__

            sql_value = ""
            for key in dict_data:
                value = dict_data[key]
                sql_value += ' {} = "{}",'.format(key, str(value).strip().replace('"', '\\"'))
            sql_value = sql_value[:-1] + ";"
            sql = sql_insert + sql_value

            try:
                self.update(sql)
            except BaseException as error:
                self.logger.warn("[foreach_replace]fail to replace data! {} | {}".format(error, sql))
                if ignore_error:
                    continue
                else:
                    raise error
        # end for

    def commit(self):
        try:
            self.connection.commit()
        except mysql.connector.Error as error:
            raise DBError(message=error)
        return DBResult()

    def close(self):
        self.commit()
        self.cursor.close()
        self.connection.close()

    def get_character_set(self):
        """
        查询字符编码
        :return: {
            'character_set_client': '',        # 客户端编码
            'character_set_connection': '',    # 连接编码
            'character_set_results': ''        # 结果编码
        }
        """
        sql = "show variables like 'character_set%%' "
        ret = self.query(sql)

        data = ret.data
        if not data or len(data) == 0:
            self.logger.info("db result is empty! {}".format(data))
            return

        result = {}
        for item in data:
            key = item["Variable_name"]
            value = item["Value"]
            result[key] = value
        # end for
        return result

    def update_no_commit(self, sql):
        """
            不自动commit
        :param sql:
        :return:
        """
        simple_sql = Xutil.simple_str(sql)
        if len(simple_sql) > 512:
            simple_sql = "{} ...".format(simple_sql[0:512])
        self.logger.info(simple_sql)

        # SQL 校验
        sql_lower = sql.strip().lower()
        if sql_lower.find("delete") != 0 \
                and sql_lower.find("insert") != 0 \
                and sql_lower.find("replace") != 0 \
                and sql_lower.find("update") != 0 \
                and sql_lower.find("set") != 0:
            raise DBError(message="not delete|insert|replace｜update|set sql! {}".format(sql))
        if sql_lower.find("delete") == 0 or sql_lower.find("set") == 0:
            self.logger.info(Xutil.simple_str(sql))

        # sql含有中文，DB链接为latin1编码时，对sql做一次转换
        if Xutil.contains_chinese(sql) and self.charset.lower() == "latin1":
            sql = sql.encode("gbk", "ignore")

        db_ret = self.__execute(sql, False, False)
        return db_ret


class MySQLUtil(object):
    @staticmethod
    def gen_update_sql(
            db_name
            , tb_name
            , update_dict: dict
            , where
            , field_filter_list: list
            , logger=Xlog.get_default_logger()
    ):
        """
            @db_name: 库
            @tb_name: 表
            @update_dict: 需要更新的信息
            @where: 更新调整
            #field_filter：过滤字段（不需要更新的字段）
        """
        if where is None or str(where).strip() == "":
            logger.error("missing where condition!")
            return None

        update_info = ""
        keys = update_dict.keys()
        for key in keys:
            if field_filter_list and key in field_filter_list:
                continue
            value = update_dict[key]
            update_info += "{}='{}',".format(key, value)
        # end for
        update_info = update_info.strip()
        if update_info.endswith(","):
            update_info = update_info[:-1]
        # end if

        sql = "UPDATE {}.{} SET {} WHERE ".format(
            db_name, tb_name, update_info, where
        )
        return sql

    @staticmethod
    def gen_insert_sql(db_name, tb_name, data_list):
        """
        data_list 转 INSERT SQL
        :param db_name:
        :param tb_name:
        :param data_list: 字段必须和库表保持一致
        :return:
        """
        if data_list is None or len(data_list) == 0:
            return None
        field_list = list(data_list[0].keys())
        if field_list is None or len(field_list) == 0:
            return None

        sql_insert_batch = "INSERT INTO {}.{} VALUES ".format(db_name, tb_name)
        for i in range(0, len(data_list)):
            data = data_list[i]

            sql_insert = ""
            for j in range(0, len(field_list)):
                field_name = field_list[j]
                field_value = data[field_name]
                if type(field_value) == str:
                    field_value = str(field_value).replace("'", "")
                sql_insert += ' "{}",'.format(str(field_value).strip().replace('"', '\\"'))
            # end for
            sql_insert = "({}),".format(sql_insert[0: -1])
            sql_insert_batch += sql_insert
        # end for
        sql_insert_batch = sql_insert_batch[:-1]
        return sql_insert_batch

    @staticmethod
    def gen_insert_sql_list(db_instance: MySQLClient, db_name, tb_name, where, batch_size=3000, max_records=5000000):
        """
        生成INSERT语句
        :param db_instance: DB实例
        :param db_name: 库名
        :param tb_name: 表名
        :param where: 条件（必须存在条件，无条件场景请用 'where 1=1' ）
        :param batch_size: 批量INSERT的批次大小
        :param max_records: 最大记录数据，最多查询数据量
        :return list(str): 批量insert语句list
        """
        # 参数检查
        if where is None or str(where).strip() == "":
            print(">> [gen_insert_sql] invalid param! where: {}".format(where))
            return None
        # 查询DB数据
        sql = "select * from {}.{} where 1=1 AND {} limit {}".format(db_name, tb_name, where, max_records)
        db_ret = db_instance.query(sql)
        data_list = db_ret.data
        if data_list is None or len(data_list) == 0:
            print(">> [gen_insert_sql] no data found! {}".format(sql))
            return None
        if len(data_list) == max_records:
            print(">> [gen_insert_sql] reached max_records, data may be incomplete! {}".format(sql))
            return None

        sql_list = []
        # DELETE 语句
        sql_delete = "DELETE FROM {}.{} where 1=1 AND {}".format(db_name, tb_name, where)
        sql_list.append(sql_delete)

        # INSERT 语句
        db_size = len(data_list)
        for i in range(0, 1 + int(db_size / batch_size)):
            idx_begin = i * batch_size
            idx_end = idx_begin + batch_size
            if idx_end > db_size:
                idx_end = db_size
            sql_insert_batch = MySQLUtil.gen_insert_sql(db_name, tb_name, data_list[idx_begin: idx_end])
            if sql_insert_batch is None:
                continue
            sql_list.append(sql_insert_batch)
        # end for
        return sql_list


if '__main__' == __name__:
    pass

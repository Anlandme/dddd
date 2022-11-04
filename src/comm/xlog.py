import os
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from .config_reader import ConfigReader


class XlogConfig(object):
    def __init__(self
                 , log_level=logging.DEBUG
                 , console_log_flag=True
                 , console_log_level=logging.INFO
                 , file_log_flag=False
                 , file_log_level=logging.INFO
                 , file_log_path="../log"
                 , file_log_name="xlog.log"):
        self.log_level = log_level                  # 全局日志级别
        self.console_log_flag = console_log_flag    # 是否打印到控制台
        self.console_log_level = console_log_level  # 控制台日志级别
        self.file_log_flag = file_log_flag          # 是否打印到文件
        self.file_log_level = file_log_level        # 文件日志级别
        self.file_log_path = file_log_path          # 文件日志路径
        self.file_log_name = file_log_name          # 文件日志路径

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", "")

    @staticmethod
    def get_config(conf_file, conf_section="xlog"):
        config_reader = ConfigReader.get_instance(conf_file)
        log_level = config_reader.get(conf_section, "log_level")
        console_log_flag = config_reader.get(conf_section, "console_log_flag")
        console_log_level = config_reader.get(conf_section, "console_log_level")
        file_log_flag = config_reader.get(conf_section, "file_log_flag")
        file_log_level = config_reader.get(conf_section, "file_log_level")
        file_log_path = config_reader.get(conf_section, "file_log_path")
        file_log_name = config_reader.get(conf_section, "file_log_name")

        log_level = XlogConfig.get_log_level(log_level)
        console_log_level = XlogConfig.get_log_level(console_log_level)
        file_log_level = XlogConfig.get_log_level(file_log_level)

        if str(console_log_flag).lower() in ["y", 'true']:
            console_log_flag = True
        else:
            console_log_flag = False
        if str(file_log_flag).lower() in ["y", 'true']:
            file_log_flag = True
        else:
            file_log_flag = False
        if not console_log_flag and not file_log_flag:
            console_log_flag = True  # 至少开启1种日志模式
        if file_log_flag and not os.path.exists(file_log_path):
            os.makedirs(file_log_path)

        log_conf = XlogConfig(
            log_level, console_log_flag, console_log_level
            , file_log_flag, file_log_level, file_log_path, file_log_name
        )
        return log_conf

    @staticmethod
    def parse_dict(data_dict: dict):
        log_conf = XlogConfig()
        if data_dict is None or len(data_dict) == 0:
            return log_conf

        for key, value in data_dict.items():
            if key in log_conf.__dict__.keys():
                log_conf.__dict__[key] = value
        # end for
        if str(log_conf.console_log_flag).lower() in ["y", 'true']:
            log_conf.console_log_flag = True
        else:
            log_conf.console_log_flag = False
        if str(log_conf.file_log_flag).lower() in ["y", 'true']:
            log_conf.file_log_flag = True
        else:
            log_conf.file_log_flag = False
        if not log_conf.console_log_flag and not log_conf.file_log_flag:
            log_conf.console_log_flag = True
        if log_conf.file_log_flag and not os.path.exists(log_conf.file_log_path):
            os.makedirs(log_conf.file_log_path)
        return log_conf

    @staticmethod
    def get_log_level(log_level):
        log_level = logging.getLevelName(str(log_level).upper())
        if log_level is None:
            log_level = logging.INFO
        return log_level


class Xlog(object):
    def __init__(self, log_conf):
        """
           log_conf:  XlogConfig
        """
        if type(log_conf) == dict:
            log_conf = XlogConfig.parse_dict(log_conf)
        self.log_conf = log_conf
        self.logger = None
        if self.logger is None:
            self.init()

    def init(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_conf.log_level)
        self.logger.handlers = []

        # 控制台日志
        if self.log_conf.console_log_flag:
            handler_console = logging.StreamHandler()
            handler_console.setLevel(self.log_conf.console_log_level)
            handler_console.setFormatter(logging.Formatter(
                '[%(asctime)s %(levelname)s] %(process)d %(thread)d %(message)s'
            ))
            self.logger.addHandler(handler_console)

        # 文件日志
        if self.log_conf.file_log_flag:
            log_file = "{}/{}".format(self.log_conf.file_log_path, self.log_conf.file_log_name)
            handler_file = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=45)
            # handler_file.suffix = "%Y-%m-%d"
            # handler_file.extMatch = re.compile(r"log.^\d{4}-\d{2}-\d{2}$")
            handler_file.setLevel(self.log_conf.file_log_level)
            handler_file.setFormatter(logging.Formatter(
                fmt='[%(asctime)s %(levelname)s] %(process)d %(thread)d %(message)s'
                , datefmt='%Y-%m-%d %H:%M:%S'
            ))
            self.logger.addHandler(handler_file)
        # end if

    @staticmethod
    def get_logger(conf_file, conf_section="xlog"):
        log_conf = XlogConfig.get_config(conf_file, conf_section)
        return Xlog(log_conf)

    @staticmethod
    def get_default_logger(log_level="INFO"):
        """
            只在控制台打印日志
        """
        log_level = XlogConfig.get_log_level(log_level)
        return Xlog(XlogConfig(log_level))

    def set_level(self, log_level="INFO"):
        log_level = XlogConfig.get_log_level(log_level)
        self.logger.setLevel(log_level)

    def debug(self, msg, py_file=None, *args, **kwargs):
        if py_file:
            msg = "{} {}".format(os.path.basename(py_file), msg)
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, py_file=None, *args, **kwargs):
        if py_file:
            msg = "{} {}".format(os.path.basename(py_file), msg)
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, py_file=None, *args, **kwargs):
        if py_file:
            msg = "{} {}".format(os.path.basename(py_file), msg)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, py_file=None, *args, **kwargs):
        if py_file:
            msg = "{} {}".format(os.path.basename(py_file), msg)
        self.logger.error(msg, *args, **kwargs)

    def fatal(self, msg, py_file=None, *args, **kwargs):
        if py_file:
            msg = "{} {}".format(os.path.basename(py_file), msg)
        self.logger.fatal(msg, *args, **kwargs)

    def exception(self, msg, py_file=None, *args, exc_info=True, **kwargs):
        if py_file:
            msg = "{} {}".format(os.path.basename(py_file), msg)
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)
        self.error(traceback.format_exc())


if __name__ == '__main__':
    logger = Xlog.get_logger("../../conf/log.ini")
    logger.info("test 1")

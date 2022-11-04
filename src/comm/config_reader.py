"""
    解析系统配置文件: conf/*.ini
    注意：底层基础工具，禁止引入过多依赖
"""
import os
import json
import configparser


class ConfigUtil(object):
    @staticmethod
    def get_sys_path(py_file, sys_name=None):
        file_path = str(os.path.abspath(py_file))
        idx_sys_name = -1
        if sys_name and len(str(sys_name)) > 0:
            idx_sys_name = file_path.rfind(sys_name)

        idx_src = file_path.rfind("/src/")
        idx_tests = file_path.rfind("/tests/")

        if idx_sys_name > 0:
            sys_path = file_path[0:idx_sys_name + len(sys_name)]
        elif idx_src > 0:
            sys_path = file_path[0:idx_src]
        elif idx_tests > 0:
            sys_path = file_path[0:idx_tests]
        else:
            sys_path = "../"
        return sys_path

    @staticmethod
    def get_env(conf_file, conf_section="sys_info", conf_key="sys_env"):
        config_reader = ConfigReader.get_instance(conf_file)
        sys_env = config_reader.get(conf_section, conf_key)
        return sys_env

    @staticmethod
    def is_dev(conf_file, conf_section="sys_info", conf_key="sys_env"):
        # 判断是否为开发环境
        return "DEV" == ConfigUtil.get_env(conf_file, conf_section, conf_key)

    @staticmethod
    def is_test(conf_file, conf_section="sys_info", conf_key="sys_env"):
        # 判断是否为测试环境
        return "TEST" == ConfigUtil.get_env(conf_file, conf_section, conf_key)

    @staticmethod
    def is_prod(conf_file, conf_section="sys_info", conf_key="sys_env"):
        # 判断是否为生产环境
        return (ConfigUtil.get_env(conf_file, conf_section, conf_key)).startswith("PROD")

    @staticmethod
    def read_conf(conf_file):
        """
            读取配置文件
        :param conf_file: 配置文件
        :return: {
            section: {
                k1: v1,
                k2: v2,
            }
        }
        """
        if not os.path.exists(conf_file) or not os.path.isfile(conf_file):
            raise BaseException(">> [ConfigReader.read_conf] file not exist! {}".format(conf_file))
        conf_parse = configparser.ConfigParser()
        conf_parse.read(conf_file, "utf-8")

        conf_dict = {}
        conf_sections = conf_parse.sections()
        for section in conf_sections:
            section_dict = {}
            keys = conf_parse.options(section)
            for key in keys:
                section_dict[key] = conf_parse.get(section, key)
            conf_dict[section] = section_dict
        # end for
        return conf_dict


class ConfigReader(object):
    def __init__(self, conf_dict):
        self.conf_dict = conf_dict

    @staticmethod
    def get_instance(conf_file):
        conf_dict = ConfigUtil.read_conf(conf_file)
        instance = ConfigReader(conf_dict)
        return instance

    def get(self, section, key):
        result = ''
        if section in self.conf_dict:
            section_dict = self.conf_dict[section]
            if key in section_dict:
                result = section_dict[key]
        return result

    def get_int(self, section, key):
        result = 0
        if section in self.conf_dict:
            section_dict = self.conf_dict[section]
            if key in section_dict:
                result = int(section_dict[key])
        return result
    
    def get_float(self, section, key):
        result = 0
        if section in self.conf_dict:
            section_dict = self.conf_dict[section]
            if key in section_dict:
                result = float(section_dict[key])
        return result
    
    def get_dict(self, section, key):
        result = {}
        if section in self.conf_dict:
            section_dict = self.conf_dict[section]
            if key in section_dict:
                value = section_dict[key]
                result = json.loads(value)
        return result
        
    def get_section_dict(self, section):
        result = {}
        if section in self.conf_dict:
            result = self.conf_dict[section]
        return result

    def get_env(self, conf_section="sys_info", conf_key="sys_env"):
        sys_env = self.get(conf_section, conf_key)
        return sys_env

    def is_dev(self, conf_section="sys_info", conf_key="sys_env"):
        # 判断是否为开发环境
        return "DEV" == self.get_env(conf_section, conf_key)

    def is_test(self, conf_section="sys_info", conf_key="sys_env"):
        # 判断是否为测试环境
        return "TEST" == self.get_env(conf_section, conf_key)

    def is_prod(self, conf_section="sys_info", conf_key="sys_env"):
        # 判断是否为生产环境
        return (self.get_env(conf_section, conf_key)).startswith("PROD")


if "__main__" == __name__:
    # res = ConfigReader.read_conf("oversea_channel.ini")
    # print(res)
    pass

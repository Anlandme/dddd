import os

from src.comm.config_reader import ConfigReader, ConfigUtil
from src.comm.xlog import Xlog


# config file
abs_path = str(os.path.abspath(__file__))
sys_path = os.path.abspath("../../../")
conf_file_sys = "../conf/sys.ini".format(sys_path)

# config instance
conf_sys = ConfigReader.get_instance(conf_file_sys)

# common instance
sys_tag = conf_sys.get("sys_info", "sys_tag")
logger = Xlog.get_logger(conf_file_sys, conf_section="xlog")

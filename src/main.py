from flask import Flask
from flask_cors import CORS
from src.common import conf_sys

from src.api.api_check    import api as api_check
from src.api.api_economic import api as api_economic

def start_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 允许跨域

    # 加载配置
    config_info = {}
    app.config.from_object(config_info)
    app.config['JSON_AS_ASCII'] = False  # 返回数据中response为中文

    # 注册API
    app.register_blueprint(api_check)
    app.register_blueprint(api_economic)

    # 启动服务
    sys_host = conf_sys.get("sys_info", "sys_host")
    sys_port = conf_sys.get_int("sys_info", "sys_port")
    sys_debug = eval(conf_sys.get("sys_info", "sys_debug"))

    app.run(host=sys_host, port=sys_port, debug=sys_debug)


if __name__ == '__main__':


    start_app()


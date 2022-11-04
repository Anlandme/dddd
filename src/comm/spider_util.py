import requests
from bs4 import BeautifulSoup
from src import Xlog


class SpiderUtil(object):
    @staticmethod
    def get_charset(tag_html, logger=Xlog.get_default_logger()):
        try:
            meta_tags = tag_html.find_all("meta")
            for meta_tag in meta_tags:
                try:
                    tmp_str = str(meta_tag)
                    idx = tmp_str.find("charset=")
                    if idx >= 0:
                        # '<meta content="text/html;charset=utf-8" http-equiv="content-type"/>'
                        charset_str = tmp_str[idx + len("charset="): -1]
                        idx_end = charset_str.find('"')
                        if idx_end < 0:
                            idx_end = charset_str.find(";")
                        charset = charset_str[:idx_end]
                        return charset.lower().strip()
                except Exception as err1:
                    logger.warn(">> fail to get charset: {}".format(err1))
            # end for
        except Exception as err2:
            logger.warn(">> fail to get charset: {}".format(err2))

        logger.error(">> fail to get charset! use 'utf-8' as default!")
        return "utf-8"

    @staticmethod
    def get_tag_html(url, charset='utf-8', logger=Xlog.get_default_logger()):
        try:
            response = requests.get(url)
            response.encoding = charset
            tag_html = BeautifulSoup(response.text, "html.parser")
            return tag_html
        except Exception as err:
            logger.warn(">> fail to get tag_html: {}".format(err))
        return None

    @staticmethod
    def get_tag_html_local(local_file):
        """
            解析本地保存的HTML文件
        """
        file_reader = open(local_file)

        html_text = ""
        while True:
            line = file_reader.readline()
            if not line:
                break
            html_text += line
        # end while

        html_tag = BeautifulSoup(html_text, "html.parser")
        return html_tag

    @staticmethod
    def find_tag(tag_html, tag_name, tag_class=None, tag_id=None):
        """
            返回第一个满足条件的标签
        """
        if tag_html is None:
            return None

        if tag_class and tag_id:
            return tag_html.find(tag_name, class_=tag_class, id=tag_id)
        elif tag_class:
            return tag_html.find(tag_name, class_=tag_class)
        elif tag_id:
            return tag_html.find(tag_name, id=tag_id)
        else:
            return tag_html.find(tag_name)

    @staticmethod
    def find_tag_all(tag_html, tag_name, tag_class=None, tag_id=None):
        """
            返回所有满足条件的标签列表
        """
        if tag_html is None:
            return None

        if tag_class and tag_id:
            return tag_html.find_all(tag_name, class_=tag_class, id=tag_id)
        elif tag_class:
            return tag_html.find_all(tag_name, class_=tag_class)
        elif tag_id:
            return tag_html.find_all(tag_name, id=tag_id)
        else:
            return tag_html.find_all(tag_name)


if "__main__" == __name__:
    url = "https://www.xe.com/zh-CN/currencytables/?from=CNY&date=2021-01-01"
    tag_html = SpiderUtil.get_tag_html(url)

    # tag_name = "table"
    # tag_class = "currencytables__Table-xlq26m-3 jaGdii"
    # tag_id = "__next"
    #
    # result = tag_html.find("div", class_="tribal-fusion-ad__AdWrapper-sc-7nznaa-0 gKugcA advertSlot")
    # result = tag_html.find("div", id="focus-announcer")
    # print(result)

    # result = SpiderUtil.find_tag(tag_html, "div")
    # print(result)
    #
    result = SpiderUtil.find_tag_all(tag_html, "div")
    print(result)

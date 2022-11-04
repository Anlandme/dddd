

class HtmlTemplate(object):
    """
        HTM模版
    """
    # HTML 结构：<html> <head></head> <body></body> </html>
    TEMPLATE_HTML = """ <html> {} {} </html> """
    
    # HEADER 结构：<head> <meta></meta> <script></script> </head>
    TEMPLATE_HEAD = """ <head><meta charset="utf-8"> {} </head> """
    
    # BODY
    TEMPLATE_BODY = """
        <body style="height:100%; width: 100%; margin-left:2%;">
        {}
        {}
        </body> 
    """

    # CSS
    TEMPLATE_CSS = """
        <style>
            .mail-table {
                font-family: Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                min-width: 600px;
            }
        
            .mail-table td, .mail-table th {
                border: 1px solid #ddd;
                padding: 8px;
            }
        
            .mail-table tr:nth-child(even){background-color: #f2f2f2;}
        
            .mail-table tr:hover {background-color: #ddd;}
        
            .mail-table th {
                padding-top: 6px;
                padding-bottom: 6px;
                text-align: center;
                background-color: #3f98b1;
                color: white;
            }
            ol {
                list-style: none;
                counter-reset: steps;
            }
            ol li {
                counter-increment: steps;
            }
            ol li::before {
                content: counter(steps);
                margin-right: 0.5rem;
                background: #ff6f00;
                color: white;
                width: 1.2em;
                height: 1.2em;
                border-radius: 50%;
                display: inline-grid;
                place-items: center;
                line-height: 1.2em;
            }
            ol ol li::before {
                background: darkorchid;
            }
        </style>
    """

    # TABLE
    TEMPLATE_TABLE = """
         <table class="mail-table">
         <tbody> {} </tbody>
         </table> 
    """
    TEMPLATE_TABLE_TR = """ <tr> {} </tr> """
    TEMPLATE_TABLE_TH = """ <th> {} </th> """
    TEMPLATE_TABLE_TD = """ <td> {} </td> """
    TEMPLATE_TABLE_TD_LEFT = """ <td style="text-align:left;"> {} </td> """
    TEMPLATE_TABLE_TD_CENTER = """ <td style="text-align:center;"> {} </td> """
    
    @staticmethod
    def get_html(content):
        body = HtmlTemplate.TEMPLATE_BODY.format(HtmlTemplate.TEMPLATE_CSS, content)
        html = HtmlTemplate.TEMPLATE_HTML.format("", body)
        return html
    
    @staticmethod
    def get_table(dict_list):
        """
            字典列表数据转 HTML 表格
        :param dict_list:
        :return:
        """
        if dict_list is None or len(dict_list) == 0:
            return ""
        if type(dict_list[0]) == dict:
            fields = tuple(dict_list[0].keys())
        else:
            fields = tuple(dict_list[0].__dict__.keys())
        
        # 标题
        _head = ""
        for i in range(len(fields)):
            item = fields[i]
            _value = "{}".format(item)
            _head += HtmlTemplate.TEMPLATE_TABLE_TH.format(_value)
        _head_line = HtmlTemplate.TEMPLATE_TABLE_TR.format(_head)
        _content = _head_line
        
        # 内容
        for data in dict_list:
            if type(data) != dict:
                data = data.__dict__
            _data = ""
            for i in range(len(fields)):
                _key = fields[i]
                _value = HtmlTemplate.get_value(data, _key)
                _data += HtmlTemplate.TEMPLATE_TABLE_TD_CENTER.format(_value)
            _data_line = HtmlTemplate.TEMPLATE_TABLE_TR.format(_data)
            _content += _data_line
        
        _table = HtmlTemplate.TEMPLATE_TABLE.format(_content)
        return _table
    
    @staticmethod
    def get_value(data, key):
        if type(data) is dict and key in data:
            return data[key]
        else:
            return ""

import os
import pdfplumber
from .file_util import FileUtil


class PDFUtil(object):
    @staticmethod
    def list_to_str(list):
        if list is None or len(list) == 0:
            return ""
        result = ""
        for data in list:
            result += str(data).strip()
        return result
    
    @staticmethod
    def clean_str(str_input):
        """
            清理换行符，多个空格替换为单个空格
        :param str_input:
        :return:
        """
        if str_input is None:
            str_input = ""
            
        # temp = str(str_input).replace("\n", " ").strip()
        temp = str(str_input).replace("\n", "").strip()
        while temp.find("  ") >= 0:
            temp = temp.replace("  ", " ")
        return temp

    @staticmethod
    def read_text_from_pdf(file_input):
        idx = file_input.rfind("/")
        file_path = file_input[0:idx + 1]
        file_name = file_input[idx + 1:]
    
        # 解码PDF，保存到临时目录
        temp_path = "{}/temp_{}/".format(file_path, FileUtil.get_date_current(date_format="%Y%m%d%H%M%S"))
        temp_file = "{}/{}".format(temp_path, file_name)
        try:
            FileUtil.mk_dirs(temp_path)
            cmd_decrypt = "qpdf --password={} --decrypt {} {}".format("", file_input, temp_file)
            print("cmd_decrypt: {}".format(cmd_decrypt))
            os.system(cmd_decrypt)
        except Exception as error:
            print("fail to decrypt pdf! {}".format(error))
            temp_file = file_input
    
        file_content = []
        pdf = pdfplumber.open(temp_file)
        pdfplumber.set_debug(-1)
        for page in pdf.pages:
            page_text = page.extract_text()
            page_text = PDFUtil.clean_str(page_text)
            file_content.append(page_text)
        pdf.close()
    
        FileUtil.rm_file(temp_path)
        return file_content

    @staticmethod
    def read_words_from_pdf(file_input):
        idx = file_input.rfind("/")
        file_path = file_input[0:idx + 1]
        file_name = file_input[idx + 1:]
    
        # 解码PDF，保存到临时目录
        temp_path = "{}/temp_{}/".format(file_path, FileUtil.get_date_current(date_format="%Y%m%d%H%M%S"))
        temp_file = "{}/{}".format(temp_path, file_name)
        try:
            FileUtil.mk_dirs(temp_path)
            cmd_decrypt = "qpdf --password={} --decrypt {} {}".format("", file_input, temp_file)
            print("cmd_decrypt: {}".format(cmd_decrypt))
            os.system(cmd_decrypt)
        except Exception as error:
            print("fail to decrypt pdf! {}".format(error))
            temp_file = file_input
        
        file_content = []
        pdf = pdfplumber.open(temp_file)
        pdfplumber.set_debug(-1)
        for page in pdf.pages:
            page_words = page.extract_words(keep_blank_chars=True)
            for word in page_words:
                text = PDFUtil.clean_str(word["text"])
                file_content.append(text)
        pdf.close()
    
        FileUtil.rm_file(temp_path)
        return file_content

    @staticmethod
    def read_tables_from_pdf(file_input):
        idx = file_input.rfind("/")
        file_path = file_input[0:idx + 1]
        file_name = file_input[idx + 1:]
    
        # 解码PDF，保存到临时目录
        temp_path = "{}/temp_{}/".format(file_path, FileUtil.get_date_current(date_format="%Y%m%d%H%M%S"))
        temp_file = "{}/{}".format(temp_path, file_name)
        try:
            FileUtil.mk_dirs(temp_path)
            cmd_decrypt = "qpdf --password={} --decrypt {} {}".format("", file_input, temp_file)
            print("cmd_decrypt: {}".format(cmd_decrypt))
            os.system(cmd_decrypt)
        except Exception as error:
            print("fail to decrypt pdf! {}".format(error))
            temp_file = file_input
    
        file_content = []
        pdf = pdfplumber.open(temp_file)
        pdfplumber.set_debug(-1)
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:  # 表格
                _table = []
                for line in table:  # 行
                    _line = []
                    for content in line:  # 单元格
                        content = PDFUtil.clean_str(content)
                        _line.append(content)
                    _table.append(_line)
                file_content.append(_table)
            
        pdf.close()
        FileUtil.rm_file(temp_path)
    
        return file_content

    @staticmethod
    def get_dict(file_input):
        """
            个别数据有使用价值，使用时请先分析数据
        :param file_input:
        :return:
        """
        file_words = PDFUtil.read_words_from_pdf(file_input)
        data_size = len(file_words)
    
        file_dict = {}
        for i in range(0, data_size):
            key = file_words[i]
            if i + 1 < data_size:
                value = file_words[i + 1]
            else:
                value = ""
            file_dict[key] = value
    
        return file_dict
    
    @staticmethod
    def get_table(file_input, field_list):
        """
            获取PDF文档中指定的表格
        :param file_input:
        :param idx_table:
        :return: [{}, {}, {}]
        """
        
        # 获取所有的table
        tables = PDFUtil.read_tables_from_pdf(file_input)
        if tables is None or len(tables) == 0:
            return []

        # 获取目标表数据
        dict_list = []
        for table in tables:
            for i in range(0, len(table)):
                line = table[i]
                if i == 0:
                    if str(field_list[0]).strip().replace(" ", "").lower() \
                            == str(line[0]).strip().replace(" ", "").lower():
                        continue  # 目标表
                    else:
                        break  # 非目标表，跳到下一个表格
                else:
                    line_str = str(PDFUtil.list_to_str(line)).replace(" ", "").replace("\n", "")
                    if line_str == "":
                        continue  # 空行
                    line_dict = dict(zip(field_list, line))
                    dict_list.append(line_dict)
        return dict_list
      
        
if __name__ == '__main__':
    pass

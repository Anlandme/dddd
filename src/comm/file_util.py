import os
import shutil
import time
from hashlib import md5


class FileUtil(object):

    @staticmethod
    def write_file(file_path, data_list):
        """
            列表数据按行写入文件中
            适用于 txt、csv 等文本格式文件
        """
        file_object = open(file_path, 'w+')
        for line in data_list:
            file_object.write(str(line) + "\n")
        file_object.close()

    @staticmethod
    def split_file(file_path, target_path, line_count=10000000):
        if not FileUtil.file_exists(file_path):
            return
        file_name = FileUtil.get_file_name(file_path)
        file_name = "{}_split_".format(file_name[:file_name.find(".")])

        cmd_split = "cd {}; split -l {} {} {};".format(target_path, line_count, file_path, file_name)
        os.system(cmd_split)
        FileUtil.rm_file(file_path)
    
    @staticmethod
    def untar_file(file_path, target_path):
        if os.path.exists(target_path):
            FileUtil.rm_file(target_path)
        FileUtil.mk_dirs(target_path)
        cmd_untar = "tar -zxvf {} -C {}".format(file_path, target_path)
        os.system(cmd_untar)

    @staticmethod
    def unzip_file(file_path, target_path):
        if not os.path.exists(target_path):
            FileUtil.mk_dirs(target_path)
        cmd_untar = "unzip -o {} -d {}".format(file_path, target_path)
        if str(file_path).endswith(".zip"):
            os.system(cmd_untar)
        else:
            print("not zip file! {}".format(file_path))
    
    @staticmethod
    def file_exists(file_path):
        if not os.path.exists(file_path):
            print("file not exist! {}".format(file_path))
            return False
        if not os.path.isfile(file_path):
            print("not a file! {}".format(file_path))
            return False
        if os.path.getsize(file_path) <= 0:
            print("file is empty! {}".format(file_path))
            return False
        return True
    
    @staticmethod
    def build_file(path, file_name):
        result = "{}/{}".format(path, file_name)
        while result.find("//") >= 0:
            result = result.replace("//", "/")
        return result

    @staticmethod
    def get_file_md5(file_path):
        file_path = FileUtil.clean_path(file_path)
        file_path = file_path.replace(" ", "\\ ").replace("(", "\\(").replace(")", "\\)")
        cmd_md5 = "md5sum {}".format(file_path)
        res = os.popen(cmd_md5).readlines()[0]
        return str(res.split(" ")[0]).strip()
    
    @staticmethod
    def get_file_name(file_path):
        if file_path is None:
            return ""
        
        file_path = FileUtil.clean_path(file_path)

        idx = file_path.rfind("/")
        if idx >= 0:
            file_name = file_path[idx+1:]
        else:
            file_name = file_path
        return file_name
    
    @staticmethod
    def get_file_list(file_path, child=False, file_name_prefix='', file_name_suffix=''):
        file_list = []
        if not os.path.exists(file_path):
            print("不存在该类型的文件：", file_path)
            return file_list

        file_path = FileUtil.clean_path(file_path)
        if os.path.isfile(file_path):
            return [file_path]

        ret = os.listdir(file_path)
        for file_name in ret:
            if file_name.startswith(".") or file_name.startswith("~"):
                continue
            temp_path = FileUtil.build_file(file_path, file_name)
            if os.path.isdir(temp_path):
                if not child:
                    continue
                else:
                    file_list.extend(FileUtil.get_file_list(temp_path, child, file_name_prefix, file_name_suffix))
            elif os.path.isfile(temp_path):
                if (
                    file_name_prefix is None or file_name_prefix.strip() == "" or file_name.startswith(file_name_prefix)
                ) and (
                    file_name_suffix is None or file_name_suffix.strip() == "" or file_name.endswith(file_name_suffix)
                ):
                    # 是文件，且前后缀满足要求
                    temp_path = str(temp_path)
                    file_list.append(temp_path)
        # end for
        return file_list

    @staticmethod
    def get_field_list(size):
        if size <= 0:
            return []
        
        field_list = []
        for i in range(0, size):
            temp = "00" + str(i+1)
            col_name = "col_" + temp[-2:]
            field_list.append(col_name)
        # end for
        return field_list
    
    @staticmethod
    def get_date_current(date_format="%Y-%m-%d %H:%M:%S"):
        """
            获取当天的日期
        :param date_format:
        :return:
        """
        return time.strftime(date_format, time.localtime(time.time()))
    
    @staticmethod
    def is_empty(input_str):
        if input_str is None or input_str.strip() == "":
            return True
        return False
    
    @staticmethod
    def is_not_empty(input_str):
        return not FileUtil.is_empty(input_str)
    
    @staticmethod
    def rm_file(file_path):
        file_path = os.path.abspath(file_path)
        if file_path.count("/") <= 3 or len(file_path.strip()) <= 15:
            # 限制目录层级，防止误操作系统文件（".", "./" ,"./*", "/", "/*"）
            print("No permission to remove {}".format(file_path))
            raise UserWarning("No permission to remove {}".format(file_path))
        
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            elif os.path.isfile(file_path):
                os.remove(file_path)
            else:
                print("Illegal file ! {}".format(file_path))
                return False
        return True

    @staticmethod
    def mk_dirs(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def rebuild_file_path(file_path):
        """
            优化文件路径，移除多余的"/"
        :param file_path:
        :return:
        """
        if file_path is None:
            return ""
    
        temp_path = str(file_path).strip()
        if FileUtil.is_empty(str(temp_path)):
            return ""
        while temp_path.find("//") >= 0:
            temp_path = temp_path.replace("//", "/")
        return temp_path

    @staticmethod
    def get_file_content(file_path):
        if file_path is None:
            return ""
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return ""

        content = ""
        file_reader = open(file_path)
        while True:
            line = file_reader.readline()
            if not line:
                break
            content += line
        file_reader.close()
        return content

    @staticmethod
    def get_dir_md5(file_path):
        file_path = FileUtil.clean_path(file_path)
        file_list = FileUtil.get_file_list(file_path)

        md5_list = []
        for file_item in file_list:
            if file_item.startswith(".") or file_item.startswith("~"):
                continue
            file_md5 = FileUtil.get_file_md5(file_item)
            md5_list.append(file_md5)
        # end for
        md5_list = sorted(md5_list)
        md5_str = "#".join(md5_list)
        return md5(str(md5_str).strip().encode("utf-8")).hexdigest()

    @staticmethod
    def update_local_md5(file_path, local_file_info="./local_file_info.csv"):
        FileUtil.remove_local_md5(file_path, local_file_info)
        FileUtil.add_local_md5(file_path, local_file_info)

    @staticmethod
    def add_local_md5(file_path, local_file_info="./local_file_info.csv"):
        if not os.path.exists(local_file_info):
            cmd_touch = "touch {}".format(local_file_info)
            ret_touch = os.popen(cmd_touch).readlines()
            print(">> [cmd_touch: {}] [ret_touch: {}]".format(cmd_touch, ret_touch))

        # 文件信息
        file_path = FileUtil.clean_path(file_path)
        file_key = "KEY_{}".format(md5(str(file_path).strip().encode("utf-8")).hexdigest())
        file_md5 = FileUtil.get_dir_md5(file_path)
        data_time = time.time()

        # 新增信息
        cmd_add = "echo {}###{}###{}###{} >> {} ".format(file_key, file_md5, data_time, file_path, local_file_info)
        ret_add = os.popen(cmd_add).readlines()
        print(">> [cmd_add: {}] [ret_add: {}]".format(cmd_add, ret_add))

    @staticmethod
    def remove_local_md5(file_path, local_file_info="./local_file_info.csv"):
        # 文件信息
        file_path = FileUtil.clean_path(file_path)
        file_key = "KEY_{}".format(md5(str(file_path).strip().encode("utf-8")).hexdigest())

        # 删除信息
        cmd_remove = "sed -i -e '/{}/d' {}".format(file_key, local_file_info)
        ret_remove = os.popen(cmd_remove).readlines()
        print(">> [cmd_remove: {}] [ret_remove: {}]".format(cmd_remove, ret_remove))

    @staticmethod
    def get_local_md5(file_path, local_file_info="./local_file_info.csv", timeout=24*60*60):
        if not os.path.exists(local_file_info):
            return None
        file_path = FileUtil.clean_path(file_path)
        file_key = "KEY_{}".format(md5(str(file_path).strip().encode("utf-8")).hexdigest())

        cmd_grep = "grep '{}' {}".format(file_key, local_file_info)
        # cmd_grep += " | awk -F '###' '{print $2 $3}'"
        ret_grep = os.popen(cmd_grep).readlines()
        print(">> [cmd_grep: {}] [ret_grep: {}]".format(cmd_grep, ret_grep))
        if ret_grep is None or len(ret_grep) != 1:
            return None

        file_key, file_md5, file_time, file_info = str(ret_grep[0]).replace("\n", "").split("###")
        if time.time() - float(file_time) > timeout:
            FileUtil.remove_local_md5(file_path, local_file_info)
            return None
        return file_md5

    @staticmethod
    def check_local_md5(file_path, local_file_info="./local_file_info.csv", timeout=24*60*60):
        if not os.path.exists(local_file_info):
            return False
        file_path = FileUtil.clean_path(file_path)

        file_md5 = FileUtil.get_dir_md5(file_path)
        local_md5 = FileUtil.get_local_md5(file_path, local_file_info, timeout)
        if local_md5 is None or local_md5 != file_md5:
            return False
        return True

    @staticmethod
    def clean_path(file_path):
        file_path = str(os.path.abspath(file_path)).strip()
        while file_path.find("//") >= 0:
            file_path = file_path.replace("//", "/")
        if file_path.endswith("/"):
            file_path = file_path[:-1]
        return file_path


if "__main__" == __name__:
    file_path = "./http_client.py"
    FileUtil.update_local_md5(file_path)
    res = FileUtil.get_local_md5(file_path)
    print(res)

    # time.sleep(5)
    # res = FileUtil.get_local_md5(file_path, timeout=5)
    # print(res)

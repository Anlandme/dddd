import os
import gzip
import zipfile
import tarfile
import bz2
import queue


class FileType(object):
    FILE_TYPE_TEXT = 1
    FILE_TYPE_GZIP = 2
    FILE_TYPE_ZIP = 3
    FILE_TYPE_BZ2 = 4
    FILE_TYPE_TGZ = 5
  
    
class FileParser(object):
    """
        when using, need catch IOError
    """
    def __init__(self, file_name, field_list, field_sep, file_type=FileType.FILE_TYPE_TEXT):
        print(">> FileParser: {}".format(file_name))
        self.file_name = file_name
        self.filed_list = field_list
        self.filed_sep = field_sep
        self.file_handle = None
        self.file_type = file_type
        self.line = ""
        self.tar_file = None
        self.tar_file_members = queue.Queue()

    def __iter__(self):
        if FileType.FILE_TYPE_GZIP == self.file_type:
            self.file_handle = gzip.open(self.file_name, "rt", encoding="utf-8")
        elif FileType.FILE_TYPE_ZIP == self.file_type:
            self.file_handle = zipfile.ZipFile(self.file_name, "r")
        elif FileType.FILE_TYPE_BZ2 == self.file_type:
            self.file_handle = bz2.open(self.file_name, "rt", encoding="utf-8")
        elif FileType.FILE_TYPE_TGZ == self.file_type:
            self.tar_file = tarfile.open(self.file_name, "r:gz")
            for member in self.tar_file.getmembers():
                if member.isfile():
                    self.tar_file_members.put(member)
        else:
            self.file_handle = open(self.file_name, 'r')

        return self

    def __next__(self):
        try:
            if FileType.FILE_TYPE_TGZ == self.file_type and self.file_handle is None:
                if self.tar_file_members.empty():
                    raise StopIteration
                self.file_handle = self.tar_file.extractfile(self.tar_file_members.get())
                if self.file_handle is None:
                    raise StopIteration
            self.line = self.file_handle.readline()
            if self.line == "":
                self.file_handle.close()
                self.file_handle = None
                raise StopIteration
            if self.line[-1] == os.linesep:
                line_array = self.line[:-1].split(self.filed_sep)
            else:
                line_array = self.line.split(self.filed_sep)
            line_dict = dict(zip(self.filed_list, line_array))
        except IOError as error:
            print("FileParser read {0} failed: {1}".format(self.file_name, error))
            raise error

        return line_dict

    def close(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None


if "__main__" == __name__:
    pass

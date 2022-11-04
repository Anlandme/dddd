import csv


class CsvParser(object):
    def __init__(self, file_path, field_list, encoding="utf-8"):
        print(">> parse csv: {}".format(file_path))
        self.file_path = file_path
        self.field_list = field_list
        self.encoding = encoding
        self.file_io = None
        self.file_reader = None
        
    def __iter__(self):
        self.file_io = open(self.file_path, "r", encoding=self.encoding)
        self.file_reader = csv.reader(self.file_io)
        return self
    
    def __next__(self):
        line = next(self.file_reader)
        line_dict = dict(zip(self.field_list, line))
        return line_dict

    def close(self):
        if self.file_io:
            self.file_io.close()

    @staticmethod
    def write_csv(data_list, csv_file_path, write_title=True):
        if data_list is None or len(data_list) == 0:
            print(">> no data to save!")
            return

        file_writer = open(csv_file_path, 'w', encoding='utf-8')
        # title
        field_list = data_list[0].keys()
        if write_title:
            line_str = ""
            for key in field_list:
                value = str(key).strip()
                if value.find(",") >= 0:
                    if value.find('"') >= 0:
                        value.replace('"', '\\"')
                    value = '"{}"'.format(value)
                line_str += "{},".format(value)
            # end for
            line_str = "{}\n".format(line_str[:-1])
            file_writer.write(line_str)

        # content
        for line in data_list:
            line_str = ""
            for key in field_list:
                value = str(line[key]).strip()
                if value.find(",") >= 0:
                    if value.find('"') >= 0:
                        value.replace('"', '\\"')
                    value = '"{}"'.format(value)
                line_str += "{},".format(value)
            # end for
            line_str = "{}\n".format(line_str[:-1])
            file_writer.write(line_str)
        # end for
        file_writer.close()


if __name__ == '__main__':
    data_list = [{"name": "henry", "job": "dev"}, {"name": "henry2", "job": "dev2"}]
    CsvParser.write_csv(data_list, "./test_attatch.csv", write_title=True)
    CsvParser.write_csv(data_list, "./test_attatch02.csv", write_title=True)

import json


class BeanError(UserWarning):
    def __init__(self, code=-100, message='BEAN_ERROR'):
        self.code = code
        self.message = message

    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')


class BeanUtil(object):
    @staticmethod
    def parse2bean(data, cls):
        if data is None or isinstance(data, cls):
            return data
        if type(data) != dict:
            raise BeanError(message="Fail to parse bean! {}".format(data))

        bean_data = cls()
        bean_keys = bean_data.__dict__.keys()

        bean_dict = {}
        for key in bean_keys:
            if key in data:
                bean_dict[key] = data[key]
        # end for

        bean_data.__dict__.update(bean_dict)
        return bean_data

    @staticmethod
    def parse2bean_list(data_list, cls):
        if data_list is None or len(data_list) == 0:
            return None
        if type(data_list) != list:
            raise BeanError(message="Fail to parse bean list! {}".format(data_list))

        bean_list = []
        for data in data_list:
            bean_data = BeanUtil.parse2bean(data, cls)
            if bean_data is not None:
                bean_list.append(bean_data)
        # end for

        return bean_list


class BaseBean(object):
    def __str__(self):
        if self is None:
            return "{}"
        else:
            return str(self.__dict__).replace("'", '"')

    def decode(self, data):
        if isinstance(data, BaseBean):
            data = data.__dict__
        elif type(data) == str:
            data = json.loads(str(data).replace("'", '"'))

        if type(data) != dict:
            raise BeanError(message="Fail to decode! {}".format(data))

        bean_dict = {}
        bean_keys = self.__dict__.keys()
        for key in bean_keys:
            if key in data:
                bean_dict[key] = data[key]
        # end for

        self.__dict__.update(bean_dict)
        return self

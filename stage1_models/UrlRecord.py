"""
    Class UrlRecord:
        A single url record.
"""
from urllib import unquote

__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


class UrlRecord:
    def __init__(self, content_list=[''] * 13):
        """
        :param content_list: list[13] -- original flow record's 13 fields.

        """

        """
            Set useful field
        """
        self.__content = '\t'.join(content_list)
        self.__timeStamp = content_list[_access_time]
        self.__sip = content_list[_sip]
        self.__method = content_list[_method]
        self.__url = content_list[_uri]
        self.__host = content_list[_host]
        self.__ua = content_list[_uagent]
        self.__refer = content_list[_refer]
        self.__data = content_list[_data]

        """
            Encoding path and parameter segment
        """
        self.__path_code = self.__set_path_code(self.__url)
        self.__para_code = self.__set_para_code(self.__url)

        """
            Set url Parameter Status:
                __para_status_dict = {'path': path_code, 'para': {variable1: ([special_symbols]),
                                                                  variable2: ([special_symbols]), ...}}
                draw structure:
                    'path': path_code

                            -- variable_1 : (['?', ':', ...]) -- the 'special_symbols' set of the value
                    'para'  -- variable_2 : (['@', ...])
                            -- variable_3 : (['//', ...])

                or
                __para_status_dict = {'path': path_code, 'para': 'NOT_EXIST'}

        """
        self.__para_status_dict = self.__set_para_status(content_list[_uri])

    @staticmethod
    def __set_path_code(url):
        path = url.split('?', 1)[0]
        # decoding the url
        while True:
            path_uncode = unquote(path)
            if path_uncode == path:
                break
            path = path_uncode
        # combining the numerical part
        path_list = path.split('/')
        path_code = []
        for part in path_list:
            part_list = []
            number_flag = False
            for a_char in part:
                if a_char.isdigit():
                    if not number_flag:
                        number_flag = True
                        part_list.append('D')
                else:
                    number_flag = False
                    part_list.append(a_char)
            path_code.append(''.join(part_list))
        path_code = 'PATH_HEAD' + '/'.join(path_code) + '/PATH_END'
        return path_code

    @staticmethod
    def __set_para_code(url):
        path = url.split('?', 1)[0]
        para = url.lstrip(path)
        while True:
            para_uncode = unquote(para)
            if para_uncode == para:
                break
            para = para_uncode
        return para

    def __set_para_status(self, a_uri):
        para_status_dict = dict()
        para_status_dict['path'] = self.__path_code
        if '?' in a_uri:
            para_seg = a_uri.split('?', 1)[1]
            paras = para_seg.split('&')
            var_value_dict = {}
            for item in paras:
                # decoding the parameter
                while True:
                    item_uncode = unquote(item)
                    if item_uncode == item:
                        break
                    item = item_uncode
                try:
                    variable, value = item.split('=', 1)
                    # counting the special symbols set
                    special_symbols_set = self.__find_special_symbols(value)
                    var_value_dict[variable] = special_symbols_set
                except ValueError:
                    # for a parameter part which just contain value. e.g. /a?b=2&97198.jpg, we ignore it.
                    continue
            para_status_dict['para'] = var_value_dict
        else:
            para_status_dict['para'] = 'NOT_EXIST'
        return para_status_dict

    @staticmethod
    def __find_special_symbols(value_str):
        """
        :param value_str: the url parameter segment's value.
        :return: the set of the special symbols that value_str contains.
        """
        special_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '{', '}',
                           '[', ']', ',', '<', '>', '?', "'", '\\', '"', ':', ';', '=']
        special_symbols_set = set()
        for a_char in value_str:
            if a_char in special_symbols:
                special_symbols_set.add(a_char)
        return special_symbols_set

    def __eq__(self, other):
        """
        :param other: UrlRecord -> the url to be compared
        :return: boolean -> True(equal) or False(not equal)
        """
        if self.__path_code == other.get_path_code():
            return True
        else:
            return False

    def __hash__(self):
        """
        :return: int -- the hash value of this UrlRecord
        """
        return hash(self.__path_code)

    def get_path_code(self):
        """
        get url's encoded path segment.
        :return: str -> encoded path segment
        """
        return self.__path_code

    def get_para_code(self):
        """
        get url's encoded parameter segment.
        :return: str -> encoded parameter segment
        """
        return self.__para_code

    def get_para_status(self):
        """
        get the parameter dict of the url.
        :return: dict -> parameter dict
        """
        return self.__para_status_dict

    def get_content(self):
        """
        get all fields of the record. Fields are separated by '\t'.
        :return: str -> content field
        """
        return self.__content

    def get_timestamp(self):
        """
        get the timestamp filed of the record.
        :return: str -> timestamp field
        """
        return self.__timeStamp

    def get_sip(self):
        """
        get the sip field of the record.
        :return: str -> sip field
        """
        return self.__sip

    def get_method(self):
        """
        get the method field of the record.
        :return: str -> method field
        """
        return self.__method

    def get_url(self):
        """
        get the url field of the record.
        :return: str -> url field
        """
        return self.__url

    def get_host(self):
        """
        get the host field of the record.
        :return: str -> host field
        """
        return self.__host

    def get_ua(self):
        """
        get the user-agent field of the record.
        :return: str -> user-agent field
        """
        return self.__ua

    def get_refer(self):
        """
        get the reference field of the record.
        :return: str -> reference field
        """
        return self.__refer

    def get_data(self):
        """
        get data field of the record.
        :return: str -> data field
        """
        return self.__data

if __name__ == '__main__':
    pass

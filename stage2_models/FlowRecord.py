"""
    Class UrlRecord:
        A single url record.
"""
from urllib import unquote

__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


class FlowRecord:
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

        # Decoding and recording path and parameter segment. Meanwhile, generate the dict -> {variable: value}.
        self.__path, self.__para, self.__variable_value_dict = self.__set_url_code(self.__url)

        # Feature attribute
        self.__path_prop = None
        self.__specialSymbol_prop = None
        self.__enumeration = None
        self.__variable_composition = None
        self.__variable_order = None
        self.__value_length_prop = None
        self.__value_distribution1 = None
        self.__value_distribution2 = None

        # It map the private attribute string to it's value
        self.__attribute_map = {}

    @staticmethod
    def __set_url_code(url):
        if '?' in url:
            path, para = url.split('?', 1)
        else:
            path = url
            para = ""

        # decoding the path segment
        while True:
            path_decode = unquote(path)
            if path_decode == path:
                break
            path = path_decode

        # combine the successive numerical sequence.
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

        # decoding the parameter segment
        while True:
            para_decode = unquote(para)
            if para_decode == para:
                break
            para = para_decode
        para_code = para

        # generate the dict -> {variable: value}
        variable_value_dict = dict()
        if para != '':
            para_seg = para.split('&')
            for seg in para_seg:
                variable, value = seg.split('=', 1)
                variable_value_dict[variable] = value

        return path_code, para_code, variable_value_dict

    def __eq__(self, other):
        """
        :param other: UrlRecord -> the url to be compared
        :return: boolean -> True(equal) or False(not equal)
        """
        if self.__path == other.get_path() and self.__para == other.get_para():
            return True
        else:
            return False

    def __hash__(self):
        """
        :return: int -- the hash value of this UrlRecord
        """
        return hash(self.__path)

    def __setitem__(self, key, value):
        valid_key = ['path_prop', 'specialSymbol_prop', 'enumeration', 'variable_composition',
                     'variable_order', 'value_length_prop', 'value_distribution1', 'value_distribution2']
        if key in valid_key:
            self.__attribute_map[key] = value
        else:
            raise KeyError("%s is not a valid key." % key)

    def __getitem__(self, item):
        self.__generate_attribute_map()
        return self.__attribute_map[item]

    def __generate_attribute_map(self):
        self.__attribute_map["content"] = self.__content
        self.__attribute_map["timeStamp"] = self.__timeStamp
        self.__attribute_map["sip"] = self.__sip
        self.__attribute_map["method"] = self.__method
        self.__attribute_map["url"] = self.__url
        self.__attribute_map["host"] = self.__host
        self.__attribute_map["ua"] = self.__ua
        self.__attribute_map["refer"] = self.__refer
        self.__attribute_map["data"] = self.__data

        self.__attribute_map["path"] = self.__path
        self.__attribute_map["para"] = self.__para
        self.__attribute_map["variable_value_dict"] = self.__variable_value_dict

        self.__attribute_map['path_prop'] = self.__path_prop
        self.__attribute_map['specialSymbol_prop'] = self.__specialSymbol_prop
        self.__attribute_map['enumeration'] = self.__enumeration
        self.__attribute_map['variable_composition'] = self.__variable_composition
        self.__attribute_map['variable_order'] = self.__variable_order
        self.__attribute_map['value_length_prop'] = self.__value_length_prop
        self.__attribute_map['value_distribution1'] = self.__value_distribution1
        self.__attribute_map['value_distribution2'] = self.__value_distribution2

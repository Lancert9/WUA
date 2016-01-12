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
        # It map the private attribute string to it's value
        self.__attribute_map = {}

        """
            Set useful field
        """
        self.__attribute_map["content"] = '\t'.join(content_list)
        self.__attribute_map["timeStamp"] = content_list[_access_time]
        self.__attribute_map["sip"] = content_list[_sip]
        self.__attribute_map["method"] = content_list[_method]
        self.__attribute_map["url"] = content_list[_uri]
        self.__attribute_map["host"] = content_list[_host]
        self.__attribute_map["ua"] = content_list[_uagent]
        self.__attribute_map["refer"] = content_list[_refer]
        self.__attribute_map["data"] = content_list[_data]

        # Decoding and recording path and parameter segment. Meanwhile, generate the dict -> {variable: value}.
        self.__attribute_map["path"], self.__attribute_map["para"], self.__attribute_map["variable_value_dict"] = \
            self.__set_url_code(self.__attribute_map["url"])

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
        if para:
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
        if self.__attribute_map["path"] == other.get_path() and self.__attribute_map["para"] == other.get_para():
            return True
        else:
            return False

    def __hash__(self):
        """
        :return: int -- the hash value of this UrlRecord
        """
        return hash(self.__attribute_map["path"])

    def __setitem__(self, key, value):
        valid_key = ['path_prop', 'specialSymbol_prop', 'enumeration', 'variable_composition',
                     'variable_order', 'value_length_prop', 'value_distribution1', 'value_distribution2']
        if key in valid_key:
            self.__attribute_map[key] = value
        else:
            raise KeyError("%s is not a valid key." % key)

    def __getitem__(self, item):
        return self.__attribute_map[item]

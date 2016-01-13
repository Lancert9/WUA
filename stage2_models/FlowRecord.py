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
        self._m = {}

        """
            Set useful field
        """
        self._m["content"] = '\t'.join(content_list)
        self._m["timeStamp"] = content_list[_access_time]
        self._m["sip"] = content_list[_sip]
        self._m["method"] = content_list[_method]
        self._m["url"] = content_list[_uri]
        self._m["host"] = content_list[_host]
        self._m["ua"] = content_list[_uagent]
        self._m["refer"] = content_list[_refer]
        self._m["data"] = content_list[_data]

        # Decoding and recording path and parameter segment. Meanwhile, generate the dict -> {variable: value}.
        self._m["path"], self._m["para"], self._m["variable_value_dict"] = \
            self.__set_url_code(self._m["url"])

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
        if para_code:
            para_seg = para_code.split('&')
            for seg in para_seg:
                variable_value = seg.split('=', 1)
                if len(variable_value) == 1:
                    variable = 'Default_Variable'
                    value = variable_value[0]
                else:
                    variable, value = variable_value
                variable_value_dict[variable] = value

        return path_code, para_code, variable_value_dict

    def __eq__(self, other):
        """
        :param other: UrlRecord -> the url to be compared
        :return: boolean -> True(equal) or False(not equal)
        """
        if self._m["path"] == other.get_path() and self._m["para"] == other.get_para():
            return True
        else:
            return False

    def __hash__(self):
        """
        :return: int -- the hash value of this UrlRecord
        """
        return hash(self._m["content"])

    def __setitem__(self, key, value):
        valid_key = ['path_prop', 'specialSymbol_prop', 'enumeration', 'variable_composition',
                     'variable_order', 'value_length_prop', 'value_distribution1', 'value_distribution2']
        if key in valid_key:
            self._m[key] = value
        else:
            raise KeyError("%s is not a valid key." % key)

    def __getitem__(self, item):
        return self._m[item]

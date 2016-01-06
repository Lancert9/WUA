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
            Decoding and recording path and parameter segment
        """
        self.__path_code, self.__para_code = self.__set_url_code(self.__url)

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

        # decoding the parameter segment
        while True:
            para_decode = unquote(para)
            if para_decode == para:
                break
            para = para_decode
        para_code = para

        return path_code, para_code

    def __eq__(self, other):
        """
        :param other: UrlRecord -> the url to be compared
        :return: boolean -> True(equal) or False(not equal)
        """
        if self.__path_code == other.get_path_code() and self.__para_code == other.get_para_code():
            return True
        else:
            return False

    def __hash__(self):
        """
        :return: int -- the hash value of this UrlRecord
        """
        return hash(self.__path_code)

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

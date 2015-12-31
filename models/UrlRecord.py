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
        self.__content = '\t'.join(content_list)
        self.__sip = content_list[_sip]
        self.__host = content_list[_host]
        self.__url = content_list[_uri]
        self.__timeStamp = content_list[_access_time]
        """
            Url Path Status
        """
        self.__path_length = self.__setPathLength(content_list[_uri])
        self.__path_code = self.__setPathCode(content_list[_uri])
        self.__para_code = self.__setParaCode(content_list[_uri])
        """
            Url Parameter Status
        """
        """
                __para_status_dict = {'path': path_code, 'para': {variable1: ([special_symbols]), variable2: ([special_symbols]), ...}}
                draw structure:
                    'path': path_code

                            -- variable_1 : (['?', ':', ...]) -- the 'special_symbols' set of the value
                    'para'  -- variable_2 : (['@', ...])
                            -- variable_3 : (['//', ...])

                or
                __para_status_dict = {'path': path_code, 'para': 'NOT_EXIST'}

        """
        self.__para_status_dict = self.__setParaStatus(content_list[_uri])

    def __setPathLength(self, url):
        path_length = url.count('/')
        return path_length

    def __setPathCode(self, url):
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

    def __setParaCode(self, url):
        path = url.split('?', 1)[0]
        para = url.lstrip(path)
        while True:
            para_uncode = unquote(para)
            if para_uncode == para:
                break
            para = para_uncode
        return para

    # def __setPathCode(self, url):
    #     if '?' in url:
    #         tmp = url.split('?', 1)
    #         path_seg = tmp[0]
    #         path = path_seg
    #     else:
    #         path = url
    #     parts = path.split('/')[1:]
    #     parts_code = [self.__pathcodeTran(i) for i in parts]
    #     path_code = 'PATH_HEAD/' + '/'.join(parts_code) + '/PATH_END'
    #     return path_code
    #
    # def __pathcodeTran(self, origin_s):
    #     tmp = re.split('\W', origin_s)
    #     for (index, item) in enumerate(tmp):
    #         item = item.replace('_', '')    # delete '_'
    #         if item == '':
    #             tmp[index] = '0'
    #         elif item.isalpha():
    #             tmp[index] = item
    #         elif item.isdigit():
    #             tmp[index] = 'D'
    #         elif item.isalnum():
    #             tmp[index] = 'N'
    #         else:
    #             tmp[index] = 'X'
    #     code = '%'.join(tmp)
    #     return code

    def __setParaStatus(self, a_uri):
        para_status_dict = {}
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
                    special_symbols_set = self.__findSpecialSymbols(value)
                    var_value_dict[variable] = special_symbols_set
                except ValueError:
                    # for a parameter part which just contain value. e.g. /a?b=2&97198.jpg, we ignore it.
                    continue
            para_status_dict['para'] = var_value_dict
        else:
            para_status_dict['para'] = 'NOT_EXIST'
        return para_status_dict

    def __findSpecialSymbols(self, origin_s):
        special_symbols = set(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '{', '}', '[', ']', ',', '<', '>', '?', "'", '\\', '"', ':', ';', '='])
        special_symbols_list = set()
        for a_char in origin_s:
            if a_char in special_symbols:
                special_symbols_list.add(a_char)
        return special_symbols_list

    def getPathCode(self):
        """
        get the encoded path of the url.
        :return: str
        """
        return self.__path_code

    def getPathLength(self):
        """
        get the length of the url path.
        :return: int
        """
        return self.__path_length

    def getParaCode(self):
        return self.__para_code

    def getParaStatus(self):
        """
        get the parameter dict of the url.
        :return: dict
        """
        return self.__para_status_dict

    def getSip(self):
        """
        get the sip field of the record.
        :return: str
        """
        return self.__sip

    def getHost(self):
        """
        get the host field of the record.
        :return: str
        """
        return self.__host

    def getUrl(self):
        """
        get the url field of the record.
        :return: str
        """
        return self.__url

    def getTimeStamp(self):
        return self.__timeStamp

    def getContent(self):
        """
        get all fields of the record. Fields are separated by '\t'.
        :return: str
        """
        return self.__content

    def __eq__(self, other):
        """
        :param other: UrlRecord
        :return: boolean
        """
        if self.__path_code == other.getPathCode():
            return True
        else:
            return False

    def __hash__(self):
        """
        :return: int -- the hash value of this UrlRecord
        """
        return hash(self.__path_code)


if __name__ == '__main__':
    pass

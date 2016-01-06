"""
    Class RecordBox:
        It contains all training records corresponding to a single hosts.
        It also contains some metrics of records.

"""
__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


class RecordBox:
    def __init__(self):
        self.__all_records = list()
        self.__sip_box = set()

        self.__path_code_list = list()
        self.__para_code_dict = dict()

    def add_record(self, a_record):
        self.__all_records.append(a_record)
        a_sip = a_record.get_sip()
        self.__sip_box.add(a_sip)

    def get_record_num(self):
        return len(self.__all_records)

    def get_sip_num(self):
        return len(self.__sip_box)

    def active(self):
        for record in self.__all_records:
            # add path segment
            path_code = record.get_path_code()
            self.__path_code_list.append(path_code)

            # add parameter segment
            para_code = record.get_para_code()
            

    def get_path_code_list(self):
        return self.__path_code_list

    def get_para_code_list(self):
        return self.__para_code_dict

    def clear(self):
        pass


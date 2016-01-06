"""
    Class RecordBox:
        It contains all training records corresponding to a single hosts.
        It also contains some metrics of records.

"""
__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


class RecordBox:
    def __init__(self):
        self.__record_box = list()
        self.__sip_box = set()

    def add_record(self, a_record):
        self.__record_box.append(a_record)
        a_sip = a_record.get_sip()
        self.__sip_box.add(a_sip)

    def get_record_num(self):
        return len(self.__record_box)

    def get_sip_num(self):
        return len(self.__sip_box)

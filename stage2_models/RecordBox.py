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

        self.__path_list = list()
        self.__variable_specialSymbol = dict()
        self.__variable_value = dict()
        self.__variable_composition = dict()
        self.__variable_order = dict()

        # It map the private attribute string to it's value
        self.__attribute_map = {}
        self.__generate_attribute_map()

    def add_record(self, a_record):
        self.__all_records.append(a_record)
        a_sip = a_record.get_sip()
        self.__sip_box.add(a_sip)

    def active(self):
        for record in self.__all_records:
            # add path segment
            path_code = record.get_path()
            self.__path_list.append(path_code)

            # add parameter segment
            para_code = record.get_para()

    def clear(self):
        pass

    def __setitem__(self, key, value):
        raise LookupError("It is not allow to set the attribute.")

    def __getitem__(self, item):
        return self.__attribute_map[item]

    def __generate_attribute_map(self):
        self.__attribute_map["record_num"] = len(self.__all_records)
        self.__attribute_map["sip_num"] = len(self.__sip_box)
        self.__attribute_map["path_list"] = self.__path_list
        self.__attribute_map["variable_specialSymbol"] = self.__variable_specialSymbol
        self.__attribute_map["variable_value"] = self.__variable_value
        self.__attribute_map["variable_composition"] = self.__variable_composition
        self.__attribute_map["variable_order"] = self.__variable_order

"""
    Class HostCollector:
        This class contains the map relationship from host to HostModel.
"""
from HostModel import HostModel

__author__ = 'j-lijiawei'


class HostCollector:
    def __init__(self):
        self.__hosts = {}   # @item host(str) : host-model(HostModel)

    def get_host_model(self, host):
        """
        Depending on a host, get the HostModel.
        :param host: str -> the destination host
        :return: HostModel -> the destination host-model
        """
        if host in self.__hosts:
            return self.__hosts[host]
        else:
            host_model = HostModel(host)
            self.__hosts[host] = host_model
            return host_model

    def show_collector(self):
        """
        When testing this Class, it sometimes need to return the collector.
        :return: dict -> {str: HostModel}
        """
        return self.__hosts

    def __iter__(self):
        return IterableCollector(self.__hosts)

    def __len__(self):
        return len(self.__hosts)


class IterableCollector:
    def __init__(self, host_dict):
        self.__host_dict = host_dict
        self.__key_list = self.__host_dict.keys()
        self.__index = 0

    def next(self):
        key = self.__key_list[self.__index]
        self.__index += 1
        return self.__host_dict[key]

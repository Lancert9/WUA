"""
    Class HostCollector:
        This class contains the map relationship from host to HostModel.
"""
from HostModel import HostModel

__author__ = 'j-lijiawei'


class HostCollector:
    def __init__(self):
        self.__hosts = {}   # @item host(str) : host-model(HostModel)

    def getHostModel(self, host):
        """
        Depending on a host, get the HostModel.
        :param host: str
        :return: HostModel
        """
        if host in self.__hosts:
            return self.__hosts[host]
        else:
            host_model = HostModel(host)
            self.__hosts[host] = host_model
            return host_model

    def showCollector(self):
        """
        When testing this Class, it sometimes need to return the collector.
        :return: dict --> {str: ModelHost}
        """
        return self.__hosts

"""
    Class AnomalyCollector:
        Containing the statistical information of detected anomaly.
        It is temporary unused.
"""

__author__ = 'j-lijiawei'


class AnomalyCollector:
    def __init__(self):
        self.__anomalies = []    # @item a url record
        self.__host_sip = {}    # @item host map to sips(a set)

    def addAnomaly(self, a_record):
        """
        When add a UrlRecord, record it's information.
        :param a_record: UrlRecord
        """
        self.__anomalies.append(a_record)
        host = a_record.get_host()
        sip = a_record.get_sip()
        if host in self.__host_sip:
            self.__host_sip[host].add(sip)
        else:
            self.__host_sip[host] = set(sip)

    def getSipNum(self, a_host):
        """
        Depending on a given host, return it's number of different number.
        :param a_host: str
        :return: int
        """
        return len(self.__host_sip[a_host])

"""
    Class HostModel:
        The model of a specific host.
        It contains the host's RecordBox and all features.
"""
from PatternController import PatternController

__author__ = 'j-lijiawei'


class HostModel:
    def __init__(self, host_name=''):
        """
        :param host_name: str -> the host of this HostModel.

        """
        """
            Model Status
        """
        self.__hostname = host_name     # The host of this host model
        self.__pattern_controller = PatternController()     # Determine when to calculate the whole model
        self.__records = {}    # @item: a record map to it's amount
        self.__url_amount = 0   # total amount of records which are related to this host
        self.__sips = set()     # contain the different sips
        self.__detect_flag = 'Study...'

    def addUrl(self, a_record):
        """
        When adding a UrlRecord, it is need to count this record's attribute to the HostModel.
        :param a_record: UrlRecord
        """
        # count new record into the host model
        if a_record in self.__records:
            self.__records[a_record] += 1
        else:
            self.__records[a_record] = 1
        self.__url_amount += 1
        sip = a_record.get_sip()
        self.__sips.add(sip)

        # add new record's path into model's path status
        a_path = a_record.get_path_code()
        self.__pathCellCount(a_path)

        # add new record's parameter into model's parameter status
        a_para_status_dict = a_record.get_para_status()
        self.__paraStatusCount(a_para_status_dict)

        pattern_flag = self.__pattern_controller.judgePattern(self)
        if pattern_flag == 'Anomaly detection':
            print "Model is Ready. Begin to detecting..."
            self.__detect_flag = 'Study ready'
            self.__calModelProp()
            # self.__writeModelRecords()
            # self.__writeParaProp()

    def getUrlAmount(self):
        """
        get the number of UrlRecords that this HostModel has been studied.
        :return: int
        """
        return self.__url_amount

    def getDifUrlAmount(self):
        """
        get the number of different UrlRecords that this HostModel has been studied.
        :return:
        """
        return len(self.__records)

    def getSipAmount(self):
        """
        get the number of different sip field that this HostModel has been studied.
        :return:
        """
        return len(self.__sips)

    def getHostName(self):
        """
        get the host field of this HostModel.
        :return:
        """
        return self.__hostname

    def getDetectFlag(self):
        """
        If this HostModel's study process is over and it is ready to detect,
        this function return 'Study ready', otherwise it return 'Study...'.
        :return: str
        """
        return self.__detect_flag

    def getRecords(self):
        return self.__records

    def __str__(self):
        """
        :return:s
        """
        return "model's url-amount is:\t%d" % self.__url_amount

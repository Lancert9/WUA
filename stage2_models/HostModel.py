"""
    Class HostModel:
        The model of a specific host.
        It contains the host's RecordBox and all features.
"""
from RecordBox import RecordBox
import ModelFeature as MF

__author__ = 'j-lijiawei'


class HostModel:
    def __init__(self, host_name=''):
        """
        :param host_name: str -> the host of this HostModel.

        """
        self.__hostname = host_name     # The host of this host model.
        self.__record_box = RecordBox()    # Contain model's training record.
        self.__pattern_controller = PatternController()     # Determine when to calculate the whole model.

    def addUrl(self, a_record):
        """
        :param a_record: UrlRecord
        """


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

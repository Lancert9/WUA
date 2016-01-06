"""
    Class HostModel:
        The model of a specific host.
        It contains the host's RecordBox and all features.
"""
from RecordBox import RecordBox
from ModelFeature import ModelFeature

__author__ = 'j-lijiawei'


class HostModel:
    def __init__(self, host=''):
        """
        :param host: str -> the host of this HostModel.

        """
        self.__host = host
        self.__record_box = RecordBox()
        self.__feature_model = ModelFeature()
        self.__model_feature_all = {}   # The Host Model's feature.

    def add_record(self, a_record):
        """
        :param a_record: UrlRecord -> the record to be added.
        """
        self.__record_box.add_record(a_record)

    def generate_feature(self):
        self.__record_box.active()
        self.__feature_model.add_train_records(self.__record_box)
        self.__feature_model.generate_all_features()

    def get_host(self):
        """
        get the host name of this HostModel.
        :return: str -> host name.
        """
        return self.__host

    def get_model_feature(self):
        return self.__model_feature_all.get_all_features()

    def __str__(self):
        information = "Host Model:\n" \
                      "\tHost: %s\n" \
                      "\tRecord number: %s\n" \
                      "\tSip number: %s" \
                      % (self.__host, self.__record_box.get_record_num(), self.__record_box.get_sip_num())
        return information

"""
    Class HostModel:
        The model of a specific host.
        It contains the host's RecordBox and all features.
"""
from RecordBox import RecordBox
from FeatureModel import FeatureModel

__author__ = 'j-lijiawei'


class HostModel:
    def __init__(self, host=''):
        """
        :param host: str -> the host of this HostModel.

        """
        self.__host = host
        self.__record_box = RecordBox()
        self.__feature_model = FeatureModel()

        # It map the private attribute string to it's value
        self.__attribute_map = {}

    def add_record(self, a_record):
        """
        :param a_record: UrlRecord -> the record to be added.
        """
        self.__record_box.add_record(a_record)

    def generate_feature(self):
        self.__record_box.active()
        self.__feature_model.generate_all_features(self.__record_box)

    def __generate_attribute_map(self):
        self.__attribute_map['host'] = self.__host
        self.__attribute_map['record_num'] = self.__record_box["record_num"]
        self.__attribute_map['sip_num'] = self.__record_box['sip_num']
        self.__attribute_map['model_feature'] = self.__feature_model

    def __str__(self):
        information = "Host Model:\n" \
                      "\tHost: %s\n" \
                      "\tRecord number: %s\n" \
                      "\tSip number: %s" \
                      % (self.__host, self.__record_box['record_num'], self.__record_box['sip_num'])
        return information

    def __setitem__(self, key, value):
        raise LookupError("It is not allow to set the attribute.")

    def __getitem__(self, item):
        self.__generate_attribute_map()
        return self.__attribute_map[item]

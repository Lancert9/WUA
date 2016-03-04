"""
    Class HostModel:
        The model of a specific host.
        It contains the host's RecordBox and all features.
"""
from RecordBox import RecordBox
from HostFeature import HostFeature

__author__ = 'j-lijiawei'


class HostModel:
    def __init__(self, host=''):
        """
        :param host: str -> the host of this HostModel.

        """
        # It map the private attribute string to it's value
        self._m = dict()

        self._m['host'] = host
        self._m['record_box'] = RecordBox()
        self._m['host_feature'] = HostFeature()

    def add_record(self, a_record):
        """
        :param a_record: UrlRecord -> the record to be added.
        """
        self._m['record_box'].add_record(a_record)

    def generate_feature(self):
        self._m['record_box'].active()
        self._m['host_feature'].generate_all_features(self._m['record_box'])

    def __str__(self):
        information = "Host Model:\n" \
                      "\tHost: %s\n" \
                      "\tRecord number: %s\n" \
                      "\tSip number: %s" \
                      % (self._m['host'], self._m['record_box']['record_num'], self._m['record_box']['sip_num'])
        return information

    def __setitem__(self, key, value):
        raise LookupError("It is not allow to set the attribute.")

    def __getitem__(self, key):
        if key == 'record_num':
            return self._m['record_box']["record_num"]
        elif key == 'sip_num':
            return self._m['record_box']['sip_num']
        return self._m[key]

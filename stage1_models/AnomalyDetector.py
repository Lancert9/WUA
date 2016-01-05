"""
    Class AnomalyDetector:
        Depending on a HostModel, AnomalyDetector detects a UrlRecord to an anomaly or not.
"""
from HostModel import HostModel
# import datetime

__author__ = 'j-lijiawei'


class AnomalyDetector:
    def __init__(self):
        self.__host_model = HostModel()

    def detect(self, a_record, a_host_model):
        """
        :param a_record: UrlRecord
        :param a_host_model: HostModel
        :return: dict --> {'Result': boolean, 'Reason': str}
        """
        a_threshold = 0.001
        self.__host_model = a_host_model
        a_path2prop = self.__host_model.calSinglePathProp_modi(a_record)
        a_para_prop_result = self.__host_model.detectSingleParaProp(a_record, a_threshold)
        # If it path or parameter probability is lower than threshold, it is detected to be anomaly
        a_anomaly_status = self.__isAnomaly(a_threshold, a_path2prop, a_para_prop_result)
        return a_anomaly_status

    def __isAnomaly(self, threshold, path2prop, para_prop_result):
        """
        anomaly_status['Result'] = True or False : means record is detected to be anomaly or not
        anomaly_status['Reason'] : the detail information to show the reason of their detection result
        :param threshold: str
        :param path2prop: dict --> {str: float} -- the encoded url path map to it's probability
        :param para_prop_result: dict --> {str: str} --
                                When key is 'Missing' or 'Normal', it means parameter part of record is normal.
                                Otherwise, when key is 'Anomaly', it means parameter part of record is anomaly,
                                and the key 'Anomaly' map to detail reason.
        :return: dict --> {'Result': boolean, 'Reason': str}
        """
        anomaly_status = {}
        path_threshold = self.__host_model.getModelPathT(threshold)
        path = path2prop.keys()[0]
        path_prop = path2prop.values()[0]
        if path_prop < path_threshold:
            anomaly_status['Result'] = True
            anomaly_status['Reason'] = 'Path: %s probability is too small.' % path
        else:
            para_result = para_prop_result.keys()
            if para_result == ['Missing'] or para_result == ['Normal']:
                anomaly_status['Result'] = False
            elif para_result == ['Anomaly']:
                anomaly_status['Result'] = True
                anomaly_status['Reason'] = para_prop_result['Anomaly']
            else:
                print para_prop_result.keys()
                raise ValueError
        return anomaly_status

    def detectpath(self, a_record, a_host_model, flag):
        """
        :param a_record: UrlRecord
        :param a_host_model: HostModel
        :param flag: 'old' or 'new'
        :return: dict --> {'Result': boolean, 'path_para': float}
        """
        threshold = 0.001
        self.__host_model = a_host_model
        if flag == 'old':
            path2prop = self.__host_model.calSinglePathProp(a_record)
        elif flag == 'new':
            path2prop = self.__host_model.calSinglePathProp_modi(a_record)
        else:
            raise ValueError
        path_threshold = self.__host_model.getModelPathT(threshold)

        path = path2prop.keys()[0]
        path_prop = path2prop.values()[0]
        anomaly_status = {}
        anomaly_status['path_para'] = path_prop
        if path_prop < path_threshold:
            anomaly_status['Result'] = True
        else:
            anomaly_status['Result'] = False
        return anomaly_status


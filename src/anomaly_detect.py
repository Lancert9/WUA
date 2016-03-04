from __future__ import division
import sys
import cPickle
import numpy as np
import datetime
from sklearn.tree import DecisionTreeClassifier
from FlowRecord import FlowRecord
import RecordFeatureFunc as rfF
import FillDefault
from pprint import pprint


__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


def cal_feature(record, host_collector):
    current_record = FlowRecord(record)
    current_model = host_collector.get_host_model(current_record['host'])
    rfF.calculate(current_record, current_model)
    flow_feature = [
                    current_record['path_prop'],
                    current_record['specialSymbol_prop'],
                    current_record['enumeration'],
                    current_record['variable_composition'],
                    current_record['variable_order'],
                    current_record['value_length_prop'],
                    current_record['value_distribution1'],
                    current_record['value_distribution2']
    ]
    flow_feature = [str(feature) for feature in flow_feature]

    return flow_feature


def classify(train_feature, train_label, predict_feature):
    clf = DecisionTreeClassifier()
    clf.fit(train_feature, train_label)
    return clf.predict(predict_feature)


def detect(train_feature_list_filled, train_label_list, predict_feature_list_filled):
    train_feature = np.array(train_feature_list_filled, dtype=np.float32)
    train_label = np.array(train_label_list, dtype=np.int)
    predict_feature = np.array(predict_feature_list_filled, dtype=np.float32)

    predict_label = classify(train_feature, train_label, predict_feature)
    return predict_label


def write_anomaly_result(anomaly_record_address, predict_record_dict, predict_feature_list, predict_label):
    with open(anomaly_record_address, 'wb') as outfile:
        for index, label in enumerate(predict_label):
            if label == -1:
                the_record = predict_record_dict[index]
                the_feature = predict_feature_list[index]
                outfile.write("%s\n" % '\t'.join(the_record))
                outfile.write("\t%s\n" % the_feature)


def main(train_normal_flow_address, train_anomaly_flow_address, predict_flow_address, host_model_address,
         anomaly_record_address):
    with open(host_model_address, 'rb') as host_collector_file:
        host_collector = cPickle.load(host_collector_file)
    print "Finished: Import HostModel"

    train_feature_list = []

    record_num = 0
    with open(train_normal_flow_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                record_num += 1

                the_flow_feature = cal_feature(record, host_collector)
                train_feature_list.append(the_flow_feature)
                # if record_num % 10000 == 0:
                #     print "Finished: Calculate Train Record ==> %d" % record_num
    normal_record_num = record_num
    print "#" * 20
    print "Normal Record: %d" % normal_record_num
    print "#" * 20

    with open(train_anomaly_flow_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                record_num += 1

                the_flow_feature = cal_feature(record, host_collector)
                train_feature_list.append(the_flow_feature)
                # if record_num % 10000 == 0:
                #     print "Finished: Calculate Train Record ==> %d" % record_num
    anomaly_record_num = record_num - normal_record_num
    print "#" * 20
    print "Anomaly Record: %d" % anomaly_record_num
    print "#" * 20

    train_label_list = [1] * normal_record_num + [-1] * anomaly_record_num
    print "Finished: Calculate Train Data Feature"

    predict_record_id = 0
    predict_record_dict = {}
    predict_feature_list = []
    with open(predict_flow_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                predict_record_dict[predict_record_id] = record
                predict_record_id += 1

                the_flow_feature = cal_feature(record, host_collector)
                predict_feature_list.append(the_flow_feature)

                # if predict_record_id % 10000 == 0:
                #     print "Finished: Calculate Predict Record ==> %d" % predict_record_id
    print "Finished: Calculate Predict Data Feature"

    default_value_dict = FillDefault.cal_default(train_feature_list)

    train_feature_list_filled = FillDefault.fill(train_feature_list, default_value_dict)
    predict_feature_list_filled = FillDefault.fill(predict_feature_list, default_value_dict)
    print "Finished: Fill Default Feature"

    predict_label = detect(train_feature_list_filled, train_label_list, predict_feature_list_filled)
    print "Finished: Detect"

    write_anomaly_result(anomaly_record_address, predict_record_dict, predict_feature_list, predict_label)
    print "Finished: Write Result"

if __name__ == '__main__':
    a_train_normal_flow_address = sys.argv[1]
    a_train_anomaly_flow_address = sys.argv[2]
    a_predict_flow_address = sys.argv[3]
    a_host_model_address = sys.argv[4]
    a_anomaly_record_address = sys.argv[5]

    # a_train_normal_flow_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_anomaly_detect\\train_normal'
    # a_train_anomaly_flow_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_anomaly_detect\\train_anomaly'
    # a_predict_flow_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_anomaly_detect\\predict_flow'
    # a_host_model_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_anomaly_detect\\host_model.pickle'
    # a_anomaly_record_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_anomaly_detect\\anomaly_result'

    main(a_train_normal_flow_address, a_train_anomaly_flow_address, a_predict_flow_address, a_host_model_address,
         a_anomaly_record_address)

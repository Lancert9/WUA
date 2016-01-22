from __future__ import division
import numpy as np
from sklearn.linear_model import SGDClassifier
import json

__author__ = 'j-lijiawei'

module_list = [
                'path probability',
                'special symbol probability',
                'enumeration',
                'variable composition',
                'variable order',
                'value length probability',
                'value distribution 1',
                'value distribution 2'
]


def get_data(feature_address, label_address):
    feature_list = list()
    label_list = list()
    with open(feature_address, 'rb') as infile:
        for line in infile:
            feature = line.strip(' \n').split('\t')
            feature_list.append(feature)
    with open(label_address, 'rb') as infile:
        for line in infile:
            label = line.strip(' \n')
            label_list.append(label)
    return np.array(feature_list, dtype=np.float32), np.array(label_list, dtype=np.int)


def classify(train_feature, train_label, test_feature):
    clf = SGDClassifier()
    clf.fit(train_feature, train_label)
    return clf.predict(test_feature)


def metrics(test_label, predict_label):
    record_num = 0
    normal_right = 0
    normal_wrong = 0
    anomaly_right = 0
    anomaly_wrong = 0
    for t_p in zip(test_label, predict_label):
        record_num += 1
        if t_p == (1, 1):
            normal_right += 1
        elif t_p == (1, -1):
            anomaly_wrong += 1
        elif t_p == (-1, -1):
            anomaly_right += 1
        else:
            normal_wrong += 1

    predict_anomaly_number = anomaly_right + anomaly_wrong
    test_anomaly_number = normal_wrong + anomaly_right

    print "Predict Anomaly Number: %d" % predict_anomaly_number

    print "Precision rate: %f" % (anomaly_right / predict_anomaly_number)
    print "Recall rate: %f" % (anomaly_right / test_anomaly_number)

    print "\n"


def save_error_record(test_label, predict_label, save_address):
    error_record_dict = {'FP': [], 'FN': []}
    for index, t_p in enumerate(zip(test_label, predict_label)):
        if t_p == (1, -1):
            error_record_dict['FP'].append(index + 1)
        if t_p == (-1, 1):
            error_record_dict['FN'].append(index + 1)
    print "FP Numbers: %s" % len(error_record_dict['FP'])
    print "FN Numbers: %s" % len(error_record_dict['FN'])
    with open(save_address, 'wb') as outfile:
        json.dump(error_record_dict, outfile, ensure_ascii=False, indent=4, separators=(',', ':'))


def whole_module(train_feature_address, train_label_address,
                 test_feature_address, test_label_address,
                 error_record_address):
    a_train_feature, a_train_label = get_data(train_feature_address, train_label_address)
    a_test_feature, a_test_label = get_data(test_feature_address, test_label_address)

    a_predict_label = classify(a_train_feature, a_train_label, a_test_feature)
    print 'Module Classified Finished.'

    metrics(a_test_label, a_predict_label)
    # save_error_record(a_test_label, a_predict_label, error_record_address)


def single_module(single_train_feature_base_address, train_label_address,
                  single_test_feature_base_address, test_label_address):
    for i in range(8):
        train_feature_address = single_train_feature_base_address + '_' + str(i)
        a_train_feature, a_train_label = get_data(train_feature_address, train_label_address)

        test_feature_address = single_test_feature_base_address + '_' + str(i)
        a_test_feature, a_test_label = get_data(test_feature_address, test_label_address)

        a_predict_label = classify(a_train_feature, a_train_label, a_test_feature)

        print 'Module-%s:' % module_list[i]
        metrics(a_test_label, a_predict_label)


if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\xiaoshuo.360.cn_try_1\\'
    single_module_base_address = 'E:\\WUA_data_container\\data_container\\Detect\\' \
                                 'xiaoshuo.360.cn_try_1\\single module\\'

    a_train_feature_address = base_address + 'train_feature_filled'
    a_train_label_address = base_address + 'train_label'
    a_test_feature_address = base_address + 'test_feature_filled'
    a_test_label_address = base_address + 'test_label'

    a_error_record_address = base_address + 'error_record.json'

    a_single_train_feature_base_address = single_module_base_address + 'train\\'
    a_single_test_feature_base_address = single_module_base_address + 'test\\'

    print "WHOLE MODULE: "
    whole_module(a_train_feature_address, a_train_label_address,
                 a_test_feature_address, a_test_label_address,
                 a_error_record_address)

    print "SINGLE MODULE: "
    single_module(a_single_train_feature_base_address, a_train_label_address,
                  a_single_test_feature_base_address, a_test_label_address)

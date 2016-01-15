from __future__ import division
import numpy as np
from sklearn import tree

__author__ = 'j-lijiawei'


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
    return np.array(feature_list), np.array(label_list)


def classify(train_feature, train_label, test_feature):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_feature, train_label)
    return clf.predict(test_feature)


def metrics(test_label, predict_label):
    record_num = 0
    normal_right = 0
    normal_wrong = 0
    anomaly_right = 0
    anomaly_wrong = 0
    for t_p in zip(test_label, predict_label):
        record_num += 1
        if t_p == ('1', '1'):
            normal_right += 1
        elif t_p == ('1', '-1'):
            normal_wrong += 1
        elif t_p == ('-1', '-1'):
            anomaly_right += 1
        else:
            anomaly_wrong += 1

    anomaly_record = anomaly_right + anomaly_wrong
    normal_record = normal_right + normal_wrong
    print "Normal Number: %d" % normal_record
    print "Anomaly Number: %d" % anomaly_record

    print "Anomaly Right: %s" % anomaly_right
    print "Anomaly Wrong: %s" % anomaly_wrong

    print "TP: %f" % (anomaly_right / anomaly_record)


def whole_module(train_feature_address, train_label_address, test_feature_address, test_label_address):
    a_train_feature, a_train_label = get_data(train_feature_address, train_label_address)
    print 'Load Train Data finished.'
    a_test_feature, a_test_label = get_data(test_feature_address, test_label_address)
    print 'Load Test Data Finished.'

    a_predict_label = classify(a_train_feature, a_train_label, a_test_feature)
    print 'Module Classified Finished.'

    classify(a_test_label, a_predict_label)

def single_module()

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\mall.360.com_20151231_31\\'
    a_train_feature_address = base_address + 'train_feature_filled'
    a_train_label_address = base_address + 'train_label'
    a_test_feature_address = base_address + 'test_feature_filled'
    a_test_label_address = base_address + 'test_label'

    whole_module(a_train_feature_address, a_train_label_address, a_test_feature_address, a_test_label_address)

    single_module(a_train_feature_address, a_train_label_address, a_test_feature_address, a_test_label_address)




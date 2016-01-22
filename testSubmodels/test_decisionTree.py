import numpy as np
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot


def decision_draw(train_data_address, train_label_address, test_data_address, test_label_address):
    train_data_list = list()
    train_label_list = list()

    with open(train_data_address, 'rb') as infile:
        for line in infile:
            record = line.strip('\n')
            train_data_list.append([record])
    with open(train_label_address, 'rb') as infile:
        for line in infile:
            record = line.strip('\n')
            train_label_list.append(record)

    train_data_array = np.array(train_data_list)
    train_label_array = np.array(train_label_list)

    clf = tree.DecisionTreeClassifier(max_depth=5)
    clf = clf.fit(train_data_array, train_label_array)



if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\mall.360.com_20151231_31'
    a_train_data_address = base_address + '\\single module\\train\\_0'
    a_train_label_address = base_address + '\\train_label'
    a_test_data_address = base_address + '\\single module\\test\\_0'
    a_test_label_address = base_address + '\\test_label'

    decision_draw(a_train_data_address, a_train_label_address, a_test_data_address, a_test_label_address)
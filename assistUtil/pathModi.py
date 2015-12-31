import pickle
import imp
import sys
import math
import matplotlib.pyplot as plt
__author__ = 'j-lijiawei'

sys.path.append('E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\models')
HostCollector = imp.load_source('HostCollector', 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\models\\HostCollector.py')


def collectPath():
    infile_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\CompleteModel\\HuaJiao_30_host_collector.pickle"
    with open(infile_address, 'rb') as infile:
        a_host_collector = pickle.load(infile)
        a_model = a_host_collector.getHostModel('live.huajiao.com')
        records_list = a_model.getModelPathProps()
        threshold_dict = a_model.getModePathPropsThreshold()
    smallest = min(records_list)
    largest = max(records_list)
    threshold = threshold_dict.values()[0]

    print "Smallest: %f" % smallest
    print "Biggest: %f" % largest
    print "Threshold: %f" % threshold
    fig = plt.figure()
    ax_1 = fig.add_subplot(1, 1, 1)
    ax_1.hist(records_list, bins=100)
    ax_1.axvline(x=threshold, ymin=0, ymax=1, color='r', label='Threshold')
    ax_1.set_title('Path Probability Score Statistics')
    ax_1.set_xlabel('score')
    ax_1.set_ylabel('amount')
    ax_1.legend(loc='best')
    plt.show()


def detectPath():
    infile_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Path_Modi\\modi_path_dict.pickle"
    with open(infile_address, 'rb') as infile:
        path_para_list = pickle.load(infile)
    smallest = min(path_para_list)
    largest = max(path_para_list)
    x_min = math.ceil(smallest)
    x_max = math.ceil(largest)
    threshold = -4.809310
    print "Smallest: %f" % smallest
    print "Biggest: %f" % largest
    print "Threshold: %f" % threshold
    fig = plt.figure()
    ax_1 = fig.add_subplot(1, 1, 1)
    ax_1.hist(path_para_list, bins=100, range=(x_min, x_max))
    ax_1.axvline(x=threshold, ymin=0, ymax=1, color='r', label='Threshold')
    ax_1.set_title('Path Probability Score Statistics')
    ax_1.set_xlabel('score')
    ax_1.set_ylabel('amount')
    ax_1.legend(loc='best')
    plt.show()

if __name__ == "__main__":
    # collectPath()
    detectPath()
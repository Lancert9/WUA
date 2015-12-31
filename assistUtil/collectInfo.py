__author__ = 'j-lijiawei'
import pickle
import sys
sys.path.append('E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\models')
from HostCollector import HostCollector
# from HostModel import HostModel


def collectPath():
    infile_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\CompleteModel\\HuaJiao_30_host_collector.pickle"
    outfile_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Path_collector"

    with open(infile_address, 'rb') as infile:
        a_host_collector = pickle.load(infile)
        a_model = a_host_collector.getHostModel('live.huajiao.com')
        records_list = a_model.getRecords()

    with open(outfile_address, 'wb') as outfile:
        for record, count in records_list.items():
            path_code = record.getPathCode()
            path_code = ' '.join(path_code.split('/'))
            # for i in range(count):
            #     outfile.write('%s\n' % path_code)
            outfile.write('%s\n' % path_code)

    print 'Path Collect system finished.'


def collectUrl():
    infile_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\CompleteModel\\HuaJiao_30_host_collector.pickle"
    outfile_address = "E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Url_collector"

    with open(infile_address, 'rb') as infile:
        a_host_collector = pickle.load(infile)
        a_model = a_host_collector.getHostModel('live.huajiao.com')
        records_list = a_model.getRecords()

    with open(outfile_address, 'wb') as outfile:
        for record, count in records_list.items():
            path_code = record.getPathCode()
            para_code = record.getParaCode()
            for i in range(count):
                outfile.write('%s%s\n' % (path_code, para_code))

    print 'Url Collect system finished.'

if __name__ == '__main__':
    # collectPath()
    collectUrl()


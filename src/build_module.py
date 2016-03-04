"""
    It is the main function to learn the HostModel.
"""

import sys
from FlowRecord import FlowRecord
from HostCollector import HostCollector
import datetime
import cPickle as cpickle

__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


def model_learn(flow_address, host_stored_address):
    host_collector = HostCollector()

    start_time = datetime.datetime.now()
    record_num = 0
    with open(flow_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                current_record = FlowRecord(record)
                current_model = host_collector.get_host_model(current_record['host'])
                current_model.add_record(current_record)
                record_num += 1
                if record_num % 10000 == 0:
                    print 'Record completed: %s' % record_num
    print 'Study Records: %d' % record_num
    print 'Study Host Models: %d' % len(host_collector)
    for host_model in host_collector:
        host_model.generate_feature()
    end_time = datetime.datetime.now()
    print 'Model Learn Consuming: %s' % (end_time - start_time)

    for host_model in host_collector:
        print host_model

    with open(host_stored_address, 'wb') as store_host_collector:
        cpickle.dump(host_collector, store_host_collector)

    print 'LEARN Module Finished.'

if __name__ == '__main__':
    a_flow_address = sys.argv[1]
    a_host_stored_address = sys.argv[2]

    # a_flow_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_build_module\\normal'
    # a_host_stored_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_build_module\\host_model.pickle'

    model_learn(a_flow_address, a_host_stored_address)

"""
    It is the main function to calculate the record feature.
"""
from FlowRecord import FlowRecord
import RecordFeatureFunc as rfF
import datetime
import pickle

__author__ = 'Lancer'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

flow_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\' \
               'flow_mall.360.com_20151231_31\\Demo\\test_flow_20s'
host_stored_address = 'E:\\WUA_data_container\\data_container\\Complete_Model\\' \
                      'flow_mall.360.com_20151231_31\\Demo\\Host_Collector.pickle'
flow_feature_stored_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\' \
                              'flow_mall.360.com_20151231_31\\Demo\\flow_feature_20'


def record_detect():
    with open(host_stored_address, 'rb') as host_collector_file:
        host_collector = pickle.load(host_collector_file)

    flow_feature_list = []
    start_time = datetime.datetime.now()
    record_num = 0
    with open(flow_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                current_record = FlowRecord(record)
                current_model = host_collector.get_host_model(current_record['host'])
                rfF.calculate(current_record, current_model)
                flow_feature_list.append(current_record)
                record_num += 1
                if record_num % 10000 == 0:
                    print 'Record completed: %s' % record_num
    end_time = datetime.datetime.now()
    print 'Calculate Records: %s' % record_num
    print 'Record Calculated Consuming: %s' % (end_time - start_time)

    flow_feature_dict = dict()
    for flow in flow_feature_list:
        feature = [flow['path_prop'],
                   flow['specialSymbol_prop'],
                   flow['enumeration'],
                   flow['variable_composition'],
                   flow['variable_order'],
                   flow['value_length_prop'],
                   flow['value_distribution1'],
                   flow['value_distribution2']]
        flow_feature_dict[flow['content']] = feature
    with open(flow_feature_stored_address, 'wb') as outfile:
        pickle.dump(flow_feature_dict, outfile)
    print 'Calculate Record Feature Module Finished.'

if __name__ == '__main__':
    record_detect()

"""
    It is the main function to calculate the record feature.
"""
from FlowRecord import FlowRecord
import RecordFeatureFunc as rfF
import datetime
import cPickle as cpickle

__author__ = 'Lancer'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


def main(normal_flow_address, anomaly_flow_address, host_stored_address, flow_feature_stored_address):
    normal_flow_feature_list = record_detect(normal_flow_address, host_stored_address)
    anomaly_flow_feature_list = record_detect(anomaly_flow_address, host_stored_address)

    with open(flow_feature_stored_address, 'wb') as outfile:
        normal_num = 0
        for item in normal_flow_feature_list:
            item.append(1)
            flow_feature = [str(feature) for feature in item]
            flow_feature = '\t'.join(flow_feature)
            outfile.write('%s\n' % flow_feature)
            normal_num += 1
        print 'Write Normal Feature numbers: %d' % normal_num

        anomaly_num = 0
        for item in anomaly_flow_feature_list:
            item.append(-1)
            flow_feature = [str(feature) for feature in item]
            flow_feature = '\t'.join(flow_feature)
            outfile.write('%s\n' % flow_feature)
            anomaly_num += 1
        print 'Write Anomaly Feature numbers: %d' % anomaly_num


def record_detect(flow_address, host_stored_address):
    with open(host_stored_address, 'rb') as host_collector_file:
        host_collector = cpickle.load(host_collector_file)

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
                flow_feature_list.append(flow_feature)
                record_num += 1
                if record_num % 10000 == 0:
                    print 'Record completed: %s' % record_num
    end_time = datetime.datetime.now()
    print 'Calculate Records: %s' % record_num
    print 'Record Calculated Consuming: %s' % (end_time - start_time)
    return flow_feature_list

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\'
    a_host_stored_address = base_address + 'Complete_Model\\xiaoshuo.360.cn_try_1\\Host_Collector.pickle'
    a_flow_feature_stored_address = base_address + 'Detect\\xiaoshuo.360.cn_try_1\\test_feature_label'

    a_normal_flow_address = base_address + 'Skyeye_Sensor\\Flow_Filter_Attack\\' \
                                           'xiaoshuo.360.cn_20160116_32_split\\test_normal'
    a_anomaly_flow_address = base_address + 'Skyeye_Sensor\\Flow_Filter_Attack\\' \
                                            'xiaoshuo.360.cn_20160116_32_split\\test_anomaly'

    main(a_normal_flow_address, a_anomaly_flow_address, a_host_stored_address, a_flow_feature_stored_address)
    print 'Calculate Record Feature Module Finished.'

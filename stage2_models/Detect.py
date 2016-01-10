"""
    It is the main function to detect the record.
"""
from stage2_models.FlowRecord import FlowRecord
from stage2_models.AnomalyDetector import AnomalyDetector
from stage2_models.AnomalyWriter import AnomalyWriter
import datetime
import pickle

__author__ = 'Lancer'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

flow_address = ''
normal_record_address = ''
anomaly_record_address = ''
host_stored_address = ''


def record_detect():
    with open(host_stored_address, 'rb') as store_host_collector:
        host_collector = pickle.load(store_host_collector)

    start_time = datetime.datetime.now()
    record_num = 0
    with open(flow_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                current_record = FlowRecord(record)
                current_model = host_collector.get_host_model(current_record['host'])
                detect_result = AnomalyDetector.detect(current_record, current_model)
                if detect_result is True:
                    AnomalyWriter.write(current_record, anomaly_record_address)
                else:
                    AnomalyWriter.write(current_record, normal_record_address)
            record_num += 1
            if record_num % 1000 == 0:
                print 'Record completed: %s' % record_num
    end_time = datetime.datetime.now()

    print 'Record Detect Consuming: %s' % (end_time - start_time)
    print 'Detect Records: %s' % record_num
    print 'Whole Module Finished.'

if __name__ == '__main__':
    record_detect()

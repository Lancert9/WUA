"""
    Main function.
    It contains the system of  module study and anomaly detection.
"""
from UrlRecord import UrlRecord
from HostCollector import HostCollector
from AnomalyDetector import AnomalyDetector
from AnomalyWriter import AnomalyWriter
import datetime
import pickle

__author__ = 'j-lijiawei'
(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

url_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Input_Flow\\filtered_flow_20151112_31'
base_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container'
whole_result_address = base_address + '\\Output_Result\\result_filtered_flow_20151112_30_HuaJiao'
host_collector_address = base_address + '\\CompleteModel\\complete_model_filtered_flow_20151112_30_HuaJiao.pickle'


def main():
    host_collector = HostCollector()
    anomaly_detector = AnomalyDetector()
    anomaly_writer = AnomalyWriter(whole_result_address)

    try:
        # save the begin time
        begin_time = datetime.datetime.now()
        detect_time_flag = True
        global study_ready_time
        global detect_ready_time

        with open(url_address, 'rb') as infile:
            record_num = 0
            study_record_num = 0
            for line in infile:
                record = line.strip(' \n').split('\t')
                if len(record) == 13 and record[_host] != '':
                    a_url = UrlRecord(record)
                    current_model = host_collector.get_host_model(a_url.get_host())
                    if detect_time_flag:
                        detect_time_flag = False
                        study_ready_time = datetime.datetime.now()
                        study_interval = study_ready_time - begin_time
                        study_record_num = record_num
                        print 'Study consuming: %s' % study_interval
                        print 'Study Record: %s' % study_record_num
                        print '\tUrl amount: %s\tDifferent url amount: %s\tDifferent sip: %s\t' % \
                            (current_model.getUrlAmount(), current_model.getDifUrlAmount(),
                             current_model.getSipAmount())
                    # Detect whether the record is anomaly
                    anomaly_status = anomaly_detector.detect(a_url, current_model)
                    # If the record is detected to be anomaly
                    if anomaly_status['Result'] is True:
                        anomaly_writer.writeResult(a_url, anomaly_status)
                record_num += 1
                if record_num % 10000 == 0:
                    print 'Record completed: ', record_num,
            else:
                detect_record_num = record_num - study_record_num
                end_time = datetime.datetime.now()
                detect_ready_time = end_time - study_ready_time
                print 'Detect Record: %s' % detect_record_num
                print "Detection consuming: %s" % detect_ready_time
                print 'Whole system test finished.'

        # Store the completed Host Model.
        with open(host_collector_address, 'wb') as save_host_collector:
            pickle.dump(host_collector, save_host_collector)

    except IndexError:
        print 'Lancer says:\n\tIt has error through the system.'
        raise

if __name__ == '__main__':
    main()

"""
    It only contains the system of anomaly detection.
    The detected module loads from pickle file.
"""
from UrlRecord import UrlRecord
from AnomalyDetector import AnomalyDetector
from AnomalyWriter import AnomalyWriter
import datetime
import pickle

__author__ = 'j-lijiawei'
(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

base_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container'
url_address = base_address + '\\Input_Flow\\HuaJiao_wvs_1113'


def originalPath():
    host_collector_address = base_address + '\\CompleteModel\\complete_host_collector.pickle'
    whole_result_address = base_address + '\\Path_Modi\\result_huajiao_wvs_1113_modipath_original'
    path_para_dic_address = base_address + '\\Path_Modi\\original_path_dict.pickle'
    path_collector = []

    with open(host_collector_address, 'rb') as read_host_collector:
        host_collector = pickle.load(read_host_collector)
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
            for line in infile:
                line = line.strip(' \n')
                record = line.split('\t')
                if len(record) == 13 and record[_host] != '':
                    a_record = UrlRecord(record)
                    current_model = host_collector.getHostModel(a_record.get_host())
                    pattern_flag = current_model.getDetectFlag()
                    if pattern_flag == 'Study ready':
                        if detect_time_flag:
                            detect_time_flag = False
                            study_ready_time = datetime.datetime.now()
                            study_interval = study_ready_time - begin_time
                            print 'Study consuming: %s' % study_interval
                        anomaly_status = anomaly_detector.detectpath(a_record, current_model, 'old')
                        path_collector.append(anomaly_status['path_para'])
                        if anomaly_status['Result'] is True:
                                anomaly_writer.writePathResult(a_record, anomaly_status)
                record_num += 1
                if record_num % 1000 == 0:
                    print 'Record completed: ', record_num,
                    print '\tUrl amount: %s\tDifferent url amount: %s\tDifferent sip: %s\t' % (current_model.getUrlAmount(), current_model.getDifUrlAmount(), current_model.getSipAmount())
    except IndexError:
        print 'Lancer says:\n' \
           '\tIt has error through the system.'
        raise

    with open(path_para_dic_address, 'wb') as save:
        pickle.dump(path_collector, save)

    end_time = datetime.datetime.now()
    detect_ready_time = end_time - study_ready_time
    print "Detection consuming: %s" % detect_ready_time
    print 'Whole system test finished.'


def modiPath():
    host_collector_address = base_address + '\\CompleteModel\\HuaJiao_30_host_collector_modipath.pickle'
    whole_result_address = base_address + '\\Path_Modi\\result_huajiao_wvs_1113_modipath_modi'
    path_para_dic_address = base_address + '\\Path_Modi\\modi_path_dict.pickle'
    path_collector = []

    with open(host_collector_address, 'rb') as read_host_collector:
        host_collector = pickle.load(read_host_collector)
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
            for line in infile:
                line = line.strip(' \n')
                record = line.split('\t')
                if len(record) == 13 and record[_host] != '':
                    a_record = UrlRecord(record)
                    current_model = host_collector.getHostModel(a_record.get_host())
                    pattern_flag = current_model.getDetectFlag()
                    if pattern_flag == 'Study ready':
                        if detect_time_flag:
                            detect_time_flag = False
                            study_ready_time = datetime.datetime.now()
                            study_interval = study_ready_time - begin_time
                            print 'Study consuming: %s' % study_interval
                        anomaly_status = anomaly_detector.detectpath(a_record, current_model, 'new')
                        path_collector.append(anomaly_status['path_para'])
                        if anomaly_status['Result'] is True:
                                anomaly_writer.writePathResult(a_record, anomaly_status)
                record_num += 1
                if record_num % 1000 == 0:
                    print 'Record completed: ', record_num,
                    print '\tUrl amount: %s\tDifferent url amount: %s\tDifferent sip: %s\t' % (current_model.getUrlAmount(), current_model.getDifUrlAmount(), current_model.getSipAmount())
    except IndexError:
        print 'Lancer says:\n' \
           '\tIt has error through the system.'
        raise

    with open(path_para_dic_address, 'wb') as save:
        pickle.dump(path_collector, save)

    end_time = datetime.datetime.now()
    detect_ready_time = end_time - study_ready_time
    print "Detection consuming: %s" % detect_ready_time
    print 'Whole system test finished.'

if __name__ == '__main__':
    # originalPath()
    modiPath()

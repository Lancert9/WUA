# -*- coding=utf-8 -*-
__author__ = 'j-lijiawei'
import sys

a_time, a_sip, a_sport, a_dip, a_dport, a_hostname, a_content, a_patten, a_type = range(9)
f_time, f_sip, f_sport, f_dip, f_dport, f_method, f_uri, f_host, f_origin, f_cookie, f_uagent, f_refer, f_data \
                                                                              = range(13)
SOH = chr(1)
CONTENT_TYPE = ['url参数值', 'url参数名值', 'url', 'User-Agent', 'Cookie']


def attack_filter(flow_address, attack_address, normal_stored_address, anomaly_stores_address):
    attack_path_set = set()
    attack_value_set = set()
    attack_cookie_set = set()
    attack_ua_set = set()
    with open(attack_address, 'rb') as attack_infile:
        attack_record_num = 0
        for line in attack_infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 9:
                attack_record_num += 1
                record_content = record[a_content]
                record_content_seg = record_content.rstrip(SOH).split(SOH)
                for i in range(0, len(record_content_seg), 2):
                    content_type = record_content_seg[i]
                    the_content = record_content_seg[i + 1]
                    if content_type == 'url参数值':
                        the_content = the_content.rstrip(' HTTP/1.1')
                        attack_value_set.add(the_content)
                    elif content_type == 'url参数名值':
                        the_content = the_content.rstrip(' HTTP/1.1')
                        value_list = []
                        para_seg = the_content.split('&')
                        k = 0
                        while k < len(para_seg) and len(para_seg) > 1:
                            if '=' not in para_seg[k]:
                                if k == 0:
                                    para_seg[k + 1] += para_seg[k]
                                else:
                                    para_seg[k - 1] += para_seg[k]
                                del para_seg[k]
                            else:
                                k += 1
                        for seg in para_seg:
                            if '=' in seg:
                                variable, value = seg.split('=', 1)
                            else:
                                value = seg
                            value_list.append(value)

                        the_value = ' '.join(value_list)
                        attack_value_set.add(the_value)
                    elif content_type == 'url':
                        the_content = the_content.rstrip(' HTTP/1.1')
                        attack_path_set.add(the_content)
                    elif content_type == 'User-Agent':
                        attack_ua_set.add(the_content)
                    elif content_type == 'Cookie':
                        attack_cookie_set.add(the_content)
                    else:
                        raise ValueError
        print 'Complete Attack Records: %s' % attack_record_num

    with open(flow_address, 'rb') as flow_infile, open(normal_stored_address, 'wb') as normal_outfile, \
            open(anomaly_stores_address, 'wb') as anomaly_outfile:
        flow_record_num = 0
        normal_record_num = 0
        for line in flow_infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13:
                flow_record_num += 1
                flow_record_ua = record[f_uagent]
                flow_record_cookie = record[f_cookie]

                attack_ua_set.add('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1;'
                                  ' .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR')
                if flow_record_ua in attack_ua_set or '360SEC webscan' in flow_record_ua:
                    anomaly_outfile.write(line)
                elif flow_record_cookie in attack_cookie_set:
                    anomaly_outfile.write(line)
                else:
                    flow_record_uri = record[f_uri]
                    if '#vul_webscan' in flow_record_uri:
                        anomaly_outfile.write(line)
                    else:
                        if '?' in flow_record_uri:
                            path, para = flow_record_uri.split('?', 1)
                        else:
                            path = flow_record_uri
                            para = ''
                        if path in attack_path_set:
                            anomaly_outfile.write(line)
                        else:
                            para_seg = para.split('&')
                            value_list = list()
                            for seg in para_seg:
                                if '=' in seg:
                                    value = seg.split('=', 1)[1]
                                else:
                                    value = seg
                                value_list.append(value)
                            the_value = ' '.join(value_list)
                            if the_value in attack_value_set:
                                anomaly_outfile.write(line)
                            else:
                                normal_record_num += 1
                                normal_outfile.write(line)

        print 'Complete Flow Records: %s' % flow_record_num
        print 'Normal Flow Records: %s' % normal_record_num
        print 'Anomaly Flow Records: %s' % (flow_record_num - normal_record_num)


if __name__ == '__main__':
    a_flow_address = sys.argv[1]
    a_attack_address = sys.argv[2]
    a_normal_stored_address = sys.argv[3]
    a_anomaly_stored_address = sys.argv[4]

    # a_flow_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_preprocess\\flow_input'
    # a_attack_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_preprocess\\attack_input'
    # a_normal_stored_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_preprocess\\normal'
    # a_anomaly_stored_address = 'E:\\WUA_data_container\\data_container\\To Linux\\test_preprocess\\anomaly'

    attack_filter(a_flow_address, a_attack_address, a_normal_stored_address, a_anomaly_stored_address)

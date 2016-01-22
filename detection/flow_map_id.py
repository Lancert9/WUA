import json

__author__ = 'j-lijiawei'


def id_map(normal_address, anomaly_address, id_flow_address):
    with open(normal_address, 'rb') as normal_infile, open(anomaly_address, 'rb') as anomaly_infile, \
                                                      open(id_flow_address, 'wb') as outfile:
        flow_id = 0
        id_flow_dict = {}
        for line in normal_infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13:
                flow_id += 1
                id_flow_dict[flow_id] = line
        print "Map Normal Records: %s" % flow_id

        for line in anomaly_infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13:
                flow_id += 1
                id_flow_dict[flow_id] = line
        print "Map Total Records: %s" % flow_id

        json.dump(id_flow_dict, outfile, ensure_ascii=False, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\'
    a_normal_address = base_address + 'Skyeye_Sensor\\Flow_Filter_Attack\\' \
                                      'xiaoshuo.360.cn_20160116_32_split\\test_normal'
    a_anomaly_address = base_address + 'Skyeye_Sensor\\Flow_Filter_Attack\\' \
                                       'xiaoshuo.360.cn_20160116_32_split\\test_anomaly'
    a_id_flow_address = base_address + 'Detect\\xiaoshuo.360.cn_try_1\\test_id_flow.json'

    id_map(a_normal_address, a_anomaly_address, a_id_flow_address)

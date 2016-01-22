import json

__author__ = 'j-lijiawei'


def id_map(feature_address, id_flow_address):
    with open(feature_address, 'rb') as infile, open(id_flow_address, 'wb') as outfile:
        flow_id = 0
        id_flow_dict = {}
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 9:
                flow_id += 1
                id_flow_dict[flow_id] = line
        print "Map Feature Records: %s" % flow_id

        json.dump(id_flow_dict, outfile, ensure_ascii=False, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\'
    a_feature_address = base_address + 'Detect\\xiaoshuo.360.cn_try_1\\test_feature_label'
    a_id_flow_address = base_address + 'Detect\\xiaoshuo.360.cn_try_1\\test_id_feature.json'

    id_map(a_feature_address, a_id_flow_address)

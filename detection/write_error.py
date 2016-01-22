__author__ = 'j-lijiawei'
import json


def write(id_flow_address, id_feature_address, error_record_address, fp_record_address, fn_record_address):
    with open(id_flow_address, 'rb') as infile_id_flow, \
            open(id_feature_address, 'rb') as infile_id_feature, \
            open(error_record_address, 'rb') as infile_error_record:
        id_flow_dict = json.load(infile_id_flow, encoding='utf-8')
        id_feature_dict = json.load(infile_id_feature)
        error_record_dict = json.load(infile_error_record)

    with open(fp_record_address, 'wb') as outfile_FP, open(fn_record_address, 'wb') as outfile_FN:
        fp_list = error_record_dict['FP']
        for index in fp_list:
            index = str(index)
            flow = id_flow_dict[index].encode('utf-8')
            feature = id_feature_dict[index]
            outfile_FP.write(flow)
            outfile_FP.write('\t%s' % feature)

        fn_list = error_record_dict['FN']
        for index in fn_list:
            index = str(index)
            flow = id_flow_dict[index].encode('utf-8')
            feature = id_feature_dict[index]
            outfile_FN.write(flow)
            outfile_FN.write('\t%s' % feature)

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\'
    a_id_flow_address = base_address + 'xiaoshuo.360.cn_try_1\\test_id_flow.json'
    a_id_feature_address = base_address + 'xiaoshuo.360.cn_try_1\\test_id_feature.json'
    a_error_record_address = base_address + 'xiaoshuo.360.cn_try_1\\error_record.json'
    a_FP_record_address = base_address + 'xiaoshuo.360.cn_try_1\\FP_record'
    a_FN_record_address = base_address + 'xiaoshuo.360.cn_try_1\\FN_record'
    write(a_id_flow_address, a_id_feature_address, a_error_record_address, a_FP_record_address, a_FN_record_address)

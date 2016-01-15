__author__ = 'j-lijiawei'


def split(flow_feature_label_address, flow_feature_address, flow_label_address):
    with open(flow_feature_label_address, 'rb') as infile, open(flow_feature_address, 'wb') as feature_outfile, \
                                                           open(flow_label_address, 'wb') as label_outfile:
        record_num = 0
        for line in infile:
            feature, label = line.strip(' \n').rsplit('\t', 1)
            feature_outfile.write("%s\n" % feature)
            label_outfile.write("%s\n" % label)
            record_num += 1
        print "Split Record %d" % record_num

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\mall.360.com_20151231_31\\'
    a_flow_feature_label_address = base_address + 'test_feature_label'
    a_feature_address = base_address + 'test_feature'
    a_label_address = base_address + 'test_label'
    split(a_flow_feature_label_address, a_feature_address, a_label_address)

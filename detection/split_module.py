__author__ = 'j-lijiawei'


def split(flow_feature_address, single_module_base_address):
    for i in range(8):
        record_num = 0
        single_module_address = single_module_base_address + '_' + str(i)
        with open(flow_feature_address, 'rb') as infile, open(single_module_address, 'wb') as outfile:
            for line in infile:
                feature = line.strip(' \n').split('\t')[i]
                outfile.write("%s\n" % feature)
                record_num += 1
        print "Module %d finished. Split Record %d" % (i, record_num)

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\xiaoshuo.360.cn_try_1\\'
    a_feature_address = base_address + 'test_feature_filled'
    a_single_module_base_address = base_address + '\\single module\\test\\'
    split(a_feature_address, a_single_module_base_address)

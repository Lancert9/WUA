__author__ = 'j-lijiawei'


def random_split(input_address, output_address_1, output_address_2):
    with open(input_address, 'rb') as infile, open(output_address_1, 'wb') as outfile_1, \
                                              open(output_address_2, 'wb') as outfile_2:
        flag = 0
        file_1_num = 0
        file_2_num = 0
        for line in infile:
            if flag % 3 == 0:
                file_1_num += 1
                outfile_1.write(line)
            else:
                file_2_num += 1
                outfile_2.write(line)
            flag += 1

    print "File 1 number: %d" % file_1_num
    print "File 2 number: %d" % file_2_num

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\Flow_Filter_Attack\\'
    a_input_address = base_address + 'xiaoshuo.360.cn_20160116_32\\anomaly'
    a_output_address_1 = base_address + 'xiaoshuo.360.cn_20160116_32_split\\test_anomaly'
    a_output_address_2 = base_address + 'xiaoshuo.360.cn_20160116_32_split\\train_anomaly'
    random_split(a_input_address, a_output_address_1, a_output_address_2)

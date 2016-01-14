__author__ = 'j-lijiawei'


def cut_out(in_add, out_add, c_len):
    try:
        with open(in_add, 'rb') as infile, open(out_add, 'wb') as outfile:
            for i in range(c_len):
                line = infile.readline()
                if line == '\n':
                    continue
                outfile.write(line)
    except IOError as e:
        print 'It has error when cut out file.'
        print e

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\Attack\\attack_mall.360.com_20151231_31\\'
    infileAddress = base_address + 'attack_input'
    outfileAddress = base_address + 'attack_input_1000'
    cutLength = 1000
    cut_out(infileAddress, outfileAddress, cutLength)

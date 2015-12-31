__author__ = 'j-lijiawei'


def cutOut(in_add, out_add, c_len):
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
    infileAddress = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\20150918_part'
    outfileAddress = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\20150918_part_10000'
    cutLength = 10000
    cutOut(infileAddress, outfileAddress, cutLength)

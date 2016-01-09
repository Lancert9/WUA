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
    infileAddress = 'E:\\Lancer\\360WUA\\WUA_data_container\\Flow\\Demo\\flow_415s'
    outfileAddress = 'E:\\Lancer\\360WUA\\WUA_data_container\\Flow\\Demo\\flow_20s'
    cutLength = 20
    cutOut(infileAddress, outfileAddress, cutLength)

__author__ = 'j-lijiawei'


def combine(infile_base_address, file_number, outfile_address):
    with open(outfile_address, 'wb') as outfile:
        for i in range(0, file_number + 1):
            infile_address = "%s\\part-%05d" % (infile_base_address, i)
            with open(infile_address, 'rb') as infile:
                for line in infile:
                    outfile.write(line)
            print "part-%d: finished" % i


if __name__ == "__main__":
    a_infile_base_address = "E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\" \
                            "flow_mall.360.com_20160104_1\\unzip"
    a_file_number = 88
    a_outfile_address = "E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\" \
                        "flow_mall.360.com_20160104_1\\flow_input"
    combine(a_infile_base_address, a_file_number, a_outfile_address)
    print "Combine finished"

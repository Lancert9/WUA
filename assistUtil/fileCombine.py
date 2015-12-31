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
    a_infile_base_address = "D:\\My360File\\web_alert\\skyeye-sensor\\result_attack_20151113_1\\unzip"
    a_file_number = 11
    a_outfile_address = "D:\\My360File\\web_alert\\skyeye-sensor\\result_attack_20151113_1\\unzip\\all"
    combine(a_infile_base_address, a_file_number, a_outfile_address)
    print "Combine finished"

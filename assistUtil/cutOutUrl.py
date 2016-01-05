__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


def main(input_address, out_address):
    with open(input_address, 'rb') as infile, open(out_address, 'wb') as outfile:
        for line in infile:
            record = line.strip(" \n").split("\t")
            if len(record) == 13:
                url = record[_uri]
                outfile.write("%s\n" % url)

if __name__ == '__main__':
    d_input_address = "E:\\WUA_data_container\\data_container\\2016-12-1_30days\\Skyeye_Sensor\\" \
                      "FLow\\flow_mall.360.com_20151231_31\\Demo\\flow_415s"
    d_output_address = "E:\\WUA_data_container\\data_container\\2016-12-1_30days\\Skyeye_Sensor\\" \
                       "FLow\\flow_mall.360.com_20151231_31\\Demo\\url_415s"
    main(d_input_address, d_output_address)
    print 'Cut out complete.'

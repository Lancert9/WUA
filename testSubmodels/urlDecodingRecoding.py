from urllib import unquote


def set_url_code(url):
    if '?' in url:
        path, para = url.split('?', 1)
    else:
        path = url
        para = ""

    # decoding the path segment
    while True:
        path_decode = unquote(path)
        if path_decode == path:
            break
        path = path_decode

    # combining the numerical part
    path_list = path.split('/')
    path_code = []
    for part in path_list:
        part_list = []
        number_flag = False
        for a_char in part:
            if a_char.isdigit():
                if not number_flag:
                    number_flag = True
                    part_list.append('D')
            else:
                number_flag = False
                part_list.append(a_char)
        path_code.append(''.join(part_list))
    path_code = 'PATH_HEAD' + '/'.join(path_code) + '/PATH_END'

    # decoding the parameter segment
    while True:
        para_decode = unquote(para)
        if para_decode == para:
            break
        para = para_decode
    para_code = para

    return path_code, para_code

if __name__ == '__main__':
    infile_address = 'E:\\WUA_data_container\\data_container\\2016-12-1_30days\\Skyeye_Sensor\\' \
                     'FLow\\flow_mall.360.com_20151231_31\\Demo\\url_415s'
    outfile_address_1 = 'E:\\WUA_data_container\\data_container\\2016-12-1_30days\\Skyeye_Sensor\\' \
                        'FLow\\flow_mall.360.com_20151231_31\\Demo\\path_415s'
    outfile_address__2 = 'E:\\WUA_data_container\\data_container\\2016-12-1_30days\\Skyeye_Sensor\\' \
                         'FLow\\flow_mall.360.com_20151231_31\\Demo\\para_415s'
    with open(infile_address, 'rb') as infile, open(outfile_address_1, 'wb') as out_path_file, \
            open(outfile_address__2, 'wb') as out_para_file:
        for line in infile:
            record = line.strip(" \n")
            record_path, record_para = set_url_code(record)
            out_path_file.write("%s\n" % record_path)
            out_para_file.write("%s\n" % record_para)

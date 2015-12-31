from urllib import unquote

__author__ = 'j-lijiawei'

input_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Input_Flow\\HuaJiao_wvs_1113'
output_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\For liuBo\\test_wvs_path'
(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


def setPathCode(url):
    path = url.split('?', 1)[0]
    # decoding the url
    while True:
        path_uncode = unquote(path)
        if path_uncode == path:
            break
        path = path_uncode
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
    path_code = ' '.join(path_code.split('/'))
    return path_code

with open(input_address, 'rb') as infile, open(output_address, 'wb') as outfile:
    for line in infile:
        line = line.rstrip('\n')
        record = line.split('\t')
        if len(record) == 13:
            url_field = record[_uri]
            path_code = setPathCode(url_field)
            outfile.write('%s\n' % path_code)

print 'Make RNN Input System finished.'




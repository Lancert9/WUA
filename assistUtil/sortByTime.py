import pickle

__author__ = 'j-lijiawei'



def sortOriginalUrl():
    infile_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Input_Flow\\HuaJiao_wvs_1113'
    outfile_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_timeOrder'
    # model_save_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_time2url.pickle'

    (_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

    original_time2url_list = []

    with open(infile_address, 'rb') as infile, open(outfile_address, 'wb') as outfile:
        for line in infile:
            line = line.rstrip(' \n')
            record = line.split('\t')
            if len(record) == 13:
                time_field = record[_access_time].split(' ')[1]
                url_field = record[_uri]
                original_time2url_list.append((time_field, url_field))
        original_time2url_list = sorted(original_time2url_list, key=lambda d: d[0])

        # with open(model_save_address, 'wb') as save:
        #     pickle.dump(time2url_list, save)

        for time, url in original_time2url_list:
            outfile.write('%s\t%s\n' % (time, url))

        return original_time2url_list


def sortAnomalyResult():
    infile_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_result'
    outfile_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_result_timeOrder'
    # model_save_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_result_time2url.pickle'

    result_time2url_list = []

    with open(infile_address, 'rb') as infile, open(outfile_address, 'wb') as outfile:
        for line in infile:
            line = line.rstrip(' \n')
            record = line.split('\t')
            if len(record) == 2:
                time_field = record[0].split(' ')[1]
                url_field = record[1]
                result_time2url_list.append((time_field, url_field))
        result_time2url_list = sorted(result_time2url_list, key=lambda d: d[0])

        # with open(model_save_address, 'wb') as save:
        #     pickle.dump(time2url_list, save)

        for time, url in result_time2url_list:
            outfile.write('%s\t%s\n' % (time, url))

        return result_time2url_list


def labelresult(org_list, res_list):
    outfile_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_result_timeOrder_label'
    time_url_label_dict = {}
    with open(outfile_address, 'wb') as outfile:
        for item in org_list:
            if item in res_list:
                outfile.write('%s\t%s\t%s\n' % (item[0], item[1], 'Anomaly'))
                time_url_label_dict[item] = 'Anomaly'
            else:
                outfile.write('%s\t%s\t%s\n' % (item[0], item[1], 'Normal'))
                time_url_label_dict[item] = 'Normal'


if __name__ == '__main__':
    list_1 = sortOriginalUrl()
    list_2 = sortAnomalyResult()
    labelresult(list_1, list_2)
    print 'Sort system finished.'

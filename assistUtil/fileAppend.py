__author__ = 'j-lijiawei'


def add(address, content):
    with open(address, 'ab') as the_file:
        for item in content:
            the_file.write('%s\n' % item)


if __name__ == '__main__':
    file_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\20150918_part'
    add_content = []
    add_content.append('11:59\t10.0.0.1\t80\t10.0.0.2\t8080\ttest_method\t/api/getconf.json?lalala=cd6530eae58e4316a4b'
                       '7fe843bd275ea&ver=1.0\t10.16.13.129\ttest_origin\ttest_cookie\ttest'
                       '_uagent\ttest_refer\ttest_data_1')
    add_content.append('12:59\t10.0.0.1\t80\t10.0.0.2\t8080\ttest_method\t/api/heartbeat.json?lalala=cd6530eae58e4316a4'
                       'b&ver=1.0\t10.16.13.129\ttest_origin\ttest_cookie\ttest_uagent\ttest_refer\ttest_data_2')
    add(file_address, add_content)
    print 'File append finished.'

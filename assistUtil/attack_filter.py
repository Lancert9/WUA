# -*- coding:utf-8 -*-
__author__ = 'j-lijiawei'


def input_attack_filter(attack_address, flow_address, output_address):
    (_time, _sip, _sport, _dip, _dport, _hostname, _content, _patten, _type) = range(9)
    (f_time, f_sip, f_sport, f_dip, f_dport, f_method, f_uri, f_host, f_origin,
     f_cookie, f_uagent, f_refer, f_data) = range(13)

    attack_para_pool = set()
    attack_path_pool = set()
    attack_agent_pool = set()
    attack_cookie_pool = set()
    with open(attack_address, 'rb') as attack_inputfile, open(flow_address, 'rb') as flow_inputfile, \
            open(output_address, 'wb') as outputfile:
        for line in attack_inputfile:
            content = line.rstrip(' \n').split('\t')[_content]
            # print len('url参数值')
            if 'url参数值' in content:
                content = content[13:]
                attack_para_pool.add(content)
            elif 'url参数名值' in content:
                content = content[16:]
                segs = content.split('&')
                values = []
                for seg in segs:
                    if '=' in seg:
                        try:
                            var, value = seg.split("=", 1)
                            values.append(value)
                        except Exception:
                            print seg
                            raise ValueError
                    else:
                        values.append(seg)

                content = " ".join(values)
                attack_para_pool.add(content)
            elif 'User-Agent' in content:
                content = content[11:]
                attack_agent_pool.add(content)
            elif 'url' == content[:3]:
                content = content[4:]
                attack_path_pool.add(content)
            elif 'Cookie' == content[:6]:
                content = content[7:]
                attack_cookie_pool.add(content)
            else:
                print content
                raise ValueError

        for line in flow_inputfile:
            record = line.rstrip(' \n').split('\t')
            u_agent = record[f_uagent]
            u_cookie = record[f_cookie]
            if u_agent not in attack_agent_pool and u_cookie not in attack_cookie_pool:
                url = record[f_uri]
                path = url.split('?', 1)[0]
                para = url.lstrip(path)
                if path not in attack_path_pool:
                    para_segs = para.split('&')
                    values = []
                    for seg in para_segs:
                        if '=' in seg:
                            var, value = seg.split('=', 1)
                            values.append(value)
                        else:
                            values.append(seg)
                    para_str = " ".join(values)
                    if para_str not in attack_para_pool:
                        outputfile.write("%s\n" % line)
        print "attack_agent_pool: ", attack_agent_pool


def output_attack_filter(attack_address, flow_address, in_attack_address, out_attack_address):
    (_time, _sip, _sport, _dip, _dport, _hostname, _content, _patten, _type) = range(9)
    (f_time, f_sip, f_sport, f_dip, f_dport, f_method, f_uri, f_host, f_origin,
     f_cookie, f_uagent, f_refer, f_data) = range(13)

    attack_para_pool = set()
    attack_path_pool = set()
    attack_agent_pool = set()
    attack_cookie_pool = set()
    with open(attack_address, 'rb') as attack_inputfile, open(flow_address, 'rb') as flow_inputfile, \
            open(in_attack_address, 'wb') as in_attack_file, open(out_attack_address, 'wb') as out_attack_file:
        i = 0
        for line in attack_inputfile:
            i += 1
            if i % 10000 == 0:
                print 'attack finished: ', i
            content = line.rstrip(' \n').split('\t')[_content]
            # print len('url参数值')
            if 'url参数值' in content:
                content = content[13:]
                attack_para_pool.add(content)
            elif 'url参数名值' in content:
                content = content[16:]
                segs = content.split('&')
                values = []
                for seg in segs:
                    if '=' in seg:
                        try:
                            var, value = seg.split("=", 1)
                            values.append(value)
                        except Exception:
                            print seg
                            raise ValueError
                    else:
                        values.append(seg)

                content = " ".join(values)
                attack_para_pool.add(content)
            elif 'User-Agent' in content:
                content = content[11:]
                attack_agent_pool.add(content)
            elif 'url' == content[:3]:
                content = content[4:]
                attack_path_pool.add(content)
            elif 'Cookie' == content[:6]:
                content = content[7:]
                attack_cookie_pool.add(content)
            else:
                print content
                raise ValueError
        j = -1
        reason_content_dict = {}
        reason = ""
        content = ""
        for line in flow_inputfile:
            line = line.rstrip('\n')
            line = line.lstrip('\t')

            j += 1
            if j % 10000 == 0:
                print "flow finished: ", j

            if j % 2 == 0:
                reason = line
                continue
            else:
                content = line
                attack_flag = False
                record = line.split('\t')
                u_agent = record[f_uagent]
                u_cookie = record[f_cookie]
                if u_agent not in attack_agent_pool and u_cookie not in attack_cookie_pool \
                        and u_cookie not in attack_agent_pool:
                    url = record[f_uri]
                    path = url.split('?', 1)[0]
                    para = url.lstrip(path)
                    if path not in attack_path_pool:
                        para_segs = para.split('&')
                        values = []
                        for seg in para_segs:
                            if '=' in seg:
                                var, value = seg.split('=', 1)
                                values.append(value)
                            else:
                                values.append(seg)
                        para_str = " ".join(values)
                        if para_str not in attack_para_pool:
                            attack_flag = False
                        else:
                            attack_flag = True
                    else:
                        attack_flag = True
                else:
                    attack_flag = True

                if attack_flag is True:
                    in_attack_file.write("%s\n" % reason)
                    in_attack_file.write("\t%s\n" % content)
                else:
                    out_attack_file.write("%s\n" % reason)
                    out_attack_file.write("\t%s\n" % content)

if __name__ == '__main__':
    input_attack_address = ''
    input_flow_address = ''
    filter_output_address = ''
    input_attack_filter(input_attack_address, input_flow_address, filter_output_address)

    # input_attack_address = ''
    # input_result_address = ''
    # filter_in_attack_address = ''
    # filter_out_attack_address = ''
    # output_attack_filter(input_attack_address, input_result_address,
    #                      filter_in_attack_address, filter_out_attack_address)


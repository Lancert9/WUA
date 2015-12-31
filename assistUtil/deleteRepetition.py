import pickle
__author__ = 'j-lijiawei'


def main(input_address, output_address, dictSave_address):
    with open(input_address, 'rb') as infile, open(output_address, 'wb') as outfile:
        line_flag = 0
        add_flag = False
        tmp_record = ''
        result = {}
        reason_path_dict = {}
        for record in infile:
            record = record.rstrip(' \n')
            record = record.lstrip(' \t')
            if line_flag % 2 == 0:
                if "Para: " in record:
                    try:
                        a_reason, a_para, a_path = record.split('\t')
                        a_reason_path = a_reason + a_path
                    except Exception:
                        print record
                else:
                    a_reason_path = record
                if a_reason_path in reason_path_dict:
                    add_flag = False
                else:
                    add_flag = True
                    reason_path_dict[a_reason_path] = True
                    tmp_record = record
            else:
                if add_flag:
                    result[tmp_record] = record
                    outfile.write('%s\n' % tmp_record)
                    outfile.write('\t%s\n' % record)
            line_flag += 1
        # for reason, url in result.items():
        #     outfile.write(reason)
        #     outfile.write('\t%s' % url)
        with open(dictSave_address, 'wb') as savedata:
            pickle.dump(result, savedata)
    print 'deleting repetiton is finished.'


if __name__ == '__main__':
    a_input_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Output_Attack_Filter\\result_out_attack_filtered_huajiao_wvs_1113_DR'
    a_output_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Delete_Repetition\\result_out_attack_filtered_huajiao_wvs_1113_DR'
    a_dictSave_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Delete_Repetition\\result_out_attack_filtered_huajiao_wvs_1113_DR_dict.pickle'
    main(a_input_address, a_output_address, a_dictSave_address)

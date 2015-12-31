import pickle
import numpy as np
__author__ = 'j-lijiawei'


def main(a_record_dict, output_address, number):
    line_number_dict = {}
    line_sum = len(a_record_dict)
    line_number = 0
    selected_dict = {}
    for reason in a_record_dict:
        line_number_dict[line_number] = reason
        line_number += 1
    tmp = range(line_sum)
    np.random.shuffle(tmp)
    for i in range(number):
        reason = line_number_dict[tmp[i]]
        selected_dict[reason] = a_record_dict[reason]
    with open(output_address, 'wb') as outfile:
        for reason, url in selected_dict.items():
            outfile.write("%s\n" % reason)
            outfile.write('\t%s\n' % url)
    print 'random select finished.'


if __name__ == '__main__':
    a_input_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Delete_Repetition\\result_out_attack_filtered_huajiao_wvs_1113_DR_dict.pickle'
    a_output_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Random_Select\\result_out_attack_filtered_huajiao_wvs_1113_DR_200'
    with open(a_input_address, 'rb') as readdata:
        a_record_dict = pickle.load(readdata)
    main(a_record_dict, a_output_address, 200)

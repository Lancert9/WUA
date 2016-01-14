# -*- coding=utf-8 -*-
import json

__author__ = 'j-lijiawei'

SOH = chr(1)


def attack_statistic(attack_address, type_stored_address):
    a_time, a_sip, a_sport, a_dip, a_dport, a_hostname, a_content, a_patten, a_type = range(9)

    attack_content_type = set()
    attack_type = set()
    with open(attack_address, 'rb') as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            record_content = record[a_content]
            content_type = record_content.split(SOH)[0]
            attack_content_type.add(content_type)

            record_type = record[a_type]
            attack_type.add(record_type)

    with open(type_stored_address, 'wb') as outfile:
        json.dump(list(attack_content_type), outfile, ensure_ascii=False, indent=4, separators=(',', ':'))
        outfile.write('\n\n')
        json.dump(list(attack_type), outfile, ensure_ascii=False, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\Attack\\attack_mall.360.com_20151231_31\\'
    a_attack_address = base_address + 'attack_input'
    a_type_stored_address = base_address + 'attack_type.json'
    attack_statistic(a_attack_address, a_type_stored_address)

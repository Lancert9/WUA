from __future__ import division
from pprint import pprint

__author__ = 'j-lijiawei'

(_path_prop, _special_symbol_prop, _enumeration, _variable_composition,
 _variable_order, _value_length_prop, _value_distribution1, _value_distribution2) = range(8)


def cal_default(feature_address):
    default_value_dict = {
                            'special_symbol_prop': 0,
                            'value_length_prop': 0,
                            'value_distribution1': 0,
                            'value_distribution2': 0
                          }
    special_symbol_prop_sum = 0
    special_symbol_prop_num = 0
    value_length_prop_sum = 0
    value_length_prop_num = 0
    value_distribution1_sum = 0
    value_distribution1_num = 0
    value_distribution2_sum = 0
    value_distribution2_num = 0

    with open(feature_address) as infile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            the_special_symbol_prop = record[_special_symbol_prop]
            the_value_length_prop = record[_value_length_prop]
            the_value_distriburion1 = record[_value_distribution1]
            the_value_distriburion2 = record[_value_distribution2]

            if the_special_symbol_prop != 'Default':
                special_symbol_prop_sum += float(the_special_symbol_prop)
                special_symbol_prop_num += 1

            if the_value_length_prop != 'Default' and the_value_length_prop != 'nan':
                value_length_prop_sum += float(the_value_length_prop)
                value_length_prop_num += 1

            if the_value_distriburion1 != 'Default':
                value_distribution1_sum += float(the_value_distriburion1)
                value_distribution1_num += 1

            if the_value_distriburion2 != 'Default':
                value_distribution2_sum += float(the_value_distriburion2)
                value_distribution2_num += 1

    default_value_dict['special_symbol_prop'] = special_symbol_prop_sum / special_symbol_prop_num
    default_value_dict['value_length_prop'] = value_length_prop_sum / value_length_prop_num
    default_value_dict['value_distribution1'] = value_distribution1_sum / value_distribution1_num
    default_value_dict['value_distribution2'] = value_distribution2_sum / value_distribution2_num

    return default_value_dict


def fill(feature_address, feature_filled, default_value_dict):
    special_symbol_prop_default = default_value_dict['special_symbol_prop']
    value_length_prop_default = default_value_dict['value_length_prop']
    value_distribution1_default = default_value_dict['value_distribution1']
    value_distribution2_default = default_value_dict['value_distribution2']

    with open(feature_address, 'rb') as infile, open(feature_filled, 'wb') as outfile:
        record_num = 0
        for line in infile:
            record = line.strip(' \n').split('\t')
            record_num += 1

            if record[_special_symbol_prop] == 'Default':
                record[_special_symbol_prop] = special_symbol_prop_default

            if record[_enumeration] == 'Default':
                record[_enumeration] = 0.5

            if record[_variable_composition] == 'Default':
                record[_variable_composition] = 0.5

            if record[_variable_order] == 'Default':
                record[_variable_order] = 0.5

            if record[_value_length_prop] == 'Default' or record[_value_length_prop] == 'nan':
                record[_value_length_prop] = value_length_prop_default

            if record[_value_distribution1] == 'Default':
                record[_value_distribution1] = value_distribution1_default

            if record[_value_distribution2] == 'Default':
                record[_value_distribution2] = value_distribution2_default

            record = [str(feature) for feature in record]
            outfile.write('%s\n' % '\t'.join(record))

        print "Fill Records %s" % record_num


if __name__ == '__main__':
    base_address = 'E:\\WUA_data_container\\data_container\\Detect\\mall.360.com_20151231_31\\'
    a_train_feature_address = base_address + 'train_feature'
    a_default_value_dict = cal_default(a_train_feature_address)

    a_feature_address = base_address + 'test_feature'
    a_feature_filled = base_address + 'test_feature_filled'

    pprint(a_default_value_dict)
    fill(a_feature_address, a_feature_filled, a_default_value_dict)

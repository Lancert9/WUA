from __future__ import division
from copy import copy

__author__ = 'j-lijiawei'

(_path_prop, _special_symbol_prop, _enumeration, _variable_composition,
 _variable_order, _value_length_prop, _value_distribution1, _value_distribution2) = range(8)


def cal_default(train_feature_list):
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

    for record in train_feature_list:
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


def fill(feature_list, default_value_dict):
    special_symbol_prop_default = default_value_dict['special_symbol_prop']
    value_length_prop_default = default_value_dict['value_length_prop']
    value_distribution1_default = default_value_dict['value_distribution1']
    value_distribution2_default = default_value_dict['value_distribution2']

    record_filled_list = []
    for record in feature_list:
        record_filled = copy(record)

        if record[_special_symbol_prop] == 'Default':
            record_filled[_special_symbol_prop] = special_symbol_prop_default

        if record[_enumeration] == 'Default':
            record_filled[_enumeration] = 0.5

        if record[_variable_composition] == 'Default':
            record_filled[_variable_composition] = 0.5

        if record[_variable_order] == 'Default':
            record_filled[_variable_order] = 0.5

        if record[_value_length_prop] == 'Default' or record[_value_length_prop] == 'nan':
            record_filled[_value_length_prop] = value_length_prop_default

        if record[_value_distribution1] == 'Default':
            record_filled[_value_distribution1] = value_distribution1_default

        if record[_value_distribution2] == 'Default':
            record_filled[_value_distribution2] = value_distribution2_default

        record_filled = [str(feature) for feature in record_filled]
        record_filled_list.append(record_filled)

    return record_filled_list

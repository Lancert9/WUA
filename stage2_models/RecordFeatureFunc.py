"""
    Calculating the flow record's feature.
"""
from __future__ import division
from math import log
from scipy.stats import chisquare

__author__ = 'j-lijiawei'

special_symbols_list = set(list("""~`!@#$%^&*()+={}[]|\:;"'<>,./?"""))


def calculate(flow_record, host_model):
    host_feature = host_model['host_feature']

    host_path_element_count = host_feature['path_element_count']
    host_value_special_symbol_prop = host_feature['value_specialSymbol_prop']
    host_variable_enumeration = host_feature['variable_enumeration']
    host_variable_composition_pool = host_feature['variable_composition_pool']
    host_variable_order_rule = host_feature['variable_order_rule']
    host_value_length_distribution = host_feature['value_length_distribution']
    host_value_distribution1 = host_feature['value_distribution1']
    host_value_distribution2 = host_feature['value_distribution2']

    flow_record['path_prop'] = _cal_path_prop(flow_record, host_path_element_count)
    flow_record['specialSymbol_prop'] = _cal_special_symbol_prop(flow_record, host_value_special_symbol_prop)
    flow_record['enumeration'] = _cal_enumeration(flow_record, host_variable_enumeration)
    flow_record['variable_composition'] = _cal_variable_composition(flow_record, host_variable_composition_pool)
    flow_record['variable_order'] = _cal_variable_order(flow_record, host_variable_order_rule)
    flow_record['value_length_prop'] = _cal_value_length_prop(flow_record, host_value_length_distribution)
    flow_record['value_distribution1'] = _cal_value_distribution1(flow_record, host_value_distribution1)
    flow_record['value_distribution2'] = _cal_value_distribution2(flow_record, host_value_distribution2)


def calculate_path_prop(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_path_element_count = host_feature['path_element_count']
    flow_record['path_prop'] = _cal_path_prop(flow_record, host_path_element_count)


def calculate_special_symbol_prop(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_value_special_symbol_prop = host_feature['value_specialSymbol_prop']
    flow_record['specialSymbol_prop'] = _cal_special_symbol_prop(flow_record, host_value_special_symbol_prop)


def calculate_enumeration(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_variable_enumeration = host_feature['variable_enumeration']
    flow_record['enumeration'] = _cal_enumeration(flow_record, host_variable_enumeration)


def calculate_variable_composition(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_variable_composition_pool = host_feature['variable_composition_pool']
    flow_record['variable_composition'] = _cal_variable_composition(flow_record, host_variable_composition_pool)


def calculate_variable_order(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_variable_order_rule = host_feature['variable_order_rule']
    flow_record['variable_order'] = _cal_variable_order(flow_record, host_variable_order_rule)


def calculate_value_length_prop(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_value_length_distribution = host_feature['value_length_distribution']
    flow_record['value_length_prop'] = _cal_value_length_prop(flow_record, host_value_length_distribution)


def calculate_value_distribution1(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_value_distribution1 = host_feature['value_distribution1']
    flow_record['value_distribution1'] = _cal_value_distribution1(flow_record, host_value_distribution1)


def calculate_value_distribution2(flow_record, host_model):
    host_feature = host_model['host_feature']
    host_value_distribution2 = host_feature['value_distribution2']
    flow_record['value_distribution2'] = _cal_value_distribution2(flow_record, host_value_distribution2)


def _cal_path_prop(flow_record, host_path_element_count):
    """
    1. P(A/B/C/D) = P(A) * P(B|A) * P(C|AB) * P(D|ABC)
        depending on Bigram model, we can get:
               = P(A) * P(B|A) * P(C|B) * P(D|C)
    2. use 'ln' to transform the equation:
        P(A/B/C/D) -> ln(A/B/C/D) = ln(A) + ln(B|A) + ln(C|B) + ln(D|C)
    3. 'A' must be 'PATH_HEAD', and we only care about the relative value, so 'ln(A)' can be ignored:
        lnP(A/B/C/D) = lnP(B|A) + lnP(C|B) + lnP(D|C)
    4. depending on maximum likelihood estimate, we can have:
        P(B|A) = Count(A, B) / Count(A);
        P(C|B) = Count(B, C) / Count(B);
        P(D|C) = Count(C, D) / Count(C)
    5. depending on Laplace-smooth, we can transform the equation:
        P(B|A) = (Count(A, B) + 1) / (Count(A) + V);
        P(C|B) = (Count(B, C) + 1) / (Count(B) + V)
        P(D|C) = (Count(C, D) + 1) / (Count(C) + V)
    6. to weaken the influence of path length:
        P(A/B/C/D) -> P(A/B/C/D) / path_length

    Note: 'Count(A, B)' means the total count of string 'AB' that 'B' occur behind 'A'
          'V' is the total type of words

    :param flow_record: FlowRecord
    :param host_path_element_count: ({'element_i': amount}, {'element_i, element_i+1': amount})
    :return: flow_record['path_prop'] = probability
    """
    single_element_dict, double_element_dict = host_path_element_count

    element_list = flow_record['path'].split('/')
    path_length = len(element_list)
    probability = 0
    v = len(single_element_dict)
    for i in range(path_length - 1):
        x = element_list[i]
        y = element_list[i + 1]
        # I transform adjacent 'xy' to 'x,y'
        x_y = x + ',' + y
        x_count = single_element_dict.get(x, 0)
        x_y_count = double_element_dict.get(x_y, 0)
        prop_i = log((x_y_count + 1) / (x_count + v))
        probability += prop_i
    probability /= path_length

    return probability


def _cal_special_symbol_prop(flow_record, host_value_special_symbol_prop):
    """
    calculate the probability of the special symbol in parameter value.
    :param flow_record: FlowRecord
    :param host_value_special_symbol_prop: {path: {variable: {specialSymbol: prop}}}
    :return: flow_record['specialSymbol_prop'] = probability
    """
    min_prop = 1
    variable_value_dict = flow_record['variable_value_dict']
    variable_dict = host_value_special_symbol_prop[flow_record['path']]

    for variable, value in variable_value_dict.items():
        special_symbol_dict = variable_dict[variable]
        for char in value:
            if char in special_symbols_list:
                char_prop = special_symbol_dict.get(char, 0)
                min_prop = min(min_prop, char_prop)
                if min_prop == 0:
                    return min_prop
    return min_prop


def _cal_enumeration(flow_record, host_variable_enumeration):
    """
    Return 0 if the variable type is enumeration and its corresponding value is not in value_set. Otherwise, return 1.
    :param flow_record: FlowRecord
    :param host_variable_enumeration: {path: {variable: set(value_code) or false}}
    :return: flow_record['enumeration'] = 1 or 0
    """
    variable_value_dict = flow_record['variable_value_dict']
    variable_dict = host_variable_enumeration[flow_record['path']]

    for variable, value in variable_value_dict.items():
        # enumeration is set(value_code) or false
        enumeration = variable_dict[variable]
        if enumeration is False:
            continue
        else:
            value_code = __value_encode(value)
            if value_code not in enumeration:
                return 0
    return 1


def _cal_variable_composition(flow_record, host_variable_composition_pool):
    """

    :param flow_record: FlowRecord
    :param host_variable_composition_pool: {path: set(frozenset([v1, v2, v3]), frozenset([v3, v4]), ...)}
    :return: flow_record['variable_composition'] = 1 or 0
    """
    record_variable_composition = frozenset(flow_record['variable_value_dict'].keys())
    variable_composition_pool = host_variable_composition_pool[flow_record['path']]
    if record_variable_composition:
        if record_variable_composition in variable_composition_pool:
            return 1
        else:
            return 0
    else:
        return 1


def _cal_variable_order(flow_record, host_variable_order_rule):
    """
    if there are some variable order violate the rule, return 0. Otherwise, return 1.
    :param flow_record: FlowRecord
    :param host_variable_order_rule: {path: set((v1, v2), (v1, v3), ...)}
    :return: flow_record['variable_order'] = 1 or 0
    """
    # get the parameter variable order
    para = flow_record['para']
    record_variable_reverse_order = []
    if para:
        record_variable_list = [para_seg.split('=')[0] for para_seg in para.split('&')]
        for i in range(len(record_variable_list) - 1):
            record_variable_reverse_order.append((record_variable_list[i + 1], record_variable_list[i]))

        variable_order_rule = host_variable_order_rule[flow_record['path']]

        for order in record_variable_reverse_order:
            if order in variable_order_rule:
                return 0
    return 1


def _cal_value_length_prop(flow_record, host_value_length_distribution):
    """
    calculate the minimum probability of parameter value's length
    :param flow_record: FlowRecord
    :param host_value_length_distribution: {path: {variable: {'mean': m, 'variance': v}}}
    :return: flow_record['value_length_prop'] = probability
    """
    variable_dict = host_value_length_distribution[flow_record['path']]
    variable_value_dict = flow_record['variable_value_dict']
    if variable_value_dict:
        length_prop_list = list()
        for variable, value in variable_value_dict.items():
            if variable in variable_dict:
                value_length = len(value)
                mean = variable_dict[variable]['mean']
                var = variable_dict[variable]['variance']
                if value_length > mean:
                    epsilon2 = (value_length - mean) ** 2
                    prop = 1 / (1 + epsilon2 / var)
                else:
                    prop = 1
                length_prop_list.append(prop)
            else:
                return 0
        return min(length_prop_list)
    else:
        return 1


def _cal_value_distribution1(flow_record, host_value_distribution1):
    """
    Use Chi-squared test to calculate the minimum P-value of parameter value's distribution.
    :param flow_record: FlowRecord
    :param host_value_distribution1: {path: {variable: (P0, P1, P2, P3, P4, P5)}}
    :return: flow_record['value_distribution1'] = probability
    """
    variable_value_dict = flow_record['variable_value_dict']
    variable_dict = host_value_distribution1[flow_record['path']]
    p_value_list = []
    if variable_value_dict:
        for variable, value in variable_value_dict.items():
            if variable in variable_dict:
                length = len(value)
                if length > 0:
                    exception = [interval * length for interval in variable_dict[variable]]
                    observation = __cal_value_observation1(value)
                    # it return (chi-squared, P-value)
                    p_value = chisquare(observation, exception)[1]
                else:
                    p_value = 1
                p_value_list.append(p_value)
            else:
                return 0
        return min(p_value_list)
    else:
        return 1


def _cal_value_distribution2(flow_record, host_value_distribution2):
    """
    Use Chi-squared test to calculate the minimum P-value of parameter value's distribution.
    :param flow_record: FlowRecord
    :param host_value_distribution2: {path: {variable: (P0, P1, P2, P3, P4, P5)}}
    :return: flow_record['value_distribution2'] = probability
    """
    variable_value_dict = flow_record['variable_value_dict']
    variable_dict = host_value_distribution2[flow_record['path']]
    p_value_list = []
    if variable_value_dict:
        for variable, value in variable_value_dict.items():
            if variable in variable_dict:
                length = len(value)
                if length > 0:
                    exception = [interval * length for interval in variable_dict[variable]]
                    observation = __cal_value_observation2(value)
                    # it return (chi-squared, P-value)
                    p_value = chisquare(observation, exception)[1]
                else:
                    p_value = 1
                p_value_list.append(p_value)
            else:
                return 0
        return min(p_value_list)
    else:
        return 1


def __value_encode(value):
    """
    combine the successive numerical sequence.
    :param value: str -> value
    :return: str -> value_code
    """
    value_code = []
    number_flag = False
    for char in value:
        if char.isdigit():
            if not number_flag:
                number_flag = True
                value_code.append('<D>')
        else:
            number_flag = False
            value_code.append(char)
    return ''.join(value_code)


def __cal_value_observation1(value):
    """
    To calculate the ICD list:
        ---------------------------------------------------------
         interval |  0     1      2      3        4        5
        ---------------------------------------------------------
           index  | (0)  (1-3)  (4-6)  (7-11)  (12-15)  (16-255)
        ---------------------------------------------------------
    :param value: str -> value
    :return: (count_0, count_1, count_2, count_3, count_4, count_5)
    """
    icd_list = [0] * 256
    for char in value:
        ascll = ord(char)
        icd_list[ascll] += 1
    icd_list.sort(reverse=True)

    icd_table = [0] * 6
    icd_table[0] = sum([icd_list[i] for i in range(0, 1)])
    icd_table[1] = sum([icd_list[i] for i in range(1, 4)])
    icd_table[2] = sum([icd_list[i] for i in range(4, 7)])
    icd_table[3] = sum([icd_list[i] for i in range(7, 12)])
    icd_table[4] = sum([icd_list[i] for i in range(12, 16)])
    icd_table[5] = sum([icd_list[i] for i in range(16, 256)])

    return tuple(icd_table)


def __cal_value_observation2(value):
    """
    To calculate the ICD list:
        -------------------------------------------------------------------------------------------------
         interval | uppercase  lowercase  digit              control              unprintable  extension
        -------------------------------------------------------------------------------------------------
           ASCII  |  (65-90)   (97-122)  (48-57)  (32-47, 58-64, 91-96, 123-126)  (0-31, 127)  (128-255)
        -------------------------------------------------------------------------------------------------
    A char number is divided into 6 categories.
        1. uppercase    -->    (65-90)
        2. lowercase    -->    (97-122)
        3. digit        -->    (48-57)
        4. control      -->    (32-47, 58-64, 91-96, 123-126)
        5. unprintable  -->    (0-31, 127)
        6. extension    -->    (128-255)
    :param value: str -> value
    :return: (count_0, count_1, count_2, count_3, count_4, count_5)
    """
    uppercase_set = set(range(65, 91))
    lowercase_set = set(range(97, 123))
    digit_set = set(range(48, 58))
    control_list = list()
    map(lambda x: control_list.extend(x), (range(32, 48), range(58, 65), range(91, 97), range(123, 127)))
    control_set = set(control_list)
    # map(lambda x: control_set.add(x), control_list)
    unprintable_set = set(range(32))
    unprintable_set.add(127)
    extension_set = set(range(128, 256))

    interval = [uppercase_set, lowercase_set, digit_set, control_set, unprintable_set, extension_set]
    icd_table = [0] * 6
    for char in value:
        for index, category in enumerate(interval):
            if ord(char) in category:
                icd_table[index] += 1
                break

    return tuple(icd_table)


if __name__ == '__main__':
    import pickle
    from FlowRecord import FlowRecord
    import __WriteHostFeature as Whf
    (_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) \
        = range(13)

    flow_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\' \
                   'flow_mall.360.com_20151231_31\\Demo\\flow_20s'
    host_stored_address = 'E:\\WUA_data_container\\data_container\\Complete_Model\\' \
                          'flow_mall.360.com_20151231_31\\Demo\\Host_Collector'
    host_feature_stores_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\' \
                                  'flow_mall.360.com_20151231_31\\Demo\\take_a_look_host_feature'
    flow_feature_stored_address = 'E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\' \
                                  'flow_mall.360.com_20151231_31\\Demo\\take_a_look_record_feature'

    with open(host_stored_address, 'rb') as host_collector_file:
        host_collector = pickle.load(host_collector_file)

    # for host in host_collector:
    #     test_host_feature = host['host_feature']
    #     Whf.write(test_host_feature, host_feature_stores_address)

    with open(flow_address, 'rb') as infile, open(flow_feature_stored_address, 'wb') as outfile:
        for line in infile:
            record = line.strip(' \n').split('\t')
            if len(record) == 13 and record[_host] != '':
                current_record = FlowRecord(record)
                current_model = host_collector.get_host_model(current_record['host'])

                calculate_path_prop(current_record, current_model)
                outfile.write('%s\n' % current_record['url'])
                outfile.write('\t%s\n' % current_record['path_prop'])

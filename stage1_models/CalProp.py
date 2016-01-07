"""
    Calculating the probability result of url's path or parameter part.
"""

from math import log
__author__ = 'j-lijiawei'


def calPathProp(records_dict, path_dict, path2_dict):
    """
    1. P(A/B/C/D) = P(A) * P(B|A) * P(C|AB) * P(D|ABC)
        depending on Bigram model, we can get:
               = P(A) * P(B|A) * P(C|B) * P(D|C)
    2. use 'log' to transform the equation:
        logP(A/B/C/D) = logP(A) + logP(B|A) + logP(C|B) + logP(D|C)
    3. 'A' must be 'PATH_HEAD', and we only care about the relative value, so 'logP(A)' can be ignored:
        logP(A/B/C/D) = logP(B|A) + logP(C|B) + logP(D|C)
    4. depending on maximum likelihood estimate, we can have:
        P(B|A) = Count(A, B) / Count(A); P(C|B) = Count(B, C) | Count(B); P(D|C) = Count(C, D) / Count(C)
        Note: 'Count(A, B)' means the total count of string 'AB' that 'B' occur behind 'A'
              'V' is the total type of words
    5. depending on Laplace-smooth, we can transform the equation:
        P(B|A) = (Count(A, B) + 1) / (Count(A) + V); P(C|B) = (Count(B, C) + 1) / (Count(B) + V)
        P(D|C) = (Count(C, D) + 1) / (Count(C) + V)

    :param records_dict: dict --> {UrlRecord: int} -- UrlRecord map to it's amounts
    :param path_dict: dict --> {str: int} -- Different tuple of path map to it's frequency of the occurrence
    :param path2_dict: dict --> {str: int} -- two adjacent tuple map to it's frequency of the occurrence
    :return: list[float] -- each path probability in records_dict
    """

    path_props = []     # a dict to contain path probability of records_dict's item
    for record, count in records_dict.items():
        path_code = record.get_path()
        path_list = path_code.split('/')
        total_prop = float(0)
        v = float(len(path_dict))   # the total type of words(a particular part of the path)
        # SUM logP(y|x) for each two adjacent parts
        for i in range(len(path_list) - 1):
            x = path_list[i]
            y = path_list[i + 1]
            x_y = x + ',' + y   # in previous encoding, I transform adjacent 'xy' to 'x,y'
            c_x = float(path_dict.get(x, 0))
            c_x_y = float(path2_dict.get(x_y, 0))
            prop_i = log((c_x_y + 1) / (c_x + v))
            total_prop += prop_i
        for i in range(count):
            path_props.append(total_prop)
    return path_props


def calPathProp_modi(records_dict, path_dict, path2_dict):
    """
    1. P(A/B/C/D) = P(A) * P(B|A) * P(C|AB) * P(D|ABC)
        depending on Bigram model, we can get:
               = P(A) * P(B|A) * P(C|B) * P(D|C)
    2. use 'log' to transform the equation:
        logP(A/B/C/D) = logP(A) + logP(B|A) + logP(C|B) + logP(D|C)
    3. 'A' must be 'PATH_HEAD', and we only care about the relative value, so 'logP(A)' can be ignored:
        logP(A/B/C/D) = logP(B|A) + logP(C|B) + logP(D|C)
    4. depending on maximum likelihood estimate, we can have:
        P(B|A) = Count(A, B) / Count(A); P(C|B) = Count(B, C) | Count(B); P(D|C) = Count(C, D) / Count(C)
        Note: 'Count(A, B)' means the total count of string 'AB' that 'B' occur behind 'A'
              'V' is the total type of words
    5. depending on Laplace-smooth, we can transform the equation:
        P(B|A) = (Count(A, B) + 1) / (Count(A) + V); P(C|B) = (Count(B, C) + 1) / (Count(B) + V)
        P(D|C) = (Count(C, D) + 1) / (Count(C) + V)

    :param records_dict: dict --> {UrlRecord: int} -- UrlRecord map to it's amounts
    :param path_dict: dict --> {str: int} -- Different tuple of path map to it's frequency of the occurrence
    :param path2_dict: dict --> {str: int} -- two adjacent tuple map to it's frequency of the occurrence
    :return: list[float] -- each path probability in records_dict
    """

    path_props = []     # a dict to contain path probability of records_dict's item
    for record, count in records_dict.items():
        path_code = record.get_path()
        path_list = path_code.split('/')
        path_length = len(path_list)
        total_prop = float(0)
        v = float(len(path_dict))   # the total type of words(a particular part of the path)
        # SUM logP(y|x) for each two adjacent parts
        for i in range(len(path_list) - 1):
            x = path_list[i]
            y = path_list[i + 1]
            x_y = x + ',' + y   # in previous encoding, I transform adjacent 'xy' to 'x,y'
            c_x = float(path_dict.get(x, 0))
            c_x_y = float(path2_dict.get(x_y, 0))
            prop_i = log((c_x_y + 1) / (c_x + v))
            total_prop += prop_i
        total_prop /= path_length
        for i in range(count):
            path_props.append(total_prop)
    return path_props


def detectParaProp(a_record, path_para_dict, threshold):
    """
    Detecting a url's parameter field:
        We split parameter field into kinds of 'variable: value' group by '='.
        In a specific variable, there are some special symbol in it's value part.
        So, if a probability of any special symbol is lower than the given threshold, it is detected to be anomaly.
    :param a_record: UrlRecord
    :param path_para_dict: dict --> {path_i: {variable_i : {special_symbols_i: count, -SUM-: sum_count}}}
    :param threshold: int
    :return: dict --> {str: str} --
                      When key is 'Missing' or 'Normal', it means parameter part of record is normal.
                      Otherwise, when key is 'Anomaly', it means parameter part of record is anomaly,
                      and the key 'Anomaly' map to detail reason.
    """
    a_para_code = repr(a_record.get_para())
    para_prop_result = {}
    # para_status_dict = {'path': path_code, 'para': {variable1: ([special_symbols_set]), ...}}
    # or
    # para_status_dict = {'path': path_code, 'para': 'NOT_EXIST'}
    para_status_dict = a_record.get_para_status()
    # record's path
    a_path = para_status_dict['path']
    # record's parameter
    # {variable1: ([special_symbols_set]), variable2: ([special_symbols_set]), ...}
    variable_value_dict = para_status_dict['para']
    if a_path in path_para_dict:
        # model's parameter
        # {variable_i : {special_symbols_i: count, -SUM-: sum_count}}
        para_var_dict = path_para_dict[a_path]
        if len(para_var_dict) != 0:
            if variable_value_dict != 'NOT_EXIST' and len(variable_value_dict) != 0:
                anomaly_flag = False
                anomaly_information_dict = []
                for variable, special_symbols_set in variable_value_dict.items():
                    if variable in para_var_dict:
                        for special_symbol in special_symbols_set:
                            # the special symbol's probability P(ss_i) = Count(ss_i) / Count(Sum(ss_i))
                            # Count(ss_i)
                            c_special_symbol = float(para_var_dict[variable].get(special_symbol, 0))
                            # Count(Sum(ss_i))
                            cs_special_symbol = float(para_var_dict[variable]['-SUM-'])
                            # P(ss_i)
                            p_var_value = c_special_symbol / cs_special_symbol
                            if p_var_value < threshold:
                                anomaly_flag = True
                                anomaly_information_dict.append("'%s' in %s is: %s;" % (special_symbol, variable, p_var_value))
                    else:
                        anomaly_flag = True
                        anomaly_information_dict.append('%s is mismatch;' % variable)
                if anomaly_flag:
                    anomaly_information = ' '.join(anomaly_information_dict)
                    para_prop_result['Anomaly'] = "%s\tPara: %s\tPath: %s" % (anomaly_information, a_para_code, a_path)
                else:
                    para_prop_result['Normal'] = "It's parameter is OK"
            else:
                para_prop_result['Missing'] = 'Record Para Miss'    # 'Record Para Miss'
        else:
            para_prop_result['Missing'] = 'Model Para Miss'    # 'Model Para Miss'
    else:
        para_prop_result['Missing'] = 'Path Mismatch'    # 'Path Mismatch'
    return para_prop_result

if __name__ == '__main__':
    # a_path = 'PATH_HEAD/a/b/PATH_END'
    # a_path_dict = {'a': 1, 'b': 1, 'PATH_HEAD': 2, 'PATH_END': 2}
    # a_path2_dict = {'PATH_HEAD,x': 2, 'PATH_HEAD,a': 1, 'a,b': 1}
    # a_AD = AnomalyDetector()
    # value = a_AD.calPathProp(a_path, a_path_dict, a_path2_dict)
    # print 'Outcome: ', value
    #
    # a_para = 'PATH_HEAD%a%b%PATH_END'
    # value1 = a_AD.calParaProp(a_para, a_path_dict, a_path2_dict)
    # print 'Outcome: ', value1
    path_list = [x for x in range(0, 10, 1)]
    para_list = [x for x in range(0, 10, 1)]
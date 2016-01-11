"""
    It generate the features of the Host Model.
"""
from __future__ import division
from pandas import DataFrame
from pandas import Series
import networkx as nx

__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)


class HostFeature:
    def __init__(self):
        # Path Probability Status = ({'element_i': amount}, {'element_i, element_i+1': amount})
        self.__path_element_count = (dict(), dict())

        # {path: {variable: {specialSymbol: prop}}}
        self.__value_specialSymbol_prop = dict()

        # {path: {variable: set(value_code) or false}}
        self.__variable_enumeration = dict()

        # {path: set(frozenset([v1, v2, v3]), frozenset([v3, v4]), ...)}
        self.__variable_composition_pool = dict()

        # {path: set((v1, v2), (v1, v3), ...)}
        self.__variable_order_rule = dict()

        # {path: {variable: {'mean': m, 'variance': v}}}
        self.__value_length_distribution = dict()

        # {path: {variable: (P0, P1, P2, P3, P4, P5)}}
        self.__value_distribution1 = dict()

        # {path: {variable: (P0, P1, P2, P3, P4, P5)}}
        self.__value_distribution2 = dict()

        # The map of the Host Model's all features.
        self.__feature_map = dict()

    def generate_all_features(self, a_record_box):
        a_path_list = a_record_box["path_list"]
        a_variable_special_symbol = a_record_box["variable_specialSymbol"]
        a_variable_value = a_record_box["variable_value"]
        a_variable_composition = a_record_box["variable_composition"]
        a_variable_order = a_record_box["variable_order"]

        self.generate_path_element_count(a_path_list)
        self.generate_value_special_symbol_prop(a_variable_special_symbol)
        self.generate_variable_enumeration(a_variable_value)
        self.generate_variable_composition_pool(a_variable_composition)
        self.generate_variable_order_rule(a_variable_order)
        self.generate_value_length_distribution(a_variable_value)
        self.generate_value_distribution1(a_variable_value)
        self.generate_value_distribution2(a_variable_value)

    def generate_path_element_count(self, path_list):
        """
        path element map to it's occurrence amount.
            self.__path_element_count

        :param path_list: [path]
        :return: ({'element_i': amount}, {'element_i, element_i+1': amount})
        """
        single_element_count = self.__path_element_count[0]
        double_element_count = self.__path_element_count[1]
        for path in path_list:
            element_list = path.split('/')
            for i, element in enumerate(element_list):
                single_element_count[element] = single_element_count.setdefault(element, 0) + 1
                if element != 'PATH_END':
                    element_right = element_list[i + 1]
                    double_element = element + ',' + element_right
                    double_element_count[double_element] = double_element_count.setdefault(double_element, 0) + 1

    def generate_value_special_symbol_prop(self, variable_special_symbol):
        """
        value map to it's probability.
            self.__value_specialSymbol_prop

        :param variable_special_symbol: {path: {variable: {specialSymbol: count}}}
        :return: {path: {variable: {specialSymbol: prop}}}
        """
        for path, variable_dict in variable_special_symbol.items():
            self.__value_specialSymbol_prop[path] = {}
            for variable, specialSymbol_dict in variable_dict.items():
                self.__value_specialSymbol_prop[path][variable] = {}
                sum_number = specialSymbol_dict['SUM']
                if sum_number != 0:
                    for special, count in specialSymbol_dict.items():
                        if special != 'SUM':
                            prop = count / sum_number
                            self.__value_specialSymbol_prop[path][variable][special] = prop

    def generate_variable_enumeration(self, variable_value):
        """
        variable map to it's enumeration type.
            self.__variable_enumeration
        :param variable_value: {path: {variable: [value]}}
        :return: {path: {variable: boolean}}
        """
        for path, variable_dict in variable_value.items():
            self.__variable_enumeration[path] = {}
            for variable, value_list in variable_dict.items():
                value_code_list = self.__value_encode(value_list)
                # flag = true -> variable is enumeration. Otherwise, is not.
                flag = self.__is_enumerated(value_code_list)
                self.__variable_enumeration[path][variable] = flag

    def generate_variable_composition_pool(self, variable_composition):
        """
        path map to it's variable composition pool.
            self.__variable_composition_pool
        :param variable_composition: {path: set(frozenset([v1, v2, v3]), frozenset([v3, v4]), ...)}
        :return: {path: set(frozenset([v1, v2, v3]), frozenset([v3, v4]), ...)}
        """
        self.__variable_composition_pool.update(variable_composition)

    def generate_variable_order_rule(self, variable_order):
        """
        path map to it's variable order rule.
            self.__variable_order_rule

        :param variable_order: {path: set((v1, v2, v3), (v3, v4), ...)}
        :return: {path: set((v1, v2), (v1, v3), ...)}
                 inside tuple consist of two variable, which specifies the order rule.
        """
        for path, variable_order_set in variable_order.items():
            self.__variable_order_rule[path] = self.__cal_variable_order_rule(variable_order_set)

    def generate_value_length_distribution(self, variable_value):
        """
        variable map to it's distribution(mean, variance).
            self.__value_length_distribution

        :param variable_value: {path: {variable: [value]}}
        :return: {path: {variable: {'mean': m, 'variance': v}}}
        """
        for path, variable_dict in variable_value.items():
            self.__value_length_distribution[path] = {}
            for variable, value_list in variable_dict.items():
                length_list = [len(value) for value in value_list]
                length_series = Series(length_list)
                mean = length_series.mean()
                var = length_series.var()

                self.__value_length_distribution[path][variable] = {'mean': mean, 'variance': var}

    def generate_value_distribution1(self, variable_value):
        """
        variable map to it's value distribution1.
            self.__value_distribution1

        :param variable_value: {path: {variable: [value]}}
        :return: {path: {variable: (P0, P1, P2, P3, P4, P5)}}
        """
        for path, variable_dict in variable_value.items():
            self.__value_distribution1[path] = {}
            for variable, value_list in variable_dict.items():
                self.__value_distribution1[path][variable] = self.__cal_value_distribution1(value_list)

    def generate_value_distribution2(self, variable_value):
        """
        variable map to it's value distribution2.
            self.__value_distribution2
        :param variable_value: {path: {variable: [value]}}
        :return: {path: {variable: (P0, P1, P2, P3, P4, P5)}}
        """
        for path, variable_dict in variable_value.items():
            self.__value_distribution2[path] = {}
            for variable, value_list in variable_dict.items():
                self.__value_distribution2[path][variable] = self.__cal_value_distribution2(value_list)

    @staticmethod
    def __value_encode(value_list):
        """
        combine the successive numerical sequence.
        :param value_list: [value]
        :return: [value_code]
        """
        value_code_list = []
        for value in value_list:
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
            value_code_list.append(''.join(value_code))
        return value_code_list

    @staticmethod
    def __is_enumerated(value_code_list):
        """
        To judge the parameter variable is enumerated or not.

        :param value_code_list: [value_code]
        :return: set(value_code) if the variable is enumerated type. Otherwise, return False.
        """
        length = len(value_code_list)
        if length > 1:
            f_function = range(1,  length + 1)

            g_function = list()
            value_set = set()
            count = 0
            for value in value_code_list:
                if value not in value_set:
                    value_set.add(value)
                    count += 1
                else:
                    count -= 1
                g_function.append(count)

            f_g_df = DataFrame({'f_function': f_function, 'g_function': g_function})
            f_g_cor = f_g_df['f_function'].corr(f_g_df['g_function'])

            return value_set if f_g_cor < 0 else False
        else:
            return False

    @staticmethod
    def __cal_variable_order_rule(variable_order_set):
        """
        To record the parameter variable's all fixed order.

        :param variable_order_set: set((v1, v2, v3), (v3, v4), ...)
        :return: set((v1, v2), (v1, v3), ...)
        """
        result_order = set()

        order_collection = set()
        for order_seg in variable_order_set:
            for i in range(len(order_seg) - 1):
                order_collection.add((order_seg[i], order_seg[i + 1]))

        g = nx.DiGraph()
        g.add_edges_from(order_collection)
        connectivity_dict = dict([])
        for source_node, connect_dict in nx.all_pairs_node_connectivity(g).items():
            connectivity_dict[source_node] = set()
            for target_node, hop in connect_dict.items():
                if hop > 0:
                    connectivity_dict[source_node].add(target_node)

        node_list = g.nodes()
        node_count = len(node_list)
        for i in range(node_count):
            for j in range(i + 1, node_count):
                node_1 = node_list[i]
                node_2 = node_list[j]
                # if node_1 connect to node_2
                connect_1_2 = node_2 in connectivity_dict[node_1]
                # if node_2 connect to node_1
                connect_2_1 = node_1 in connectivity_dict[node_2]
                if connect_1_2 and not connect_2_1:
                    result_order.add((node_1, node_2))
                elif connect_2_1 and not connect_1_2:
                    result_order.add((node_2, node_1))
                else:
                    continue

        return result_order

    @staticmethod
    def __cal_value_distribution1(value_list):
        """
        To calculate the ICD list:
            ---------------------------------------------------------
             interval |  0     1      2      3        4        5
            ---------------------------------------------------------
               index  | (0)  (1-3)  (4-6)  (7-11)  (12-15)  (16-255)
            ---------------------------------------------------------

        :param value_list: [value]
        :return: (P0, P1, P2, P3, P4, P5)
        """
        result_prop_list = list()
        number = len(value_list)
        icd_table_list = list()

        for value in value_list:
            icd_list = [0] * 256
            for char in value:
                ascll = ord(char)
                icd_list[ascll] += 1
            icd_list.sort(reverse=True)

            value_length = len(value)
            icd_table = [0] * 6
            if value_length != 0:
                icd_table[0] = sum([icd_list[i] for i in range(0, 1)]) / value_length
                icd_table[1] = sum([icd_list[i] for i in range(1, 4)]) / value_length
                icd_table[2] = sum([icd_list[i] for i in range(4, 7)]) / value_length
                icd_table[3] = sum([icd_list[i] for i in range(7, 12)]) / value_length
                icd_table[4] = sum([icd_list[i] for i in range(12, 16)]) / value_length
                icd_table[5] = sum([icd_list[i] for i in range(16, 256)]) / value_length

            icd_table_list.append(icd_table)

        for interval in range(6):
            interval_sum = 0
            for record in icd_table_list:
                interval_sum += record[interval]
            result_prop_list.append(interval_sum / number)

        return tuple(result_prop_list)

    @staticmethod
    def __cal_value_distribution2(value_list):
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

        :param value_list: [value]
        :return: (P0, P1, P2, P3, P4, P5)
        """
        result_prop_list = list()
        number = len(value_list)
        icd_table_list = list()

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

        for value in value_list:
            value_length = len(value)
            icd_table = [0] * 6
            if value_length > 0:
                for char in value:
                    for index, category in enumerate(interval):
                        if ord(char) in category:
                            icd_table[index] += 1
                            break
                icd_table = [k / value_length for k in icd_table]
            icd_table_list.append(icd_table)

        for interval in range(6):
            interval_sum = 0
            for record in icd_table_list:
                interval_sum += record[interval]
            result_prop_list.append(interval_sum / number)

        return tuple(result_prop_list)

    def __setitem__(self, key, value):
        raise LookupError("It is not allow to set the attribute.")

    def __getitem__(self, item):
        self.__generate_all_feature_map()
        return self.__feature_map[item]

    def __generate_all_feature_map(self):
        self.__feature_map['path_element_count'] = self.__path_element_count
        self.__feature_map['value_specialSymbol_prop'] = self.__value_specialSymbol_prop
        self.__feature_map['variable_enumeration'] = self.__variable_enumeration
        self.__feature_map['variable_composition_pool'] = self.__variable_composition_pool
        self.__feature_map['variable_order_rule'] = self.__variable_order_rule
        self.__feature_map['value_length_distribution'] = self.__value_length_distribution
        self.__feature_map['value_distribution1'] = self.__value_distribution1
        self.__feature_map['value_distribution2'] = self.__value_distribution2

if __name__ == '__main__':
    from RecordBox import RecordBox
    from FlowRecord import FlowRecord
    test_record_box = RecordBox()
    test_feature_model = HostFeature()
    with open('E:\\Lancer\\360WUA\\WUA_data_container\\Flow\\Demo\\flow_20s', 'rb') as infile:
        for line in infile:
            line = line.strip(' \n').split('\t')
            if len(line) == 13 and line[_host] != '':
                t_record = FlowRecord(line)
                test_record_box.add_record(t_record)
    print 'Record add finished.'
    test_record_box.active()

    with open('E:\\Lancer\\360WUA\\WUA_data_container\\Flow\\Demo\\test_FeatureModel', 'wb') as outfile:

        # t_path_list = test_record_box['path_list']
        # test_feature_model.generate_path_element_count(t_path_list)
        # t_single_element_count, t_double_element_count = test_feature_model['path_element_count']
        # outfile.write('Single Element Count:\n')
        # for t_element, t_count in t_single_element_count.items():
        #     outfile.write('\t%s\t%d\n' % (repr(t_element), t_count))
        # outfile.write('\n\nDouble Element Count:\n')
        # for t_element, t_count in t_double_element_count.items():
        #     outfile.write('\t%s\t%d\n' % (repr(t_element), t_count))

        # variable_specialSymbol = test_record_box['variable_specialSymbol']
        # test_feature_model.generate_value_special_symbol_prop(variable_specialSymbol)
        # value_specialSymbol_prop = test_feature_model['value_specialSymbol_prop']
        # outfile.write('Value Special Symbol Probability:\n')
        # for t_path, t_variable_dict in value_specialSymbol_prop.items():
        #     outfile.write('\t%s\n' % t_path)
        #     for t_variable, t_specialSymbol_dict in t_variable_dict.items():
        #         outfile.write('\t\t%s\n' % t_variable)
        #         for specialSymbol, t_prop in t_specialSymbol_dict.items():
        #             outfile.write('\t\t\t%s:\t%f\n' % (specialSymbol, t_prop))

        # t_variable_value = test_record_box['variable_value']
        # test_feature_model.generate_variable_enumeration(t_variable_value)
        # variable_enumeration = test_feature_model['variable_enumeration']
        # outfile.write('Variable Enumeration:\n')
        # for t_path, t_variable_dict in variable_enumeration.items():
        #     outfile.write('\t%s\n' % t_path)
        #     for t_variable, t_enumerated_type in t_variable_dict.items():
        #         outfile.write('\t\t%s\t%s\n' % (t_variable, t_enumerated_type))

        # t_variable_composition = test_record_box['variable_composition']
        # test_feature_model.generate_variable_composition_pool(t_variable_composition)
        # t_variable_composition_pool = test_feature_model['variable_composition_pool']
        # outfile.write('Variable Composition:\n')
        # for t_path, t_variable_composition_set in t_variable_composition_pool.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for a_t_variable_composition in t_variable_composition_set:
        #         outfile.write('\t\t%s:\n' % a_t_variable_composition)

        # t_variable_order = test_record_box['variable_order']
        # test_feature_model.generate_variable_order_rule(t_variable_order)
        # t_variable_order_rule = test_feature_model['variable_order_rule']
        # outfile.write('Variable Order Rule:\n')
        # for t_path, t_variable_order_set in t_variable_order_rule.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable_order in t_variable_order_set:
        #         outfile.write('\t\t%s:\n' % repr(t_variable_order))

        # t_variable_value = test_record_box['variable_value']
        # test_feature_model.generate_value_length_distribution(t_variable_value)
        # t_value_length_distribution = test_feature_model['value_length_distribution']
        # outfile.write('Value Length Distribution:\n')
        # for t_path, t_variable_dict in t_value_length_distribution.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable, t_distribution in t_variable_dict.items():
        #         outfile.write('\t\t%s:\n' % t_variable)
        #         outfile.write('\t\t\tmean: %f\n' % t_distribution['mean'])
        #         outfile.write('\t\t\tvariance: %f\n' % t_distribution['variance'])

        # t_variable_value = test_record_box['variable_value']
        # test_feature_model.generate_value_distribution1(t_variable_value)
        # t_value_distribution1 = test_feature_model['value_distribution1']
        # outfile.write('Value Distribution1:\n')
        # for t_path, t_variable_dict in t_value_distribution1.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable, t_distribution in t_variable_dict.items():
        #         outfile.write('\t\t%s:\n' % t_variable)
        #         for t_i, t_prop in enumerate(t_distribution):
        #             outfile.write('\t\t\tP%d: %f\n' % (t_i, t_prop))

        t_variable_value = test_record_box['variable_value']
        test_feature_model.generate_value_distribution2(t_variable_value)
        t_value_distribution2 = test_feature_model['value_distribution2']
        outfile.write('Value Distribution2:\n')
        for t_path, t_variable_dict in t_value_distribution2.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable, t_distribution in t_variable_dict.items():
                outfile.write('\t\t%s:\n' % t_variable)
                for t_i, t_prop in enumerate(t_distribution):
                    outfile.write('\t\t\tP%d: %f\n' % (t_i, t_prop))

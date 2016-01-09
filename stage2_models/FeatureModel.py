"""
    It generate the features of the Host Model.
"""
from RecordBox import RecordBox

__author__ = 'j-lijiawei'


class FeatureModel:
    def __init__(self):
        """
            All features of the Host Model.

            Structure(dict):
                'path_element_prop': (self.__path_1element_prop, self.__path_2element_prop)
                'para_special_symbols': self.__para_special_symbols
        """
        self.__model_feature_all = dict()

        # Path Probability Status = (path_1element_prop, path_2element_prop)
        self.__path_element_prop = (dict(), dict())

        self.__value_specialSymbol_prop = dict()
        self.__value_variable_enumeration = dict()
        self.__variable_composition_pool = dict()
        self.__variable_order_rule = dict()
        self.__value_length_distribution = dict()
        self.__value_distribution1 = dict()
        self.__value_distribution2 = dict()

    def generate_all_features(self, a_record_box):
        a_path_list = a_record_box["path_list"]
        a_variable_special_symbol = a_record_box["variable_specialSymbol"]
        a_variable_value = a_record_box["variable_value"]
        a_variable_composition = a_record_box["variable_composition"]
        a_variable_order = a_record_box["variable_order"]

        self.generate_path_element_prop(a_path_list)
        self.generate_value_special_symbol_prop(a_variable_special_symbol)
        self.generate_variable_enumeration(a_variable_value)
        self.generate_variable_composition_pool(a_variable_composition)
        self.generate_variable_order_rule(a_variable_order)
        self.generate_value_length_distribution(a_variable_value)
        self.generate_value_distribution1(a_variable_value)
        self.generate_value_distribution2(a_variable_value)

    def generate_path_element_prop(self, path_list):
        """
        Path Probability Status:
            path element map to it's occurrence amount.

        self.__path_1element_prop = dict()
            {string: int} -> {'element_1': amount}
        self.__path_2element_prop = dict()
            {string: int} -> {'element_1,element_2': amount}
        :return:
        """
        pass
        return self.__path_element_prop

    def generate_value_special_symbol_prop(self, variable_special_symbol):
        pass
        # self.__value_specialSymbol_prop

    def generate_variable_enumeration(self, variable_value):
        pass
        # self.__value_variable_enumeration

    def generate_variable_composition_pool(self, variable_composition):
        pass
        # self.__variable_composition_pool

    def generate_variable_order_rule(self, variable_order):
        pass
        # self.__variable_order_rule

    def generate_value_length_distribution(self, variable_value):
        pass
        # self.__value_length_distribution

    def generate_value_distribution1(self, variable_value):
        pass
        # self.__value_distribution1

    def generate_value_distribution2(self, variable_value):
        pass
        # self.__value_distribution2

    # def __pathCellCount(self, path):
    #     tmp = path.split('/')
    #     length = len(tmp)
    #     for i in range(length):
    #         cell1 = tmp[i]
    #         if cell1 in self.__path_cell:
    #             self.__path_cell[cell1] += 1
    #         else:
    #             self.__path_cell[cell1] = 1
    #         if cell1 != 'PATH_END':
    #             cell2 = tmp[i + 1]
    #             cells = cell1 + ',' + cell2
    #             if cells in self.__2path_cells:
    #                 self.__2path_cells[cells] += 1
    #             else:
    #                 self.__2path_cells[cells] = 1

    def get_all_features(self):
        return self.__model_feature_all

    # def __paraStatusCount(self, para_status_dict):
    #     """
    #     Parameter Special Symbols Status:
    #         parameter element map to it's occurrence amount.
    #
    #     Structure:
    #         self.__para_special_symbols = {path_i: para_value_dict} or {path_i: {para_i : {value_i: count}}}
    #
    #         para_value_dict = {para_i: value_count_dict} or {para_i: {value_i: count}}
    #
    #         value_count_dict = {value_i: count}
    #
    #         **DRAW**
    #
    #                                     -- special_symbol_1 : count
    #                     -- variable_1   -- special_symbol_2 : count
    #                                     -- special_symbol_3 : count
    #                                     ...
    #                                     -- -SUM- : sum_count
    #
    #                                     -- special_symbol_1 : count
    #             path_i  -- variable_2   -- special_symbol_2 : count
    #                                     -- special_symbol_3 : count
    #                                     ...
    #                                     -- -SUM- : sum_count
    #
    #                                     -- special_symbol_1 : count
    #                     -- variable_3   -- special_symbol_2 : count
    #                                     -- special_symbol_3 : count
    #                                     ...
    #                                     -- -SUM- : sum_count
    #
    #     :param para_status_dict:
    #     :return:
    #     """
    #     path = para_status_dict['path']
    #     # {variable1 : {value1: count, value2:count2, ...}, variable2: {value1:count ...}}
    #     para_value_dict = self.__path_para_dict.setdefault(path, {})
    #     # {variable1: value, variable2: value ...} or 'NOT_EXIST'
    #     var_value_dict = para_status_dict['para']
    #     if var_value_dict != 'NOT_EXIST':
    #         for variable, special_symbols_set in var_value_dict.items():
    #             value_count_dict = para_value_dict.setdefault(variable, {})
    #             # {value1: count, value2: count2 ..., '-SUM-': ...}
    #             value_count_dict['-SUM-'] = value_count_dict.get('-SUM-', 0) + 1
    #             for special_symbol in special_symbols_set:
    #                 value_count_dict[special_symbol] = value_count_dict.get(special_symbol, 0) + 1

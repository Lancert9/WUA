"""
    Class RecordBox:
        It contains all training records corresponding to a single hosts.
        It also contains some metrics of records.

"""
__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

special_symbols_list = set(list("""~`!@#$%^&*()+={}[]|\:;"'<>,./?"""))


class RecordBox:
    def __init__(self):
        self.__all_records = list()
        self.__sip_box = set()

        # [path]
        self.__path_list = list()

        # {path: {variable: {specialSymbol: count}}}
        self.__variable_specialSymbol = dict()

        # {path: {variable: [value]}}
        self.__variable_value = dict()

        # {path: set(set(v1, v2, v3), set(v1, v4), ...)}
        self.__variable_composition = dict()

        # {path: set((v1, v2, v3), (v1, v4), ...)}
        self.__variable_order = dict()

        # It map the private attribute string to it's value
        self.__attribute_map = {}

    def add_record(self, a_record):
        self.__all_records.append(a_record)
        a_sip = a_record["sip"]
        self.__sip_box.add(a_sip)

    def active(self):
        """
        Active it to generate:
            1. self.__path_list
            2. self.__variable_specialSymbol
            3. self.__variable_value
            4. self.__variable_composition
            5. self.__variable_order
        """
        for record in self.__all_records:
            # add path segment
            # add it to path_list
            path = record["path"]
            self.__path_list.append(path)

            # add para segment
            para = record["para"]
            # if this url has parameter segment
            if para != "":
                para_seg = para.split('&')
                variable_list = list()
                for seg in para_seg:
                    variable, value = seg.split('=', 1)
                    variable_list.append(variable)
                    # add it to variable_value
                    if path in self.__variable_value:
                        if variable in self.__variable_value[path]:
                                self.__variable_value[path][variable].append(value)
                        else:
                            self.__variable_value[path][variable] = [value]
                    else:
                        self.__variable_value[path] = {variable: [value]}

                    # add it to variable_specialSymbol
                    if path in self.__variable_specialSymbol:
                        if variable in self.__variable_specialSymbol[path]:
                            for char in value:
                                if char in special_symbols_list:
                                    self.__variable_specialSymbol[path][variable][char] = \
                                        self.__variable_specialSymbol[path][variable].setdefault(char, 0) + 1
                        else:
                            self.__variable_specialSymbol[path][variable] = {}
                            for char in value:
                                if char in special_symbols_list:
                                    self.__variable_specialSymbol[path][variable][char] = \
                                        self.__variable_specialSymbol[path][variable].setdefault(char, 0) + 1
                    else:
                        self.__variable_specialSymbol[path] = {variable: {}}
                        for char in value:
                                if char in special_symbols_list:
                                    self.__variable_specialSymbol[path][variable][char] = \
                                        self.__variable_specialSymbol[path][variable].setdefault(char, 0) + 1

                # add it to variable_composition
                if path not in self.__variable_composition:
                    self.__variable_composition[path] = set()
                self.__variable_composition[path].add(frozenset(variable_list))

                # add it to variable_order
                if path not in self.__variable_order:
                    self.__variable_order[path] = set()
                self.__variable_order[path].add(tuple(variable_list))

        # generate the attribute map
        self.__generate_attribute_map()

    def clear(self):
        pass

    def __setitem__(self, key, value):
        raise LookupError("It is not allow to set the attribute.")

    def __getitem__(self, item):
        return self.__attribute_map[item]

    def __generate_attribute_map(self):
        self.__attribute_map["record_num"] = len(self.__all_records)
        self.__attribute_map["sip_num"] = len(self.__sip_box)
        self.__attribute_map["path_list"] = self.__path_list
        self.__attribute_map["variable_specialSymbol"] = self.__variable_specialSymbol
        self.__attribute_map["variable_value"] = self.__variable_value
        self.__attribute_map["variable_composition"] = self.__variable_composition
        self.__attribute_map["variable_order"] = self.__variable_order

if __name__ == '__main__':
    from stage2_models.UrlRecord import UrlRecord
    test_record_box = RecordBox()
    with open('E:\\Lancer\\360WUA\\WUA_data_container\\Flow\\Demo\\flow_20s', 'rb') as infile:

        for line in infile:
            line = line.strip(' \n').split('\t')
            if len(line) == 13 and line[_host] != '':
                t_record = UrlRecord(line)
                test_record_box.add_record(t_record)
    print 'Record add finished.'
    test_record_box.active()

    with open('E:\\Lancer\\360WUA\\WUA_data_container\\Flow\\Demo\\test_recordBox', 'wb') as outfile:
        # sip_num = test_record_box["sip_num"]
        # outfile.write("Sip_Num: %d\n" % sip_num)

        # path_list = test_record_box['path_list']
        # outfile.write("Path list:\n")
        # for i, t_path in enumerate(path_list):
        #     outfile.write("\t%d: %s\n" % (i, t_path))

        # variable_specialSymbol = test_record_box['variable_specialSymbol']
        # outfile.write('Variable_SpecialSymbol:\n')
        # for t_path, t_variable_dict in variable_specialSymbol.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable, t_specialSymbols_dict in t_variable_dict.items():
        #         outfile.write('\t\t%s:\n' % t_variable)
        #         for t_specialSymbols, t_count in t_specialSymbols_dict.items():
        #             outfile.write('\t\t\t%s:\t%d\n' % (t_specialSymbols, t_count))

        # variable_value = test_record_box['variable_value']
        # outfile.write('Variable_Value:\n')
        # for t_path, t_variable_dict in variable_value.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable, t_value_list in t_variable_dict.items():
        #         outfile.write('\t\t%s:\n' % t_variable)
        #         for t_value in t_value_list:
        #             outfile.write('\t\t\t%s\n' % repr(t_value))

        variable_composition = test_record_box['variable_composition']
        outfile.write('Variable_Composition:\n')
        for t_path, t_variable_composition_set in variable_composition.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable_composition in t_variable_composition_set:
                outfile.write('\t\t%s:\n' % t_variable_composition)

        # variable_order = test_record_box['variable_order']
        # outfile.write('Variable_Order:\n')
        # for t_path, t_variable_order_set in variable_order.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable_order in t_variable_order_set:
        #         outfile.write('\t\t%s:\n' % repr(t_variable_order))

"""
    Class RecordBox:
        It contains all training records corresponding to a single hosts.
        It also contains some metrics of records.

"""
from __future__ import division

__author__ = 'j-lijiawei'

(_access_time, _sip, _sport, _dip, _dport, _method, _uri, _host, _origin, _cookie, _uagent, _refer, _data) = range(13)

special_symbols_list = set(list("""~`!@#$%^&*()+={}[]|\:;"'<>,./?"""))


class RecordBox:
    def __init__(self):
        self.__all_records = list()
        self.__sip_box = set()

        # It map the private attribute string to it's value
        self._m = dict()

        # [path]
        self._m["path_list"] = list()
        self._m["path_set"] = set()

        # {path: {variable: {specialSymbol: count}}}
        self._m["variable_specialSymbol"] = dict()

        # {path: {variable: [value]}}
        self._m["variable_value"] = dict()

        # {path: set(set(v1, v2, v3), set(v1, v4), ...)}
        self._m["variable_composition"] = dict()

        # {path: set((v1, v2, v3), (v1, v4), ...)}
        self._m["variable_order"] = dict()

    def add_record(self, a_record):
        self.__all_records.append(a_record)
        self.__sip_box.add(a_record["sip"])

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
            path = record['path']
            self._m["path_list"].append(path)

            # add para segment
            para = record['para']
            variable_list = list()
            if para:
                para_seg = para.split('&')
                for seg in para_seg:
                    variable_value = seg.split('=', 1)
                    if len(variable_value) == 1:
                        variable = 'Default_Variable'
                        value = variable_value[0]
                    else:
                        variable, value = variable_value
                    variable_list.append(variable)
                    # add it to variable_value
                    if path in self._m["variable_value"]:
                        if variable in self._m["variable_value"][path]:
                                self._m["variable_value"][path][variable].append(value)
                        else:
                            self._m["variable_value"][path][variable] = [value]
                    else:
                        self._m["variable_value"][path] = {variable: [value]}

                    # add it to variable_specialSymbol
                    if path not in self._m["variable_specialSymbol"]:
                        self._m["variable_specialSymbol"][path] = {variable: {}}
                        self._m["variable_specialSymbol"][path][variable]['SUM'] = 0
                    else:
                        if variable not in self._m["variable_specialSymbol"][path]:
                            self._m["variable_specialSymbol"][path][variable] = {}
                            self._m["variable_specialSymbol"][path][variable]['SUM'] = 0
                    for char in value:
                        if char in special_symbols_list:
                            self._m["variable_specialSymbol"][path][variable][char] = \
                                self._m["variable_specialSymbol"][path][variable].setdefault(char, 0) + 1
                            self._m["variable_specialSymbol"][path][variable]['SUM'] += 1

                # add it to variable_composition
                if path not in self._m["variable_composition"]:
                    self._m["variable_composition"][path] = set()
                self._m["variable_composition"][path].add(frozenset(variable_list))

                # add it to variable_order
                if path not in self._m["variable_order"]:
                    self._m["variable_order"][path] = set()
                self._m["variable_order"][path].add(tuple(variable_list))

        self._m['path_set'] = set(self._m["path_list"])

    def __setitem__(self, key, value):
        raise LookupError("It is not allow to set the attribute.")

    def __getitem__(self, key):
        if key == 'record_num':
            return len(self.__all_records)
        elif key == 'sip_num':
            return len(self.__sip_box)
        else:
            return self._m[key]

if __name__ == '__main__':
    from FlowRecord import FlowRecord
    test_record_box = RecordBox()
    with open('E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\'
              'flow_mall.360.com_20151231_31\\flow_input', 'rb') as infile:

        for line in infile:
            line = line.strip(' \n').split('\t')
            if len(line) == 13 and line[_host] != '':
                t_record = FlowRecord(line)
                test_record_box.add_record(t_record)
    print 'Record add finished.'
    test_record_box.active()

    with open('E:\\WUA_data_container\\data_container\\Skyeye_Sensor\\FLow\\'
              'flow_mall.360.com_20151231_31\Demo\\test_recordBox', 'wb') as outfile:
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

        t_variable_value = test_record_box['variable_value']
        outfile.write('Variable_Value:\n')
        for t_path, t_variable_dict in t_variable_value.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable, t_value_list in t_variable_dict.items():
                outfile.write('\t\t%s:\n' % t_variable)
                for t_value in t_value_list:
                    outfile.write('\t\t\t%s\n' % repr(t_value))

        # variable_composition = test_record_box['variable_composition']
        # outfile.write('Variable_Composition:\n')
        # for t_path, t_variable_composition_set in variable_composition.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable_composition in t_variable_composition_set:
        #         outfile.write('\t\t%s:\n' % t_variable_composition)

        # variable_order = test_record_box['variable_order']
        # outfile.write('Variable_Order:\n')
        # for t_path, t_variable_order_set in variable_order.items():
        #     outfile.write('\t%s:\n' % t_path)
        #     for t_variable_order in t_variable_order_set:
        #         outfile.write('\t\t%s:\n' % repr(t_variable_order))

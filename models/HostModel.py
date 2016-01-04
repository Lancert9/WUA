"""
    Class HostModel:
        The model of a specific host.
"""
from PatternController import PatternController
import CalProp
import heapq


__author__ = 'j-lijiawei'


class HostModel:
    def __init__(self, host_name=''):
        """
        :param host_name: str -- the host of this HostModel.

        """
        """
            Model Status
        """
        self.__hostname = host_name     # The host of this host model
        self.__pattern_controller = PatternController()     # Determine when to calculate the whole model
        self.__records = {}    # @item: a record map to it's amount
        self.__url_amount = 0   # total amount of records which are related to this host
        self.__sips = set()     # contain the different sips
        self.__detect_flag = 'Study...'
        """
            Path Status
        """
        # @item: a string(e.g. A) map to [Amount, Verbs], Amount means the total amount of A,
        # Verbs means the different type of strings(A or B or C...) next to A
        self.__path_cell = {}   # @item: a string(a part of path) map to it's amount
        self.__2path_cells = {}  # @item: a string(two adjacent part) map to it's amount
        self.__model_path_props = []    # @item: the probability of a record's path in this host model
        self.__path_per2threshold = {}  # @item: the detection percentage map to path probability threshold
        """
            Parameter Status:
                __path_para_dict dictionary:
                    {path_i: para_value_dict} or
                    {path_i: [{para_i : {value_i: count}}]}
                para_value_dict dictionary:
                    {para_i: value_count_dict} or
                    {para_i: {value_i: count}}
                value_count_dict dictionary:
                    {value_i: count}
                draw structure:

                                            -- special_symbol_1 : count
                            -- variable_1   -- special_symbol_2 : count
                                            -- special_symbol_3 : count
                                            ...
                                            -- -SUM- : sum_count

                                            -- special_symbol_1 : count
                    path_i  -- variable_2   -- special_symbol_2 : count
                                            -- special_symbol_3 : count
                                            ...
                                            -- -SUM- : sum_count

                                            -- special_symbol_1 : count
                            -- variable_3   -- special_symbol_2 : count
                                            -- special_symbol_3 : count
                                            ...
                                            -- -SUM- : sum_count
        """
        self.__path_para_dict = {}

    def __pathCellCount(self, path):
        tmp = path.split('/')
        length = len(tmp)
        for i in range(length):
            cell1 = tmp[i]
            if cell1 in self.__path_cell:
                self.__path_cell[cell1] += 1
            else:
                self.__path_cell[cell1] = 1
            if cell1 != 'PATH_END':
                cell2 = tmp[i + 1]
                cells = cell1 + ',' + cell2
                if cells in self.__2path_cells:
                    self.__2path_cells[cells] += 1
                else:
                    self.__2path_cells[cells] = 1

    def __calModelProp(self):
        self.__model_path_props = CalProp.calPathProp_modi(self.__records, self.__path_cell, self.__2path_cells)

    def __calModelPathT(self, per):
        number = int(per * len(self.__model_path_props))
        __path_threshold = heapq.nsmallest(number, self.__model_path_props)[-1]
        return __path_threshold

    def __paraStatusCount(self, para_status_dict):
        path = para_status_dict['path']
        # {variable1 : {value1: count, value2:count2, ...}, variable2: {value1:count ...}}
        para_value_dict = self.__path_para_dict.setdefault(path, {})
        # {variable1: value, variable2: value ...} or 'NOT_EXIST'
        var_value_dict = para_status_dict['para']
        if var_value_dict != 'NOT_EXIST':
            for variable, special_symbols_set in var_value_dict.items():
                value_count_dict = para_value_dict.setdefault(variable, {})
                # {value1: count, value2: count2 ..., '-SUM-': ...}
                value_count_dict['-SUM-'] = value_count_dict.get('-SUM-', 0) + 1
                for special_symbol in special_symbols_set:
                    value_count_dict[special_symbol] = value_count_dict.get(special_symbol, 0) + 1

    def __writeModelRecords(self):
        host_url_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Host\\%s_urls' % self.__hostname
        with open(host_url_address, 'wb') as outfile:
            for record in self.__records:
                url = record.get_url()
                outfile.write('%s\n' % url)
            outfile.flush()

    def __writeParaProp(self):
        host_para_prop_address = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Host\\%s_para_prop' % self.__hostname
        with open(host_para_prop_address, 'wb') as outfile:
            for record in self.__records:
                path = record.get_path_code()
                outfile.write("PATH: %s\n" % path)
                # {variable_i : {special_symbols_i: count, -SUM-: sum_count}}
                para_value_dict = self.__path_para_dict.get(path, {})
                for variable, special_symbol_count_dict in para_value_dict.items():
                    outfile.write("\t%s:\n" % variable)
                    for special_symbol, count in special_symbol_count_dict.items():
                        outfile.write("\t\tspecial_symbol: %s count: %s\n" % (special_symbol, count))
            outfile.flush()

    def addUrl(self, a_record):
        """
        When adding a UrlRecord, it is need to count this record's attribute to the HostModel.
        :param a_record: UrlRecord
        """
        # count new record into the host model
        if a_record in self.__records:
            self.__records[a_record] += 1
        else:
            self.__records[a_record] = 1
        self.__url_amount += 1
        sip = a_record.get_sip()
        self.__sips.add(sip)

        # add new record's path into model's path status
        a_path = a_record.get_path_code()
        self.__pathCellCount(a_path)

        # add new record's parameter into model's parameter status
        a_para_status_dict = a_record.get_para_status()
        self.__paraStatusCount(a_para_status_dict)

        pattern_flag = self.__pattern_controller.judgePattern(self)
        if pattern_flag == 'Anomaly detection':
            print "Model is Ready. Begin to detecting..."
            self.__detect_flag = 'Study ready'
            self.__calModelProp()
            # self.__writeModelRecords()
            # self.__writeParaProp()

    def calSinglePathProp(self, a_record):
        """
        get the probability of a UrlRecord's url path.
        :param a_record: UrlRecord
        :return: dict --> {str: float} -- url's encoded path map to it's probability.
        """
        a_path_prop = CalProp.calPathProp({a_record: 1}, self.__path_cell, self.__2path_cells)[0]
        a_path_code = a_record.get_path_code()
        return {a_path_code: a_path_prop}

    def calSinglePathProp_modi(self, a_record):
        """
        get the probability of a UrlRecord's url path by the modification-way.
        :param a_record: UrlRecord
        :return: dict --> {str: float} -- url's encoded path map to it's probability.
        """
        a_path_prop = CalProp.calPathProp_modi({a_record: 1}, self.__path_cell, self.__2path_cells)[0]
        a_path_code = a_record.get_path_code()
        return {a_path_code: a_path_prop}

    def getModelPathT(self, percentage):
        """
        Depending on the given percentage, get the HostModel's probability threshold of url path.
        This threshold is used for anomaly detection.
        :param percentage: float
        :return: float
        """
        if percentage in self.__path_per2threshold:
            return self.__path_per2threshold[percentage]
        else:
            threshold = self.__calModelPathT(percentage)
            self.__path_per2threshold[percentage] = threshold
            return threshold
        # return self.__path_per2threshold.setdefault(percentage, self.__calModelPathT(percentage))

    def detectSingleParaProp(self, a_record, a_threshold):
        """
        Depending on the UrlRecord's parameter field and a given threshold, HostModel detects whether it is a anomaly.
        :param a_record: UrlRecord
        :param a_threshold: float
        :return: dict --> {str: str} -- the detection result and it's reason.
        """
        para_prop_result = CalProp.detectParaProp(a_record, self.__path_para_dict, a_threshold)
        return para_prop_result

    def getUrlAmount(self):
        """
        get the number of UrlRecords that this HostModel has been studied.
        :return: int
        """
        return self.__url_amount

    def getDifUrlAmount(self):
        """
        get the number of different UrlRecords that this HostModel has been studied.
        :return:
        """
        return len(self.__records)

    def getSipAmount(self):
        """
        get the number of different sip field that this HostModel has been studied.
        :return:
        """
        return len(self.__sips)

    def getHostName(self):
        """
        get the host field of this HostModel.
        :return:
        """
        return self.__hostname

    def getDetectFlag(self):
        """
        If this HostModel's study process is over and it is ready to detect,
        this function return 'Study ready', otherwise it return 'Study...'.
        :return: str
        """
        return self.__detect_flag

    def getRecords(self):
        return self.__records

    def getModelPathProps(self):
        return self.__model_path_props

    def getModePathPropsThreshold(self):
        return self.__path_per2threshold

    def __str__(self):
        """
        :return:s
        """
        return "model's url-amount is:\t%d" % self.__url_amount

if __name__ == '__main__':
    HM = HostModel()
    ppd = {'XiAn': {'name': {'LJW': 2, 'Lan': 1}, 'year': {'24': 3, '12': 4}}, 'BeiJing': {'Sport': {'Football': 3}}}
    HM.path_para_dict = ppd
    pvd_1 = {'path': 'XiAn', 'para': {'name': 'Lancer', 'year': '12', 'Like': 'Ball'}}
    pvd_2 = {'path': 'YuXia', 'para': {'people': 'NieBin'}}
    HM.paraStatusCount(pvd_1)
    HM.paraStatusCount(pvd_2)
    print HM.path_para_dict

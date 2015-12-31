"""
    Calculate kinds of function's cost time.
"""

from datetime import datetime

__author__ = 'j-lijiawei'


def func_1(values_input):
    begin_time = datetime.now()
    diff_list = []
    for k in range(100000):
            diff_list = []
            values_set = set()
            length = len(values_input)
            for i in xrange(length):
                values_set.add(values_input[i])
                diff_list.append(len(values_set))

    print diff_list
    end_time = datetime.now()
    print end_time - begin_time


def func_2(values_input):
    begin_time = datetime.now()
    diff_list = []
    for k in range(100000):
            diff_list = []
            values_set = set()
            length = len(values_input)
            count = 0
            for i in xrange(length):
                temp = values_input[i]
                if temp not in values_set:
                    values_set.add(temp)
                    count += 1
                diff_list.append(count)

    print diff_list
    end_time = datetime.now()
    print end_time - begin_time

if __name__ == '__main__':
    func_1([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    func_2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

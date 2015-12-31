# -*- coding=utf-8 -*-
from pandas import Series

__author__ = 'j-lijiawei'


def cal_chebyshev(a_num, a_mean, a_var):
    if a_num <= a_mean:
        return 1
    else:
        """
        P(x - μ > ε) <= 1 / (1 + (ε^2) / D(x))
        """
        epsilon2 = (a_num - a_mean) ** 2

        return 1 / (1 + epsilon2 / a_var)

if __name__ == '__main__':
    input_list = [1, 2, 3, 4, 5]
    data = Series(input_list)
    mean = data.mean()
    var = data.var()
    print "mean: %f" % mean
    print "var: %f" % var

    for x in range(10):
        prop = cal_chebyshev(x, mean, var)
        print "%s: %f" % (x, prop)

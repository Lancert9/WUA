from pandas import Series
from pandas import DataFrame

__author__ = 'j-lijiawei'

"""         x1  x2  x3
    A = [
            1   2   2
            2   3   1
            3   3.5 0.5
        ]

    calculate var, cov, corr, cov-matrix, corr-matrix
"""

data = {'x1': [1, 2], 'x2': [2, 3], 'x3': [2, 1]}
A = DataFrame(data)
print A

data1 = Series([3, 3.5, 0.5], index=['x1', 'x2', 'x3'])
A = A.append(data1, ignore_index=True)
print '\n', A, '\n'

var_x1 = A['x1'].var()
var_x2 = A['x2'].var()
var_x3 = A['x3'].var()

print 'var_x1: %f' % var_x1
print 'var_x2: %f' % var_x2
print 'var_x3: %f' % var_x3

cov_matrix = A.cov()
print '\ncov_matrix:\n', cov_matrix

corr_matrix = A.corr()
print '\ncorr_matrix:\n', corr_matrix

print "\nA['x1'].corr(A['x2']): %f" % A['x1'].corr(A['x2'])
print "A['x1'].corr(A['x3']): %f" % A['x1'].corr(A['x3'])

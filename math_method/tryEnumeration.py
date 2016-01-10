"""
    Judging the parameter whether is enumerated type or not.
"""
from pandas import DataFrame

__author__ = 'j-lijiawei'


def is_enumerated(values_input):
    """
    To judge the parameter variable is enumerated or not.
    :param values_input: the parameter's value list.
    :return: True if the parameter is enumerated type. Otherwise, return False.
    """
    length = len(values_input)
    all_list = range(1, length + 1)

    diff_list = []
    values_set = set()
    count = 0
    for i in range(length):
        temp = values_input[i]
        if temp not in values_set:
            values_set.add(temp)
            count += 1
        else:
            count -= 1
        diff_list.append(count)

    all_dif_df = DataFrame({'all_values': all_list, 'diff_values': diff_list})
    all_dif_cor = all_dif_df['all_values'].corr(all_dif_df['diff_values'])
    print "Correlation is %s" % all_dif_cor

    return True if all_dif_cor < 0 else False


if __name__ == '__main__':
    index_str = 'Continue'
    while index_str != 'q':
        value_str = raw_input('Input a value list:\n')
        value_list = [num.strip() for num in value_str.split(',')]
        print 'Enumerated type is: %s' % (is_enumerated(value_list))
        index_str = raw_input("Quit to input 'q', others to continue.\n").lower()

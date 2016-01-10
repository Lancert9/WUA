"""
    Chi-squared test.
"""
from scipy.stats import chisquare


def chi_squared_test(obs, exp):
    """
    :param obs: observation sequences
    :param exp: exception sequences
    :return: P-value
    """
    return chisquare(obs, exp)[1]
    # print 'Chi-squared: %f' % chisq
    # print 'P-value: %s' % p


def icd_type1(obs_str, exp_pro):
    icd_list = [0] * 256
    for char in obs_str:
        ascll = ord(char)
        icd_list[ascll] += 1
    icd_list.sort(reverse=True)
    """
        ---------------------------------------------------------
         interval |  0     1      2      3        4        5
        ---------------------------------------------------------
           index  | (0)  (1-3)  (4-6)  (7-11)  (12-15)  (16-255)
        ---------------------------------------------------------
    """
    icd_table = [0] * 6
    icd_table[0] = sum([icd_list[i] for i in range(0, 1)])
    icd_table[1] = sum([icd_list[i] for i in range(1, 4)])
    icd_table[2] = sum([icd_list[i] for i in range(4, 7)])
    icd_table[3] = sum([icd_list[i] for i in range(7, 12)])
    icd_table[4] = sum([icd_list[i] for i in range(12, 16)])
    icd_table[5] = sum([icd_list[i] for i in range(16, 256)])

    length = len(obs_str)
    exp_table = map(lambda x: x * length, exp_pro)

    return icd_table, exp_table


def icd_type2(obs_str, exp_pro):
    """
        A char number is divided into 6 categories.
        1. uppercase    -->    (65-90)
        2. lowercase    -->    (97-122)
        3. digit        -->    (48-57)
        4. control      -->    (32-47, 58-64, 91-96, 123-126)
        5. unprintable  -->    (0-31, 127)
        6. extension    -->    (128-255)
    """
    uppercase_set = set(range(65, 91))

    lowercase_set = set(range(97, 123))

    digit_set = set(range(48, 58))

    control_list = list()
    map(lambda x: control_list.extend(x), (range(32, 48), range(58, 65), range(91, 97), range(123, 127)))
    control_set = set()
    map(lambda x: control_set.add(x), control_list)

    unprintable_set = set(range(32))
    unprintable_set.add(127)

    extension_set = set(range(128, 256))

    """
        -------------------------------------------------------------------------------------------------
         interval | uppercase  lowercase  digit              control              unprintable  extension
        -------------------------------------------------------------------------------------------------
           ASCII  |  (65-90)   (97-122)  (48-57)  (32-47, 58-64, 91-96, 123-126)  (0-31, 127)  (128-255)
        -------------------------------------------------------------------------------------------------
    """
    interval = [uppercase_set, lowercase_set, digit_set, control_set, unprintable_set, extension_set]
    icd_table = [0] * 6
    for char in obs_str:
        for index, category in enumerate(interval):
            if ord(char) in category:
                icd_table[index] += 1
                break

    length = len(obs_str)
    exp_table = map(lambda x: x * length, exp_pro)

    return icd_table, exp_table

if __name__ == '__main__':
    test_str = 'abade1234?'
    exp_p_1 = [0.1, 0.1, 0.15, 0.2, 0.3, 0.15]
    exp_p_2 = [0.1, 0.6, 0.2, 0.1, 0.00001, 0.00001]

    test_obs_1, test_exp_1 = icd_type1(test_str, exp_p_1)
    print "Test_1 observation: ", test_obs_1
    print "Test_1 exception: ", test_exp_1
    p_value = chi_squared_test(test_obs_1, test_exp_1)
    print "Test_1 P-value: ", p_value

    test_obs_2, test_exp_2 = icd_type2(test_str, exp_p_2)
    print "Test_2 observation: ", test_obs_2
    print "Test_2 exception: ", test_exp_2
    p_value = chi_squared_test(test_obs_2, test_exp_2)
    print "Test_2 P-value: ", p_value

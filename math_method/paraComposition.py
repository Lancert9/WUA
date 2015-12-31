"""
    Recording url's different parameter composition.
"""

__author__ = 'j-lijiawei'


def cal_para_composition(input_list):
    """
    To record url's different parameter composition.
    :param input_list:
    :return: a set --> the parameter composition result.
    """

    result_list = []
    for url in input_list:
        if '?' in url:
            paras_list = url.split('?', 1)[1].split('&')
            variable_compo = set()
            for para in paras_list:
                variable_compo.add(para.split('=')[0])
            if variable_compo not in result_list:
                result_list.append(variable_compo)
    return result_list


if __name__ == '__main__':
    url_list = list()
    url_list.append('xxx?a=1&b=2&c=3')
    url_list.append('xx?a=1&b=2&c=3')
    url_list.append('x?a=1&b=2')
    url_list.append('x?')
    url_list.append('xxx')
    url_list.append('xxx?d=2&c=2')
    print url_list
    para_composition_list = cal_para_composition(url_list)
    print para_composition_list

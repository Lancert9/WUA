__author__ = 'j-lijiawei'
from urllib import unquote

def paraTran(item):
    while True:
        item_uncode = unquote(item)
        if item_uncode == item:
            break
        item = item_uncode
    print item
    variable, value = item.split('=', 1)
    special_symbols_set = findSS(value)
    return special_symbols_set


def findSS(origin_s):
    special_symbols = set(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '{', '}', '[', ']', ',', '<', '>', '?', "'", '\\', '"', ':', ';', '='])
    special_symbols_list = set()
    for a_char in origin_s:
        if a_char in special_symbols:
            special_symbols_list.add(a_char)
    return special_symbols_list


def pathTran(path):
    while True:
        path_uncode = unquote(path)
        if path_uncode == path:
            break
        path = path_uncode
    print path
    path_list = []
    number_flag = False
    for a_char in path:
        if a_char.isdigit():
            if not number_flag:
                number_flag = True
                path_list.append('D')
        else:
            number_flag = False
            path_list.append(a_char)
    return ''.join(path_list)


if __name__ == '__main__':
    s = "id=2%20%7Cless%20/etc/passwd"
    paraTran(s)

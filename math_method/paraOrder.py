"""
    Recording the url's all fixed parameter order.
"""
import networkx as nx

__author__ = 'j-lijiawei'


def cal_para_order(para_list):
    """
    To record the parameter variable's all fixed order.
    :param para_list: the url's kinds of url's.
    :return: list -> all fixed parameter order.
    """
    result_order = list()

    order_collection = set()
    for order_seg in para_list:
        length = len(order_seg)
        for i in range(length - 1):
            order_collection.add((order_seg[i], order_seg[i + 1]))
    print 'G2:', sorted(list(order_collection))
    g = nx.DiGraph()
    g.add_edges_from(order_collection)
    connectivity_dict = dict([])
    for source_node, connect_dict in nx.all_pairs_node_connectivity(g).items():
        connectivity_dict[source_node] = []
        for target_node, hop in connect_dict.items():
            if hop > 0:
                connectivity_dict[source_node].append(target_node)
    print 'Connectivity_Original:', nx.all_pairs_node_connectivity(g)
    print 'Connectivity_dict:', connectivity_dict
    node_list = g.nodes()
    node_length = len(node_list)
    for i in range(node_length):
        for j in range(i + 1, node_length):
            node_1 = node_list[i]
            node_2 = node_list[j]
            connect_1_2 = node_2 in connectivity_dict[node_1]
            connect_2_1 = node_1 in connectivity_dict[node_2]
            if connect_1_2 and not connect_2_1:
                result_order.append((node_1, node_2))
            elif connect_2_1 and not connect_1_2:
                result_order.append((node_2, node_1))
            else:
                continue

    return result_order


if __name__ == '__main__':
    input_list = [(1, 2, 3), (2, 4), (5, 6), (6, 7), (7, 6)]
    para_sequence_result = cal_para_order(input_list)
    print "Fixed Order:", sorted(list(para_sequence_result))

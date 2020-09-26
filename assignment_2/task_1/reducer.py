#!/usr/bin/python3
"""reducer.py"""

import sys

curr_node = None

fptr = open('adj_list', 'a')

for line in sys.stdin:
    from_node, to_node = line.split("\t")
    if curr_node != from_node:
        if curr_node == None:
            node_adj_list = list()
            node_adj_list.append(to_node)
            curr_node = from_node
        else:
            fptr.write("%s\t[" % curr_node)
            for item in range(0,len(node_adj_list)):
                if item == len(node_adj_list)-1:
                    fptr.write("%s, " % item)
                else:
                    fptr.write("%s]" % item)
            node_adj_list = list()
            node_adj_list.append(to_node)
            curr_node = from_node
    else:
        if curr_node == None:
            pass
        elif curr_node == from_node:
            node_adj_list.append(to_node)

fptr.close()
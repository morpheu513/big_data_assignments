#!/usr/bin/python3
"""reducer.py"""

import sys

curr_node = None

v_file_path = sys.argv[1]

fptr_v_file = open(v_file_path, 'a')

for line in sys.stdin:
    from_node, to_node = line.split("\t")
    to_node = to_node.rstrip("\n")
    if curr_node != from_node:
        if curr_node == None:
            node_adj_list = list()
            node_adj_list.append(to_node)
            curr_node = from_node
        else:
            print(curr_node,"  ",node_adj_list,"\n")
            fptr_v_file.write("%s\t1\n" % curr_node)
            node_adj_list = list()
            node_adj_list.append(to_node)
            curr_node = from_node
    elif curr_node == from_node:
        node_adj_list.append(to_node)

if(curr_node == from_node):
    print(curr_node,"\t",node_adj_list,"\n")

#!/usr/bin/python3
"""reducer.py"""

import sys

curr_node = None

v_file_path = sys.argv[1]

fptr_v_file = open(v_file_path, 'a')

for line in sys.stdin:
    from_node,to_node = line.split()
    from_node.rstrip()
    if curr_node != from_node:
        if curr_node == None:
            node_adj_list = list()
            node_adj_list.append(to_node)
            curr_node = from_node
        else:
            print(curr_node,"\t",end="")
            for i in range(0,len(node_adj_list)):
                if i == len(node_adj_list) - 1:
                    print(node_adj_list[i])
                else:
                    print(node_adj_list[i],end=",")
            fptr_v_file.write("%s,1\n" % curr_node)
            node_adj_list = list()
            node_adj_list.append(to_node)
            curr_node = from_node
    elif curr_node == from_node:
        node_adj_list.append(to_node)

if(curr_node == from_node):
    print(curr_node,"\t",end="")
    for i in range(0,len(node_adj_list)):
        if i == len(node_adj_list) - 1:
            print(node_adj_list[i])
        else:
            print(node_adj_list[i],end=",")
    fptr_v_file.write("%s,1\n" % curr_node)

fptr_v_file.close()
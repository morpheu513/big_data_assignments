#!/usr/bin/python3
"""reducer.py"""

import sys

curr_node = None
#NOTE, CASE WITH LIKE MISSING NODES IN MIDDLE NOT TAKEN CARE OF, i.e if it has page rank zero
nodeVal = 0

v_file_path = sys.argv[1]

fptr_v_file = open(v_file_path, 'a')

for line in sys.stdin:
    node, partRank = line.split(" ")
    partRank = partRank.rstrip("\n")
    if curr_node != node:
        if curr_node == None:
            nodeVal+=int(partRank)
            curr_node = node
        else:
            currRank=0.15+0.85*partRank
            print(node,"  ",currRank,"\n")
            #fptr_v_file.write("%s\t1\n" % curr_node)   Dont know what to do here
            nodeVal=0
            nodeVal+=int(partRank)
            curr_node = node
    elif curr_node == node:
        nodeVal+=int(partRank)

#if(curr_node == from_node):
    #print(curr_node,"\t",node_adj_list,"\n") Dont know what these two do either



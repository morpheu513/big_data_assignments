#!/usr/bin/python3
"""reducer.py"""

import sys
curr_node = None
for line in sys.stdin:
	from_node,to_node = line.split()
	to_node=float(to_node)
	from_node.rstrip()
	if curr_node != from_node:
		if curr_node == None:
			node_adj_list = list()
			node_adj_list.append(to_node)
			curr_node = from_node
		else:
			final_pr=0.15 + (0.85*sum(node_adj_list))
			print(curr_node,",","%.5f" % final_pr)
			node_adj_list = list()
			node_adj_list.append(to_node)
			curr_node = from_node
	elif curr_node == from_node:
		node_adj_list.append(to_node)

if(curr_node == from_node):
	final_pr=0.15+(0.85*sum(node_adj_list))
	print(curr_node,",","%.5f" % final_pr)




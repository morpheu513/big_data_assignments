#!/usr/bin/python3
"""
reducer.py
This file contains the code for the reducer which is used in task 2
"""

import sys

curr_node = None

for line in sys.stdin:
	
	node,contribution = line.split()
	contribution=float(contribution)
	node.rstrip()
	
	if curr_node != node:
		if curr_node == None:
			node_contribution_list = list()
			node_contribution_list.append(contribution)
			curr_node = node
		else:
			final_pr = 0.15 + (0.85*sum(node_contribution_list))
			print(curr_node,"%.5f" % final_pr,sep=",")
			node_contribution_list = list()
			node_contribution_list.append(contribution)
			curr_node = node
	
	elif curr_node == node:
		node_contribution_list.append(contribution)

if(curr_node == node):
	final_pr = 0.15 + (0.85*sum(node_contribution_list))
	print(curr_node,"%.5f" % final_pr,sep=",")




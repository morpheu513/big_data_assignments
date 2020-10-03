#!/usr/bin/python3
"""
mapper.py
This file contains the code for the mapper which is used in task 2
"""

import sys


var = sys.argv[1]

f=open(var,'r')
my_dict={}

for i in f:
	a=i.split(",")
	my_dict.update({a[0]:a[1].strip()})

for line in sys.stdin:
	ip = line.split("\t")
	
	if len(ip) > 1 and ip[1] != '\n':
		
		ip[0] = ip[0].rstrip()
		ip[1] = ip[1].rstrip("\n")
		adj_list = ip[1].split(",")
		length = len(adj_list)
		print(ip[0],"\t",0)
		
		for i in adj_list:
			if i in my_dict.keys():
				print(i,"\t",float(my_dict[ip[0]])/length)
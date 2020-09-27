#!/usr/bin/python3
"""mapper.py"""

import sys
import re

var = sys.argv[1]
#change value to 0 afterwards
f=open(var,'r')
my_dict={}
for i in f:
	a=i.split(",")
	my_dict.update({a[0]:a[1].strip()})

for line in sys.stdin:
	ip = line.split("\t")
	if len(ip) > 1:
		ip[1] = ip[1].rstrip("\n")
		adj_list = ip[1].split(",")
		length = len(adj_list)
		for i in adj_list:
			print(i,"\t",float(my_dict[i])/length)

#!usr/bin/python3
"""mapper.py"""

import sys
v_list_path=sys.argv[0]
v_ptr=open(v_list_path,'r')

x=v_ptr.readlines().split(",")
xDict={x[1]:x[0]}

for line in sys.stdin:
	ip=line.split("\t")
	node=ip[0]
	plist=list(ip[1])
	for i in plist:
		print(i,"\t",xDict[i]/len(plist))

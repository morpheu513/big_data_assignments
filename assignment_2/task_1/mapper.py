#!/usr/bin/python3
"""mapper.py"""

import sys

curr_node = None

fptr = open('v', 'a')

for line in sys.stdin:
    ip = line.split()
    from_node = ip[0]
    to_node = ip[1]
    if curr_node != from_node:
        fptr.write("%s,\t1\n" % from_node)
        curr_node = from_node
    print(from_node,"\t",to_node)

fptr.close()
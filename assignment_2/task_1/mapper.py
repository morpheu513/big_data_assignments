#!/usr/bin/python3
"""mapper.py"""

import sys

curr_node = None

for line in sys.stdin:
    ip = line.split()
    from_node = ip[0]
    to_node = ip[1]
    if from_node != '#' and from_node != to_node:
        print(from_node,"\t",to_node)

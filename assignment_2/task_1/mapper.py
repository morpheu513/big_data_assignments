#!/usr/bin/python3
"""
mapper.py
This file contains the code for the mapper which is used in task 1
"""

import sys

curr_node = None

for line in sys.stdin:
    ip = line.split()

    if(len(ip) == 2):
        from_node = ip[0]
        to_node = ip[1]
        if from_node != '#':
            print(from_node,"\t",to_node)
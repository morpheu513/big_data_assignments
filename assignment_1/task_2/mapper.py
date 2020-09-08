#!/usr/bin/python3
"""mapper.py"""

import datetime
import json
import sys
import re


# Function to check if a record is bad or not
def isValid(record):
    wo = record['word']
    cc = record['countrycode']
    re = record['recognized']
    ki = record['key_id']
    dr = record['drawing']

    if not all(x.isalpha() or x.isspace() for x in wo):
        return False
    
    if not (cc.isupper() and len(cc)==2):
        return False

    if not (str(re)=='True' or str(re)=='False'):
        return False

    if not (ki.isdecimal() and len(ki)==16):
        return False
    
    if len(dr) < 1:
        return False

    for arr in dr:
        if len(arr)!=2:
            return False
    
    return True

var = sys.argv[1]
k = int(sys.argv[2])

for line in sys.stdin:
    airplane_record = json.loads(line)
    if (isValid(airplane_record)):
        if airplane_record['word']==var:
            dr = airplane_record['drawing']
            x0 = dr[0][0][0]
            y0 = dr[0][1][0]
            if ((x0**2 + y0**2)**0.5 > k):
                print('%s\t%s' % (airplane_record['countrycode'],1))
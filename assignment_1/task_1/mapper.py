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

for line in sys.stdin:
    record = json.loads(line)
    if (isValid(record)):
        if record['word']==var:
            if str(record['recognized'])=='True':
                print('%s\t%s' % ('recognized', 1))

            else:
                year=int(record['timestamp'][0:4])
                month=int(record['timestamp'][5:7])
                day=int(record['timestamp'][8:10])
                currDate=datetime.datetime(year, month, day)
                dayNo=currDate.weekday()
                if dayNo>4:
                    print('%s\t%s' % ('unrecognized', 1))
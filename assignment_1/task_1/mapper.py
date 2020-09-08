#!/usr/bin/python
"""mapper.py"""

import datetime
import json
import sys
var="airplane"
#current variable for input is var

# Function to check if a record is bad or not
def isValid(airplane_record):
    wo = airplane_record['word']
    cc = airplane_record['countrycode']
    re = airplane_record['recognized']
    ki = airplane_record['key_id']
    dr = airplane_record['drawing']

    if not all(x.isalpha() or x.isspace() for x in wo):
        #print("fail 1")
        return False
    if not (cc.isupper() and len(cc)==2):
        #print("fail 2")
        return False
    if not (str(re)=='True' or str(re)=='False'):
        #print("fail 3")
        #print(str(re));

        return False
    if not (ki.isdecimal() and len(ki)==16):
        #print("fail 4")

        return False
    if len(dr) < 1:
        #print("fail 5")

        return False
    for arr in dr:
        if len(arr)!=2:
            #print("fail 6")

            return False
    return True


for line in sys.stdin:
    airplane_record = json.loads(line)
    if (isValid(airplane_record)):
        if airplane_record['word']==var:
            if str(airplane_record['recognized'])=='True':
                print('%s\t%s' % (var, 1))
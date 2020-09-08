#!/usr/bin/python3
"""reducer.py"""

import sys

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # parse the input we got from mapper.py
    word, count= line.split('\t', 1)

    # convert count (currently a string) to int
    count = int(count)

    # this IF-switch only works because Hadoop sorts map output
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # writing result to STDOUT
            print('%s' % (current_count))
        current_count = count
        current_word = word

# write output for last word
if current_word == word:
    print('%s' % (current_count))

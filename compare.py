#!/usr/bin/python
#
# Fast key compare script. Accepts newline-delimited lists of hex encoded
# 160 bit keys. This will report keys NOT found in the haystak. Meaning keys
# that are found in "ringkeys" that are NOT found in "haystack".
# Unless you use the --inclusive flag, which will report keys that are found
# in both lists.
#
# WARNING: it reads the lists into memory and then compares. If your lists
# are larger than available memory then do not fear. Use the "shard.py" script
# to quickly devide your lists into smaller chunks.
#
#   --ringkeys   - is a list of keys to search for
#   --haystack   - is the list of keys to search
#   --out        - is the file to write 
#   --inclusive  - report keys that are found in the haystack

import os
import sys
import argparse
from collections import deque


def just_go(args):
    findin = {}
    print("reading search list..."),
    fh = open(args.ringkeys, "r")
    fulllist = fh.read()
    print("ok")
    print("create data structure"),
    search_list = fulllist.split('\n')
    print("ok")
    fh.close()

    print("reading list to search..."),
    fh = open(args.haystack, "r")
    fulllist = fh.read()
    print("ok")
    print("create data structure"),
    haystack = deque(fulllist.split('\n'))
    while True:
        k = haystack.popleft()
        if not k: break
        findin[k] = True
    print("ok")
    fh.close()

    fh = open(args.out, "w")
    if args.inclusive:
        
    else:
        for k in search_list:
            if k not in findin:
                fh.write("{0}\n".format(k))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='compare keylists')
    parser.add_argument('--ringkeys', required=True, help="new-line list of RING keys" )
    parser.add_argument('--haystack', required=True, help="list of keys to search in, probably a dump from the application index")
    parser.add_argument('--out', required=True, help="output file")
    parser.add_argument('--inclusive', help="find keys that are present in both lists")
    args = parser.parse_args()

    just_go(args)



#!/usr/bin/python

import os
import sys
import argparse
from collections import deque


def just_go(args):
    findin = {}
    print("reading search list..."),
    fh = open(args.find, "r")
    fulllist = fh.read()
    print("ok")
    print("create data structure"),
    search_list = fulllist.split('\n')
    print("ok")
    fh.close()

    print("reading list to search..."),
    fh = open(args.inlist, "r")
    fulllist = fh.read()
    print("ok")
    print("create data structure"),
    inlist = deque(fulllist.split('\n'))
    while True:
        k = inlist.popleft()
        if not k: break
        findin[k] = True
    print("ok")
    fh.close()

    fh = open(args.out, "w")
    for k in search_list:
        if k not in findin:
            fh.write("{0}\n".format(k))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='compare keylists')
    parser.add_argument('--find', required=True)
    parser.add_argument('--inlist', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    just_go(args)



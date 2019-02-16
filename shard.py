#!/usr/bin/python

##
# Takes a list of input keys and quickly shards them into an arbitrary space
# based on characters from the UKS dispersion nibbles.

import os
import sys
import argparse
import resource

##
# Configuration

# To speed things up this will open files in blocks and work with them rather
# than opening and closing files repeately
MAX_HANDLES=resource.RLIMIT_NOFILE

fh_arr = {}
shard_root='shards'
monres = 10000
count = 0
tic = 0

def prepare_fh(depth, append, shard_file):
    fh_blocks = 1
    shard_file_count = 2**(depth*4)
    flag = 'w'

    if shard_file_count > MAX_HANDLES:
        print(
          "Can't open that many files ({0}), reduce the depth or set your nofilen"+
          "limit to >{0}".format(str(shard_file_count))
        sys.exit(1)

    for n in range(0, shard_file_count):
        arpath = "{0}/".format(shard_root)
        keypre = ('%0*x' % (depth, n)).upper()

        for c in range(0, depth):
            arpath += "{0}/".format(keypre[c])

        if not os.path.exists(arpath):
            os.makedirs(arpath)

        if append == "true": flag='a'
        fh_arr[keypre] = open("{0}/{1}".format(arpath, shard_file), flag)

def sortus(keylist, mode, depth):

    sf = open(keylist, "r")
    if mode == "random":
        starts = 6 - depth
        ends = starts + depth
    else:
        starts = 0
        ends = depth

    while True:
        line = sf.readline()
        if not line: break
        if len(line) != 41: continue
        if line[starts:ends] == '': continue
        fh_arr[line[starts:ends]].write(line)


def clean_fh():
    for fh in fh_arr:
        fh_arr[fh].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Divide large keylist along some logic to divide operations on those keys')
    parser.add_argument('--depth', '-d', help='shard depth in nibbles (max 4, default 2)', default=2)
    parser.add_argument('--source', '-s',  help='source file for RING input keys', required=True)
    parser.add_argument('--output', '-o',  help='name of output file', default="shardlist.txt", required=True)
    parser.add_argument('--mode', '-m',  help='"random" sharding or "ordered" (default: ordered', default='orderd')
    parser.add_argument('--append', '-a',  help='append keys in sharded lists (default: false)', default='false')
    args = parser.parse_args()

    prepare_fh(int(args.depth), args.append, args.output)
    sortus(args.source, args.mode, int(args.depth))
    clean_fh()


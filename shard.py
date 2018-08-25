#!/bin/python

##
# Takes a list of keys as input and quickly shards them into an 8-bit space
# based on the first two hex chars of the RING key.

import os
import sys

fh_arr = {}
src_file = sys.argv[1]
shard_root='shards'
shard_file='keys.txt'
monres = 10000
count = 0
tic = 0

for n in range(0, 2**8):
    keypre = ('%0*x' % (2, n)).upper()
    print(keypre)
    arpath = "{0}/{1}/{2}".format(shard_root, keypre[0], keypre[1])
    if not os.path.exists(arpath):
        os.makedirs(arpath)

    fh_arr[keypre] = open("{0}/{1}".format(arpath, shard_file), "w")

srcf = open(src_file, "r")

while True:
    count += 1
    tic += 1
    line = srcf.readline()
    if not line: break
    fh_arr[line[0:2]].write(line)

    if tic == monres:
        print("{0} keys sharded".format(count))
        tic = 0

srcf.close()

for n in range(0, 2**8):
    keypre = ('%0*x' % (2, n)).upper()
    fh_arr[keypre].close()

print("done")

#!/usr/bin/python
import sys

srcFile=sys.argv[1]
extractFrom=sys.argv[2]
extractTo=sys.argv[3]
outputTo=sys.argv[4]

fh = open(srcFile, "r")
dst = open(outputTo, "w")
while True:
    line = fh.readline().strip()
    
    if line > extractFrom and line < extractTo:
        dst.write("{0}\n".format(line))
        dst.flush()
        
fh.close()
dst.close()


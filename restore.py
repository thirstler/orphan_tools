#!/usr/bin/python
#
# Restore messages from sqlite DB that recorded a 200 status during archive
#
# Script takes two arguments: [SOURCE DATABASE FILE] [SPROXYD HOST]

import sys
import sqlite3
import urllib2
import time

##
# Configuration
SPROXY_PORT="81"
SPROXY_PATH="/proxy"
SPROXY_DRIVER="chord"
# End configuration
##

##
# Args
DB_FILE=sys.argv[1]
SPROXY_HOST="localhost" # <- default

try:
    SPROXYD_HOST=sys.argv[2]
except:
    print("no sproxyd host specified, using {0}".format(SPROXY_HOST))

SPROXY_ENDPOINT="http://{0}:{1}/{2}/{3}".format(SPROXYD_HOST, SPROXY_PORT, SPROXY_PATH, SPROXY_DRIVER)

##
# Open everything
dbconn = sqlite3.connect(DB_FILE)
cur = dbconn.cursor()

# happy output
errs=0
tic=0
count=0
skip=1000
timer=0
msg_sec=0
lst_cnt=0
nownow = int(time.time())
start_t = nownow
cur.execute('''SELECT http_status, locator, message FROM mail WHERE http_status=200''')
while True:
    count += 1
    tic += 1
    try:
        code, key, message = cur.fetchone()
    except: break
    
    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request("{0}/{1}".format(SPROXY_ENDPOINT, key), data=message)
        request.add_header('Content-Type', 'application/text')
        request.get_method = lambda: 'PUT'
        url = opener.open(request)
    except Exception as e:
        print(e)
        errs+=1
        
    if tic == skip:
        timer = nownow
        nownow = int(time.time())
        msg_sec = float((count - lst_cnt))/(nownow - timer)
        tic = 0
        lst_cnt = count
        print("{0} messages restored, {1} errors logged, {2:.2f} messages/s".format(
                                                         count, errs, msg_sec))

print("{0} messages restored, {1} errors logged, in {2} seconds".format(
                                      count, errs, (int(time.time())-start_t)))
dbconn.close()
        

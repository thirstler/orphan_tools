#!/usr/bin/python
#
# Deletes all messages that were archived with a 200 status in the passed-in
# sqlite database
#
# Script takes two arguments: [method] [SOURCE DATABASE FILE] [SPROXYD HOST]

import sys
import sqlite3
import urllib2
import time
import datetime

##
# Configuration
SPROXY_HOST="localhost"
SPROXY_PORT="81"
SPROXY_PATH="/proxy"
SPROXY_DRIVER="chord"
# End configuration
##

##
# Args
METHOD=sys.argv[1] # one of file or db
DB_FILE=sys.argv[2]

try:
    SPROXYD_HOST=sys.argv[3]
except:
    print("no sproxyd host specified, using {0}".format(SPROXY_HOST))

SPROXY_ENDPOINT="http://{0}:{1}/{2}/{3}".format(SPROXYD_HOST, SPROXY_PORT, SPROXY_PATH, SPROXY_DRIVER)

def timef():
    return (float(datetime.datetime.now().microsecond)/1000000) + time.time()

##
# happy output
errs=0
tic=0
count=0
skip=1000
timer=0
msg_sec=0
lst_cnt=0
nownow = timef()
start_t = nownow


if METHOD=="db":
    dbconn = sqlite3.connect(DB_FILE)
    cur = dbconn.cursor()
    cur.execute('''SELECT http_status, locator FROM mail WHERE http_status=200''')
elif METHOD=="file":
    srcfh = open(DB_FILE, "r")
else:
    sys.stderr.write("bad method.\n")
    sys.exit(1)

while True:
    count += 1
    tic += 1

    if METHOD == "db":
        try:
            code, key = cur.fetchone()
        except: break
    elif METHOD == "file":
        key = srcfh.readline().strip()

    if not key: break

    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request("{0}/{1}".format(SPROXY_ENDPOINT, key))
        request.get_method = lambda: 'DELETE'
        url = opener.open(request)
    except Exception as e:
        print(e)
        errs+=1

    if tic == skip:
        timer = nownow
        nownow = timef()
        msg_sec = float((count - lst_cnt))/(nownow - timer)
        tic = 0
        lst_cnt = count
        print("{0} messages deleted, {1} errors logged, {2:.2f} messages/s".format(count, errs, msg_sec))


print("{0} messages deleted, {1} errors logged, in {2} seconds".format(
        count, errs, (timef()-start_t)))

if METHOD == "file": srcfh.close()
elif METHOD == "db": dbconn.close()


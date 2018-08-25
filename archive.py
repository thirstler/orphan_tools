#!/usr/bin/python
#
# Archive messages given a bare key-list. Records HTTTP status code and logs
# extraction errors.
#
# Script takes three arguments:
#                    [TEXT KEY LIST FILE] [TARGET DATABASE FILE] [SPROXYD HOST]

import sys
import sqlite3
import urllib
import time

##
# Configuration
SPROXY_PORT="81"
SPROXY_PATH="/proxy"
SPROXY_DRIVER="chord"
fail_log="extraction_failure.txt"
# End configuration
##

##
# Args
KEY_SOURCE=sys.argv[1]
DB_FILE=sys.argv[2]
SPROXY_HOST="localhost" # <- DEFAULT

try:
    SPROXYD_HOST=sys.argv[3]
except:
    print("no sproxyd host specified, using {0}".format(SPROXY_HOST))

SPROXY_ENDPOINT="http://{0}:{1}/{2}/{3}".format(SPROXYD_HOST, SPROXY_PORT, SPROXY_PATH, SPROXY_DRIVER)

##
# Open everything
keysrcf=open(KEY_SOURCE, "r")
dbconn = sqlite3.connect(DB_FILE)
cur = dbconn.cursor()
fl = open(fail_log, "w")

##
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
fofcount=0
fof_ttl=0
try:
    cur.execute('''CREATE TABLE mail (http_status int, locator text PRIMARY KEY, message blob)''')
except sqlite3.OperationalError as e:
    pass
except:
    print ("something messed up")
    sys.exit(1)

while True:
    count += 1
    tic += 1

    getkey = keysrcf.readline().strip()
    if not getkey: break
    
    try:
        req = urllib.urlopen("{0}/{1}".format(SPROXY_ENDPOINT, getkey))
        mail_content = req.read()
		http_status = int(req.getcode())
		if http_status != 200: fofcount += 1
    except:
        errs += 1
        fl.write("{0} {1}\n".format(getkey, e))
    
    try:
        sql = '''INSERT INTO mail (http_status, locator, message) values (?, ?, ?);'''
        cur.execute(sql, [http_status, getkey,
                sqlite3.Binary(mail_content)])
        dbconn.commit()
    except Exception as e:
        errs += 1
        fl.write("{0} {1}\n".format(getkey, e))
        
    req.close()
    
    if tic == skip:
        timer = nownow
        nownow = int(time.time())
        msg_sec = float((count - lst_cnt))/(nownow - timer)
        tic = 0
        lst_cnt = count
		fof_ttl += fofcount
        print("{0} processed, {1} errors, {2:.2f} messages/s, {3} non-200s".format(
                count, errs, msg_sec, fofcount))


print("{0} messages archived, {1} errors logged and {2} non-200s returned in {3} seconds".format(
                                      count, errs, fof_ttl, (int(time.time())-start_t)))
fl.close()
dbconn.close()


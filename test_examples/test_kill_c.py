#! /bin/env python2.7

"""
# test_kill_c.py
# invoked from test_kill.py
# this is just a simple immitation of a child process
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys
import time


pid = os.getpid()

nn = 60
ii = 0
while ii < nn:
    ii += 1
    print "pid=%d, ii = %d, time = %s" % (pid, ii, time.strftime('%H:%M:%S'))
    time.sleep(2)

print "FINISHED - pid=%d, ii = %d, time = %s" % (pid, ii, time.strftime('%H:%M:%S'))

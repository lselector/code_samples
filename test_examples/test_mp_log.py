#! /bin/env python2.7

""" 
# test_mp_log.py
# run like this:
#   python test_mp_log.py >/tmp/junk.txt
"""

import sys
import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

import multiprocessing as mp
import time

import ipython_debug
reload(ipython_debug)
from ipython_debug import debug_here
# import affinity

# ---------------------------------------------------------------
# reset CPU affinity mask as described here
# http://stackoverflow.com/questions/15639779/what-determines-whether-different-python-processes-are-assigned-to-the-same-or-d
os.system("taskset -p 0xff %d" % os.getpid())

# ---------------------------------------------------------------
def do_work(ii,nn):
    """
    # this runs in child process
    """
    print "work_start",ii
    for jj in range(1000):
      for line in range(4):
          ss = "a_%d_%d_%d " % (ii,jj,line)
          ss = ss*20
          print ss
    print "work_end %d" % ii
    return ii, nn

# ---------------------------------------------------------------
def save_results(retval):
    """
    # this runs in parent process
    """
    ii, nn = retval
    print "save %2d" % (ii)
    result[ii] = 1

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
NN=20
result = [0]*NN
pool = mp.Pool(processes=NN, maxtasksperchild=1)    
# --------------------------------------
# start several processes
t3 = time.time()
for ii in range(NN):
    pool.apply_async(do_work, args=[ii,NN], callback=save_results)
    print "started %d" %ii
pool.close()
pool.join()
t4 = time.time()
print 'finished work'
print "t4-t3=%.3f" %(t4-t3)
print "result =",result

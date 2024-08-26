#! /bin/env python2.7

""" 
# test_mp.py
#   putting dataframe into a shared memory
#   starting many child processes which lookup data in the dataframe
#   collect results from all children in the parent
"""

import sys
import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

import pandas as pd
import numpy as np
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
    rn = ii*nrows_per_child
    df_val = int(df.ix[rn,'col1']) # lookup operation
    pid = int(os.getpid())
    fh = open("junk/mp%d.txt" % pid, "w")
    fh.write("%s(pid=%d): %d\n" % ("mama", pid, df_val))
    fh.close()
    # time.sleep(10)
    print "work_end  ",ii
    return ii, nn, df_val

# ---------------------------------------------------------------
def save_results(retval):
    """
    # this runs in parent process
    """
    ii, nn, df_val = retval
    print "save %2d" % (ii)
    result[ii] = df_val

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
NN=30
nrows_per_child = int(1e6)
nrows_total = NN * nrows_per_child
print "populating dataframe with %d rows" % nrows_total
t1 = time.time()
df = pd.DataFrame({'col1':range(0, nrows_total),
                   'col2':range(1, nrows_total+1),
                   'col3':range(2, nrows_total+2),
                   'col4':range(3, nrows_total+3)
                 }, index = range(nrows_total))
t2 = time.time()
print "finished creating the dataframe"
print "t2-t1=%.3f" %(t2-t1)

result = [0]*NN
pool = mp.Pool(processes=NN, maxtasksperchild=1)    
# --------------------------------------
# start several processes
t3 = time.time()
for ii in range(NN):
    pool.apply_async(do_work, args=[ii,NN], callback=save_results)
    print "started ",ii
pool.close()
pool.join()
t4 = time.time()
print 'finished work'
print "t4-t3=%.3f" %(t4-t3)
print "result =",result

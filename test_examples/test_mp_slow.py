#! /bin/env python2.7

""" 
# test_mp_slow.py - test putting dataframe into a shared memory
# using multiprocessing.Manager.
# This method is slow. 
"""

import sys
import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

import ipython_debug
reload(ipython_debug)
from ipython_debug import debug_here

import numpy as np
import pandas as pd
from multiprocessing import Manager, Process
import time

# ---------------------------------------------------------------
# reset CPU affinity mask as described here
# http://stackoverflow.com/questions/15639779/what-determines-whether-different-python-processes-are-assigned-to-the-same-or-d
os.system("taskset -p 0xff %d" % os.getpid())

# ---------------------------------------------------------------
def do_work(ns, mynum, label):
    # df = ns.df
    df_val = ns.df.ix[mynum,'bb']
    df_val = 1
    pid = int(os.getpid())
    fh = open("junk/junk%d.txt"%pid,"w")
    fh.write("%s(pid=%d): %d\n" % (label, pid, df_val))
    fh.close()

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
# create big dataframe
n_rows = int(2e7)
print "populating dataframe with %d rows" % n_rows
t1 = time.time()
df = pd.DataFrame({'aa':range(n_rows),'bb':range(n_rows)})
t2 = time.time()
print "finished creating the dataframe"
print "t2-t1=%.3f" %(t2-t1)

# --------------------------------------
# create a multiprocessing Manager object,
# and put the dataframe into its namespace
mgr = Manager()
ns = mgr.Namespace()
ns.df = df

# --------------------------------------
# start several processes - and pass them the namespace to share
NN=30
procs = [0]*NN
ns1=1
t3 = time.time()
for ii in range(NN):
    label = "proc%2d" % ii
    print "before %s" % label
    procs[ii] = Process(target=do_work, args=(ns, ii, label,))
    procs[ii].start()

print "All started"

# --------------------------------------
# wait for the workers to finish
for ii in range(NN):
    procs[ii].join()
    print "Finished %d" % ii

t4 = time.time()
print 'finished work'
print "t4-t3=%.3f" %(t4-t3)

#! /bin/env python2.7

"""
# test_garbage_collect.py
# simple test to show how python collects garbage
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

import myutil
reload(myutil)
from myutil import *

mem1 = memory_usage()
print mem1

print "creating big numpy array (takes ~30sec, >5GBytes)"
aa = np.random.rand(int(6e8))
mem2 = memory_usage()
print mem2

print "deleting big numpy array"
del aa
mem3 = memory_usage()
print mem3

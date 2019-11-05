#! /bin/env python2.7

""" 
# Script to do bulk rename many files
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

import sys
import glob
import os
import re


print "nothing to run, this is just a code template"

# glob_pattern = "somedir/20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]*myname.csv"
# src_files = sorted(glob.glob(glob_pattern))
# # print src_files
# for src in src_files:
#     dst = re.sub(r'myname','d_myname',src)
#     print src,dst
#     os.rename(src,dst)

#! /bin/env python2.7

"""
# test_path.py
# simple script to show how to get the absolute path of the script
# By Lev Selector, March 2015
# ---------------------------------------------------------------
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import os.path
import sys


method1 = os.path.realpath(__file__)
print method1

method2 = os.path.abspath(sys.argv[0])
print method2

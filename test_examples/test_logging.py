#! /bin/env python2.7

"""
#  test_logging.py
#  by Lev Selector
"""

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
from ipython_debug import *
import logging

log1 = logging.getLogger('log1')
log1.setLevel(logging.DEBUG)
log2 = logging.getLogger('log2')
log2.setLevel(logging.DEBUG)

log1.handlers=[]
log2.handlers=[]

ch1 = logging.StreamHandler()
ch1.setLevel(logging.DEBUG)

ch2 = logging.StreamHandler()
ch2.setLevel(logging.DEBUG)

form1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
form2 = logging.Formatter('%(asctime)s - %(message)s')

# add formatter to ch
ch1.setFormatter(form1)
ch2.setFormatter(form2)

# add ch to logger
log1.addHandler(ch1)
log2.addHandler(ch2)

log1.debug('*** log1 debug message')
# log2.debug('*** log2 debug message')

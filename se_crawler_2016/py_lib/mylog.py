#! /bin/env python3

"""
# mylog.py - mylog(bag,...) & myerr(bag, ....) functions
"""

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
# --------------------------------------
import sys
if sys.version_info > (3,3):
    import importlib
# --------------------------------------
import ipython_debug
if sys.version_info > (3,3):
    importlib.reload(ipython_debug)
else:
    reload(ipython_debug)
from ipython_debug import *
# --------------------------------------
import mybag
if sys.version_info > (3,3):
    importlib.reload(mybag)
else:
    reload(mybag)
from mybag import *
# --------------------------------------

# --------------------------------------------------------------
def mylog(bag, message='', verbose=True, mask_log=True):
    """
    # optionally prepends prefix to (all) lines of the message 
    # and prints it out
    # options:
    #   verbose  (True of False) - if set to false, will not log
    #   mask_log (True or False) - flag to mask (prepend) lines.
    #            note: default value of the prefix_string 'mask_log'
    #            can be changed by defining bag.mask_log_str
    """
    if not verbose:
        return
    mask_log_str = ''
    if mask_log:
        if test_avail(bag, "mask_log_str"):
            mask_log_str = bag.mask_log_str
        else:
            mask_log_str = 'mask_log'
    if len(mask_log_str):
        mask_log_str = mask_log_str + "  "
    mystr = str(message)
    mylist = mystr.split("\n")
    output = ""
    for ss in mylist:
        output += mask_log_str + ss + "\n"
    print(output.rstrip())

# ---------------------------------------------------------------
def myerr(bag, message):
    """
    # prints error message without masking it
    """
    mylog(bag, message, mask_log=False)


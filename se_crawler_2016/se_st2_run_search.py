#! /bin/env python3

# --------------------------------------------------------------
# se_st2_run_search.py
# --------------------------------------------------------------

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys, random, gc, argparse, time
import importlib

import myutil
importlib.reload(myutil)
from myutil import *

import myutil_dt
importlib.reload(myutil_dt)
from myutil_dt import *

import http_headers
import requests

# --------------------------------------------------------------
def main(bag):
    """
    # main
    """
    myinit(bag)
    scriptname = os.path.basename(sys.argv[0])
    print("starting ", scriptname)
#    while True:
#        time.sleep(1)
#        print(time.time())


# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)

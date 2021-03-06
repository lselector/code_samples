#! /bin/env python3

# --------------------------------------------------------------
# se_st4_parse_listings.py
# --------------------------------------------------------------

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys, random, gc, argparse
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

# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)

#! /bin/env python2.7

"""
# test_exception.py
# script showing how to raise exceptions
# https://docs.python.org/2/tutorial/errors.html
# http://jeffknupp.com/blog/2013/02/06/write-cleaner-python-use-exceptions/
# We decided to always throw generic exeptions.
# We decided to use "raise" instead of "sys.exit(1)"
# Sometimes we need to exit with specific error code - we use
# sys.exit(65) for that in the out-most "except:" block
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys, traceback

import myutil
reload(myutil)
from myutil import *

# ---------------------------------------------------------------
def do_work(bag):
    """
    #
    """
    print "hhhh"
    try:
        print "in do_work() - opening file", bag.fname
        fh = open(bag.fname)
    except:
        print "in do_work() - problem opening file", bag.fname
        raise
    else:
        print "in do_work() - file %s was opened for reading OK" % bag.fname

# ---------------------------------------------------------------
def main(bag):
    """
    #
    """
    print "Hello"
    # ----------------------------------
    try:
        bag.fname = sys.argv[0]
        do_work(bag)
        bag.fname = "non_existent_file.txt"
        do_work(bag)
    except:
        print "in main() - catching error"
        traceback.print_exc()
        sys.exit(65)
    else:
        print "in main() - everything finished OK"

# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)

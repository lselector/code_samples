#! /bin/env python
"""
# test_df_speed2.py
# df.to_csv speedtests
"""

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
import sys, time

import myutil
reload(myutil)
from myutil import *

import myutil_dt
reload(myutil_dt)
from myutil_dt import *

# ---------------------------------------------------------------
def run10_to_csv(bag):
    """ run 10 tests """
    print type(bag.df['c1'][5])
    for ii in range(10):
        label = "test"+str(ii)
        t1 = time.time()
        bag.df.to_csv("junk/%s.csv"%label,index=False)
        dt = time.time()-t1
        print "%s : %12.6f" % (label, dt)

# ---------------------------------------------------------------
def run_write_tests(bag):
    """ run_write_tests """
    nrows = 10**6
    print("creating the test DataFrame df with %s rows" % commify(nrows))
    bag.df = pd.DataFrame(data={'c1':[jj for jj in range(nrows)]})
    #  , index=range(nrows), dtype=object)
    # ----------------------------------
    print "writing as is"
    run10tests(bag)
    # ----------------------------------
    print "changing type to np.int64"
    bag.df.c1 = bag.df.c1.astype(np.int64)
    run10tests(bag)
    # ----------------------------------
    print "changing type to np.int32"
    bag.df.c1 = bag.df.c1.astype(np.int32)
    run10tests(bag)
    # ----------------------------------
    print "changing type to object"
    bag.df.c1 = bag.df.c1.astype(object)
    run10tests(bag)
    # ----------------------------------
    print "changing type to np.str"
    bag.df.c1 = bag.df.c1.astype(np.str)
    run10tests(bag)
    # ----------------------------------
    print "changing type to np.int64"
    bag.df.c1 = bag.df.c1.astype(np.int64)
    run10tests(bag)

# ---------------------------------------------------------------
def print_read_results(df,t1):
    """ print_read_results """
    print "%d : %12.6f" % (len(df), time.time()-t1)
    # print "-"*40
    # print "(%-13s,%-13s),(%-25s,%-25s)" % (df.c1[0], df.c1[1], type(df.c1[0]), type(df.c1[1]))

# ---------------------------------------------------------------
def run_read_tests(bag):
    """ run_read_tests """
    # ----------------------------------
    nrows = 10**6
    base = 978*(10**10)
    print("creating the test DataFrame df with %s rows" % commify(nrows))
    bag.df = pd.DataFrame(data={'c1':[base+jj for jj in range(nrows)]})
    bag.df.c1 = bag.df.c1.map(lambda x : str(x) if (x % 2) else '')
    fname = "junk/test.csv"
    print("writing to file %s" % fname)
    bag.df.to_csv("junk/test.csv", index=False)
    # ----------------------------------
    print "-"*40, "\nreading as is"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False)
    print_read_results(df,t1)
    # ----------------------------------
    print "-"*40, "\nreading engine=python"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False, engine='python')
    print_read_results(df,t1)
    # ----------------------------------
    print "-"*40, "\nreading as np.float64"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False, dtype={'c1':np.float64})
    print_read_results(df,t1)
    # ----------------------------------
    print "-"*40, "\nreading as object"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False, dtype={'c1':object})
    print_read_results(df,t1)
    # ----------------------------------
    print "-"*40, "\nreading as np.object"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False, dtype={'c1':np.object})
    print_read_results(df,t1)
    # ----------------------------------
    print "-"*40, "\nreading as np.str"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False, dtype={'c1':np.str})
    print_read_results(df,t1)
    # ----------------------------------
    print "-"*40, "\nreading as is"
    t1 = time.time()
    for ii in range(3):
        df=pd.read_csv(fname, skip_blank_lines=False)
    print_read_results(df,t1)

# ---------------------------------------------------------------
def main(bag):
    """ main """
    myinit(bag)
    bag.mask_log_str = ""
    print_start_time(bag)
    # ----------------------------------
    # run_write_tests(bag)
    run_read_tests(bag)
    # ----------------------------------
    print_timing(bag, exclude=bag.exclude)
    print_elapsed_time(bag)

# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)

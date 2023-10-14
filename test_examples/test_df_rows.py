#! /bin/env python

"""
# test_df_rows.py
# testing row-by-row operations
"""

# Lev's imports (not all used here)

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
import sys
if sys.version_info > (3,3):
    import importlib

import time
from datetime import date, datetime, timedelta
import timeit

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
pd.options.display.width           =  1000
pd.options.mode.chained_assignment =  None
import inspect

from ipython_debug import debug_here

# ---------------------------------------------------------------
decades = [1,10,100,1000,10000,100000,1000000,10000000]
#decades = [10]
def get_df(nrows):
    """
    # Lev's notes from test_df_speed.py:

    # returns a simple DataFrame for performance testing
    
    # typical usage:
    #   aa=mmm()    #       10 rows, very small and fast
    #   aa=mmm(1e6) #   1 mil. rows - takes    3 sec to create
    #   aa=mmm(1e7) #  10 mil. rows - takes   30 sec to create and approx 1.2 GBytes
    #   aa=mmm(1e8) # 100 mil. rows - takes  300 sec to create and approx 18 GBytes
    # Note:
    #   If you groupby column:
    #      'gg'  - size of groups will be ~10 rows
    #      'ind' - size of each group is exactly 1 row
    #      'ss'  - size of groups is approx (nrows/26)
    # Structure of the DataFrame:
    #          aa        bb        cc    ii         ss  ind  gg
    # 0  0.693826  0.456081  0.196131  6938  ***wxy***    0   0
    # 1  0.594927  0.606414  0.898009  5949  ***vwx***    1   0
    # 2  0.546712  0.053141  0.691350  5467  ***hij***    2   0
    # 3  0.540285  0.325912  0.792903  5402  ***uvw***    3   0
    # 4  0.157368  0.756183  0.404507  1573  ***nop***    4   0
    """
    ncols  =  3
    nrows = int(nrows)
    # if nrows > 1e6:
    #     print("working, it should take ~%d sec" % int(nrows * 3.0/1e6))
    if nrows <= 1: nrows = 1
    mydata = np.random.rand(nrows, ncols)
    df = pd.DataFrame(data=mydata,
                     index=range(nrows),
                   columns=[chr(97+x)*2 for x in range(ncols)])
    return (mydata,df)

def spaceInt(max,quant):
    return ' ' * (max-len(str(int(quant))))

def runTest(mydata,df):
    t1 = time.time()
    #debug_here()
    sum = df.aa.sum()
    t2 = time.time()
    print '%sDataFrame(%d).sum()' % (spaceInt(8,nrows),nrows),\
          '%s%6.9f'               % (spaceInt(7,sum),sum),\
          'in %s%3.9f seconds'    % (spaceInt(3,t2-t1),t2-t1)
    badSum = sum
    sum = 0.0
    t1 = time.time()
    for rw in mydata: sum += rw[0]
    t2 = time.time()
    print '%s          Array(%d)' % (spaceInt(8,nrows),nrows),\
          '%s%6.9f'               % (spaceInt(7,sum),sum),\
          'in %s%3.9f seconds'    % (spaceInt(3,t2-t1),t2-t1)
    sum = 0.0
    t1 = time.time()
    for rw in df.iterrows(): sum += rw[1][0]
    t2 = time.time()
    print '%s      DataFrame(%d)' % (spaceInt(8,nrows),nrows),\
          '%s%6.9f'               % (spaceInt(7,sum),sum),\
          'in %s%3.9f seconds'    % (spaceInt(3,t2-t1),t2-t1)
    #goodSum = sum
    #error = abs(goodSum-badSum)
    #sumError = error/goodSum
    #print "Error is %f, or %f%%" % (error,sumError*100)
    print

if __name__ == '__main__':
    for nrows in decades:
        (mydata,df) = get_df(nrows)
        runTest(mydata,df)


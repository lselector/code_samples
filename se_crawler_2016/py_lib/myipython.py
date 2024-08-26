#! /bin/env python3

"""
# myipython.py - module with functions for ipython
# called from ~/.ipython/profile_default/startup/python_init.py
# 2014-2015 by Lev Selector
"""

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
# --------------------------------------
import sys
if sys.version_info > (3,3):
    import importlib
# --------------------------------------
import myutil
if sys.version_info > (3,3):
    importlib.reload(myutil)
else:
    reload(myutil)
from myutil import *
# --------------------------------------
import myutil_dt
if sys.version_info > (3,3):
    importlib.reload(myutil_dt)
else:
    reload(myutil_dt)
from myutil_dt import *
# --------------------------------------
import pkgutil
pd.set_option('display.width',1000)           # set big width to avoid wrapping
pd.set_option('mode.chained_assignment',None) # to avoid warnings when working with DataFrames
# print("pd.options.display.width           = " + str(pd.options.display.width))
# print("pd.options.mode.chained_assignment = " + str(pd.options.mode.chained_assignment))
print("python: " + sys.executable)
import platform
print(sys.version.split("\n")[0] + "| " + str(platform.architecture()[0]))
print("ipython profile: default")

# ---------------------------------------------------------------
def remask(ser, regex, flags=re.I):
    """
    # uses regex to create a mask for a DataFrame column (or a series)
    # Example of usage:
    #   mm=bag.member
    #   mask = remask(mm.billing_name, r'ebay')
    #   mm[['id','billing_name']][mask]
    # Note: 
    # to make case sensitive match, provide 3rd parameter flags=0
    # for example:
    #   mask = remask(mm.billing_name, r'eBay', flags=0)
    """
    return ser.map(lambda x: True if re.search(regex, str(x), flags) else False)

# ---------------------------------------------------------------
def bbb():
    """
    # returns a simple pandas DataFrame - useful for drop_duplicates
    # Example of usage:
    #   bb=bbb()
    #   bb=drop_duplicates()
    """
    bb=pd.DataFrame({
        'id1':[1,2,2,3,3,3],
        'id2':[11,22,22,33,33,33],
        'val1':['v1','v2','v2','v3','v3','v3'],
        'val2':['z1','z2','z2','z3','z3','z3']})

    return bb

# ---------------------------------------------------------------
def ddd():
    """
    # returns a simple pandas DataFrame - useful for quick tests
    """
    nrows = 7
    aa = pd.DataFrame({
          'ii':[0,1,2,3,4,5,np.nan],                                           # float64
          'i1':[6,5,4,3,2,1,0],
          'i2':[6,5,4,4,1,1,0],
          'ff':[0.0,1.0,2.0,np.NaN,4.0,5.0,6.0],                               # float64
          'f1':[0.0,1.01,2.002,3.0003,4.00004,5.000005,6.0000006],
          'f2':[1.11,2.22,3.33,4.44,5.55,7.77,9.99],
          'ss':['s0','s1','s2','s3',np.nan,'s5','s6'],                         # dtype=object, np.nan is float64
          's1':np.array(['s0','s1','s2','s2',np.nan,'s5','s6'],dtype=np.str),  # dtype=object, 'nan' is string
          's2':['1.11','2.22','3.33','4.44','5.55','7.77','9.99'],
          'bb':[True, False, True, False, np.nan, False, True],                # dtype=object, np.nan is float64
          'b1':[True, False, True, False, True, False, True],                  # dtype=bool
          'xx':range(nrows),
          'yy':[x*50 + 60 + np.random.randn() for x in range(nrows)]
    })

    return aa.ix[:,['ii','i1','i2','ff','f1','f2','ss','s1','s2','bb','b1','xx','yy']]

# ---------------------------------------------------------------
def ddd2():
    """
    # returns a simple pandas DataFrame useful for quick stack/unstack/pivot tests
    # example of usage:
    # xx=ddd2()
    # xx.set_index(["Month","name"]).stack().unstack('Month')
    """
    aa = pd.DataFrame([
        ["Jan","name1",1,2,3],
        ["Jan","name2",4,5,6],
        ["Mar","name1",11,12,13],
        ["Mar","name2",14,15,16]], columns=["Month","name","c1","c2","c3"])

    return aa

# ---------------------------------------------------------------
def ddd3():
    """
    # returns a simple pandas DataFrame useful for quick stack/unstack/pivot tests
    # example of usage:
    # xx=ddd3()
    # xx.pivot('foo','bar','baz')
    #         A   B   C
    #    one  1   2   3
    #    two  4   5   6
    #
    # xx.pivot('foo', 'bar')['baz']
    #         A   B   C
    #    one  1   2   3
    #    two  4   5   6
    """
    aa = pd.DataFrame({
      'foo':3*['one'] + 3*['two'],
      'bar':2*['A','B','C'],
      'baz':[1,2,3,4,5,6] })

    return aa[['foo','bar','baz']]

# ---------------------------------------------------------------
def mmm(nrows=10):
    """
    # returns a simple DataFrame for performance testing
    # typical usage:
    #   aa=mmm()    #       10 rows, very small and fast
    #   aa=mmm(1e6) #   1 mil. rows - takes    3 sec to create    
    #   aa=mmm(1e7) #  10 mil. rows - takes   30 sec to create and approx 1.2 GBytes
    #   aa=mmm(1e8) # 100 mil. rows - takes  300 sec to create and approx 18 GBytes
    
    """
    ncols  =  3
    nrows = int(nrows)
    if nrows > 1e6:
        print("working, it should take ~%d sec" % int(nrows * 3.0/1e6))
    if nrows <= 1:
        nrows = 1
    mydata = np.random.rand(nrows, ncols)
    df = pd.DataFrame(data=mydata, 
                   index=range(nrows), 
                   columns=[chr(97+x)*2 for x in range(ncols)])
    df['ii'] = df.aa.map(lambda xx: int(xx*10000))

    # -----------------------
    def chars3(xx):
        return chr(97+xx%26) + chr(97+(xx+1)%26) + chr(97+(xx+2)%26)
    # -----------------------
    df['ss'] = '>>>' + df.ii.map(lambda xx: chars3(xx)) + '<<<'
    df['ind'] = df.index
    ngroups = int(nrows/10.0)+1
    df['gg'] = df.ind % ngroups

    return df

# ---------------------------------------------------------------
def myprint(df):
    """
    # prints DataFrame or Series
    # Example: /myprint DF
    # notice leading "/" to tell ipython that this is a function call
    """
    print(df.to_string())

# ---------------------------------------------------------------
def mygrep(df,ss):
    """
    # prints DataFrame or Series for some pattern. Returns a list of lines.
    # Example: /mygrep   DF    r'some regex'
    # notice leading "/" to tell ipython that this is a function call
    """
    lines = df.to_string().split("\n")
    return [line for line in lines if re.search(ss,line)]

# ---------------------------------------------------------------
def mymodules():
    return sorted([m[1] for m in pkgutil.iter_modules()])

# ---------------------------------------------------------------
def show_duplicates(df, cols=None, include_nulls=True):
    """
    # accepts a dataframe df and a column (or list of columns)
    # if list of columns is not provided - uses all df columns
    # returns a dataframe consisting of rows of df
    # which have duplicate values in "cols"
    # sorted by "cols" so that duplciates are next to each other
    # Note - doesn't change index values of rows
    """
    if not cols:
        cols = []
    # ---------------------------------
    aa = df.copy()
    mycols = cols
    # ---------------------------------
    if len(mycols) <= 0:
        mycols = aa.columns.tolist()
    elif type(mycols) != list:
        mycols = list(mycols)
    # ---------------------------------
    if not include_nulls:
        mask = False
        for mycol in mycols:
            mask = mask | (aa[mycol] != aa[mycol])  # test for null values
        aa = aa[~mask]                              # remove rows with nulls in mycols
    if len(aa) <= 0:
        return aa[:0]
    # ---------------------------------
    # duplicated() method returns Boolean Series denoting duplicate rows
    mask = aa.duplicated(cols=mycols, take_last=False).values \
         | aa.duplicated(cols=mycols, take_last=True).values
    aa = aa[mask]
    if len(aa) <= 0:
        return aa[:0]
    # ---------------------------------
    # sorting to keep duplicates together
    # Attention - can not sort by nulls
    # bb contains mycols except for cols which are completely nulls
    bb = aa[mycols]
    bb = bb.dropna(how='all',axis=1)
    # sort aa by columns in bb (thus avoiding nulls)
    aa = aa.sort_index(by=bb.columns.tolist())
    # ---------------------------------
    # sorting skips nulls thus messing up the order. 
    # Let's put nulls at the end
    mask = False
    for mycol in mycols:
        mask = mask | (aa[mycol] != aa[mycol])  # test for null values
    aa1 = aa[~mask]
    aa2 = aa[mask]
    aa = aa1.append(aa2)

    return aa

# ---------------------------------------------------------------
def rows_with_nulls(df):
    """
    # accepts a DataFrame with 0 or more rows
    # returns a DataFrame which contains rows with at least one null value.
    # If no nulls - returns an empty DataFrame
    """
    mask=False
    for col in df.columns: mask = mask | df[col].isnull()
    return df[mask]

# ---------------------------------------------------------------
def df_size(df):
    """
    # ballpark estimate of DataFrame memory usage
    """
    mysizes = {
        float : sys.getsizeof(1.0),
        int   : sys.getsizeof(1),
        bool  : sys.getsizeof(True),
    }
    bb = df.dtypes.tolist()
    memsize = 0
    for mytype in bb:
        if mytype == float:
            memsize += mysizes[float]
        elif mytype == int:
            memsize += mysizes[int]
        elif mytype == bool:
            memsize += mysizes[bool]
        else:
            memsize += 30

    return memsize * len(df)

# ---------------------------------------------------------------
def myhist(N=30, regex='', pr=True):
    """
    # ipython history function searches multiple sessions.
    # You can specify number of lines to search, and optionally regex to select from these commands.
    #     myhist(200)
    #     myhist(1000, 'myword')
    # You can return history list into a variable instead of printing:
    #     aa = myhist(10000, 'cpx', pr=False)
    # Note: alternative approach to this function is to create a magic function
    # See how to do it here:
    # http://ipython.org/ipython-doc/stable/interactive/reference.html
    # Also you can create an ipython function which would use this ipython magic
    # command to output history from a range of sessions:
    #    ~2000/1-~0/2000
    """
    import subprocess
    import re
    import shutil
    # ----------------------------------
    # If home directory is on a network drive, then there may be a locking conflict
    # between this procedure trying to read the sqlite file, and ipython trying
    # to update it. To resolve this problem we make a temporary copy - and query it.
    homedir = os.environ['HOME']
    dbfile = homedir + "/.ipython/profile_default/history.sqlite"
    db_tmp = dbfile + ".tmp"
    shutil.copyfile(dbfile, db_tmp)
    cmd = '/usr/bin/sqlite3 %s "select source_raw from history"' % db_tmp
    txt = subprocess.check_output(cmd, shell=True)
    # ----------------------------------
    lines = txt.split('\n')
    lines2 = []
    if len(regex) <= 0:
        lines2 = lines[-N:]   # get last N lines
    else:
        for line in lines:
            if re.search(regex, line, re.I):
                lines2.append(line)
        lines2 = lines2[-N:]  # get last N lines which match the criteria
    # ----------------------------------
    if pr:     # by default just print the history
        for line in lines2:
            print(line)
    # ----------------------------------
    else:      # if "pr" is unset - return the list
        return lines2

# ---------------------------------------------------------------
def tofile(obj,fname):
    """
    # prints any object as string to a text file
    # Example: /tofile  DF  'junk.txt'
    # notice leading "/" to tell ipython that this is a function call
    """
    ss= str(type(obj))
    if re.search(r'Series|DataFrame',ss):
        mystr = obj.to_string()
    else:
        mystr = obj.__str__()
    f=open(fname,'w')
    f.write(mystr)
    f.close()

# ##############################################################
# main execution
# ##############################################################
pass

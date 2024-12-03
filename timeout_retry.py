
"""
# How to do timeouts in Python
# using wrapt_timeout: https://github.com/bitranox/wrapt_timeout_decorator
# code below is extracted from a script querying Salesforce
# is is somewhat cleaned - but still uses some custom objects and functions
# which need to be substituted by something else.
# 
# bag - a dictionary where you can use dot notation (bag.key instead of bag['key'])
#     https://github.com/lselector/setup_computer/blob/master/py_lib/mybag.py
# bag.soql - a string with the query
# bag.sf.query_all() - a function to run the query and return a result
# commify - function to format a number by separating thousands with commas
# conv_res_to_df() - function to convert result set into pandas dataframe
# test_avail() - function to test if a particular key exists in a bag dictionary
# run_query() - function to run one query in a forked subprocess created by timeout
# now_str() - function returning current date-time
# run_sql(bag, bag2) - wrapper to run a query. 
#    It uses two global variables (dictionaries) - bag and bag2 
#    bag is used to pass parameters
#    bag2.df is used to accumulate (concat) data of sequential calls to run_sql()
"""

import os, sys, time
import ...
from wrapt_timeout_decorator import *

# ---------------------------------------------------------------
def run_query(bag):
    """
    # procedure to run individual query bag.soql
    # returns bag, result
        """
    qt1 = time.time()
    result = bag.sf.query_all(bag.soql)
    print("\nQuery finished at   %s" % (now_str()))
    N_records = result['totalSize']
    print("Received records:", commify(N_records))
    qt2 = time.time()
    print("Finished query: elapsed seconds = %s" % (commify(qt2-qt1,2)))
    bag.success_flag = True
    return bag, result

# ---------------------------------------------------------------
def run_sql(bag, bag2):
    """
    # runs query with timeout and retry
    # bag.mylabel - contains label for the query (object and dates)
    # bag.sql - SQL string
    # bag is passed to separate process (controlled by timeout)
    # the returned result is converted to pandas df and appended to bag2.df
    # bag2.df is kept separate from bag to keep bag object small
    # (because bag is being passed to the forked function)
    """
    bag.success_flag = False
    result = None
    print("querying for ", bag.mylabel)
    N_try_max = 9
    N_try = 0
    while (bag.success_flag == False) and (N_try < N_try_max):
        bag.t1 = time.time()
        N_try += 1
        print("\n--------------------\n")
        print("Attempt # %d of %d  at   %s\n" % (N_try, N_try_max, now_str()))
        print("Running Query\n" + bag.sql + "\n ... \n")
        try:
            # bag, result = run_query(bag) # without timeout
            bag,result = timeout(dec_timeout=bag.arg_timeout, use_signals=False)(run_query)(bag)
        except:
            e = sys.exc_info()[0]
            print("FAILED Attempt # %d of %d" % (N_try,N_try_max))
            print(e) # unfortunately printing "e" or "e.message" is not very helpful
            if N_try < N_try_max:
                my_sleep_time = 30 * ( N_try ** 2 ) # sleep time grows with number of tries
                print(f"sleeping {my_sleep_time} seconds after N_try = {N_try} for {bag.mylabel}")
                time.sleep(my_sleep_time)

    if not bag.success_flag:
        print("FATAL ERROR, failed to get data after several attemtps, exiting ...")
        sys.exit(1)

# ---------------------------------
    print("Returned from run_query(bag) at %s\n" % (now_str()))
    t2 = time.time()
    print("Total query+data_transfer took %s seconds" % (commify(t2-bag.t1,2)))
    print("Converting result into pandas DataFrame ...\n")
    df = conv_res_to_df(result)
    if test_avail(bag2, "df"):
        print("appending %s rows into bag2.df" % (commify(len(df))))
        bag2.df = pd.concat([bag2.df,df], ignore_index=True)
    else:
        print("starting %s rows into bag2.df" % (commify(len(df))))
        bag2.df = df.copy()
    del df
    t2 = time.time()
    print("len(bag2.df) = ", commify(len(bag2.df)) )
    print("DONE for interval %s" % bag.mylabel, "elapsed seconds = %s" % (commify(t2-bag.t1,2)))
    return bag
    # ---------------------------------


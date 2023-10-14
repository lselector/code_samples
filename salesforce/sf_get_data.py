"""
# sf_get_data.py
# runs SOQL query - and produces CSV file 
# Always uses timeout and tries several times on failure
#
# uses modules from 
#   https://github.com/lselector/setup_computer/tree/master/py_lib
# also module simple_salesforce
"""

import os, sys, time, gc
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
from myutil import *
from myutil_dt import *
from my_sf_api import *
from wrapt_timeout_decorator import *

# ---------------------------------------------------------------
def run_query(bag):
    """ 
    # procedure to run individual query
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
def extract_soql(bag, bag2):
    """
    # Extracts data from Salesforce for a given label and object.
    # label indicates time interval (all, year, month)
    # object indicates the object in Salesforce
    # converts to pandas DataFrame - and appends to bag2.df
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
        print("Running Query\n" + bag.soql + "\n ... \n")
        try:
            # run_query(bag)
            bag,result = timeout(dec_timeout=bag.arg_timeout, use_signals=False)(run_query)(bag)
        except:
            e = sys.exc_info()[0]
            print("FAILED Attempt # %d of %d" % (N_try,N_try_max))
            print(e) # unfortunately printing "e" or "e.message" is not very helpful
            time.sleep(2)

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
        bag2.df = bag2.df.append(df, ignore_index = True)
    else:
        print("starting %s rows into bag2.df" % (commify(len(df))))
        bag2.df = df.copy()
    del df
    t2 = time.time()
    print("len(bag2.df) = ", commify(len(bag2.df)) )
    print("DONE for interval %s" % bag.mylabel, "elapsed seconds = %s" % (commify(t2-bag.t1,2)))
    return bag
    # ---------------------------------
    
# ---------------------------------------------------------------
def main(bag):
    """
    # main execution
    """
    mylog(bag, "in main")
    # ---------------------------------
    soql_orig = "SELECT some fields from some object where ..." # XXXXXXXXXXXX
    # ---------------------------------
    # create a list of tuples (label, SOQL)
    mytuples = []
    mytuples += [soql_orig]   # ... (by month, year, ...)

    # ---------------------------------
    # connect to Salesforce
    bag.sf = get_sf(myurl=url_prod, params=params_prod) 

    # ---------------------------------
    # run all queries one by one
    for mylabel, soql in mytuples:
        if bag.arg_lim > 0:
            soql += "\n    LIMIT %d" % bag.arg_lim
        bag.mylabel = mylabel
        bag.soql    = soql
        extract_soql(bag,bag2)
        gc.collect()
    # ---------------------------------
    # if we are here - this means that all yearly queries were
    # successful and all results are saved in bag2.df
    fname = "/mydir/extract_%s.csv" % bag.arg_obj 
    print("writing %s rows to file %s" % (commify(len(bag2.df)), fname))
    bag2.df.to_csv(fname, index=False)
    print("File created")

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
if __name__ == "__main__":
    bag  = MyBunch()
    bag2 = MyBunch()
    bag.mask_log_str = ""
    myinit(bag)
    print_start_time(bag)
    # ------------------------
    main(bag)
    # ------------------------
    print_timing(bag)
    print_elapsed_time(bag)


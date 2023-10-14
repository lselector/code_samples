"""
# runs Salesforce query, outputs CSV to STDOUT
#
# Usage:
#   python soql.py -l=5 -p -q 'select Id from SomeObject'
#
# where parameters:
#    -q '...' - to specify SOQL query
#    -l N     - optional, adds  " LIMIT N" to SOQL query
#    -p       - optional, use production environment
# 
# uses modules from 
#   https://github.com/lselector/setup_computer/tree/master/py_lib
# also module simple_salesforce
"""

import os
import sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
from myutil import *
from myutil_dt import *
from my_sf_api import *

# ---------------------------------------------------------------
def process_cmd_args(bag):
    """
    # processes cmd arguments - and populates bag.arg_* 
    #     -l - limit number
    #     -q - query
    #     -p - production flag
    """
    descr_str = """script to run SOQL and output CSV data to STDOUT"""
    bag.app.parser = argparse.ArgumentParser(description=descr_str)

    bag.app.parser.add_argument('-l', '-lim', '--lim', action='store',
        dest='arg_lim', default=0, help="optional number of rows (LIMIT)")
    bag.app.parser.add_argument('-q', action='store',
        dest='arg_query', default='', help="required - SOQL query to run")
    bag.app.parser.add_argument('-p', '-prod',  '--prod', action='store_true',  
        dest='arg_prod', help="""optional - flag to query production""")

    parsed, unknown = bag.app.parser.parse_known_args()
    if len(unknown):
        exit_with_error(bag, "unrecognized argument(s) " + str(unknown))

    bag.arg_lim   = 0
    bag.arg_query = ""
    bag.arg_prod  = False

    if parsed.arg_lim:
        bag.arg_lim = int(float(parsed.arg_lim))
    if parsed.arg_query:
        bag.arg_query = str(parsed.arg_query).strip()
    if parsed.arg_prod:
        bag.arg_prod = True

    print("arg_lim   = ", bag.arg_lim)
    print("arg_query = ", bag.arg_query)
    print("arg_prod  = ", bag.arg_prod)

# ---------------------------------------------------------------
def main(bag):
    """
    # main execution
    """
    mylog(bag, "in main")
    process_cmd_args(bag)
    # --------------------------------------------------------------

    soql = bag.arg_query
    if bag.arg_lim > 0:
        soql += "\n    LIMIT %d" % bag.arg_lim

    # --------------------------------------------------------------
    if bag.arg_prod:
        sf = get_sf(myurl=url_prod, params=params_prod)
    else:
        sf = get_sf(myurl=url_sand, params=params_sand)

    t1 = time.time()
    # --------------------------------------------------------------
    print("Running Query\n" + soql + "\n ... \n")
    result = sf.query_all(soql)
    print("\nQuery finished, received records:", result['totalSize'])
    t2 = time.time()
    print("Finished query: elapsed seconds = %.3f" % (t2-t1))

    # --------------------------------------------------------------
    print("Converting result into pandas DataFrame ...\n")
    df = conv_res_to_df(result)
    t2 = time.time()
    print("Finished df: elapsed seconds = %.3f" % (t2-t1))
    # --------------------------------------------------------------
    print(df.to_string())
    t2 = time.time()
    print("\nDONE, elapsed seconds = %.3f" % (t2-t1))

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    bag.mask_log_str = ""
    myinit(bag)
    print_start_time(bag)
    # ------------------------
    main(bag)
    # ------------------------
    print_timing(bag)
    print_elapsed_time(bag)


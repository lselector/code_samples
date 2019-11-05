#! /bin/env python2.7

"""
# test_excel2df.py
# read Excel file into pandas DataFrame
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys

import myutil
reload(myutil)
from myutil import *

# ---------------------------------------------------------------
def main(bag):
    """
    # main - reading excel file
    """
    myinit(bag)
    bag.mask_log_str = ""
    # ----------------------------------
    fname = 'files/cdi_pref_mapping.xlsx'
    sheet_name = 'ESP Pref Type & Value'
    print "opening file", fname
    xf = pd.ExcelFile(fname)
    sheets = [sname for sname in xf.sheet_names]
    print "sheet names = ", sheets
    df =  xf.parse(sheet_name)
    print df
    # ----------------------------------

# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)

#! /bin/env python2.7

""" 
# test_df2excel.py
# Script to test writing into Excel file 
#     files/simple.xlsx
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys
import xlsxwriter

import ipython_debug
reload(ipython_debug)
from ipython_debug import *

import myutil
reload(myutil)
from myutil import *

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
bag=MyBunch()

bag.data_fname = 'files/data.tsv'
print "read file", bag.data_fname
bag.txt = slurp(bag.data_fname)

print "reset 8th bit"
bag.txt2, counter = reset_8th_bit(bag.txt)
print "reset done in %d chars" % counter

print "Create a Pandas dataframe from the data."
from StringIO import StringIO
bag.df=DataFrame.from_csv(StringIO(bag.txt2),sep='\t', index_col=None, parse_dates=False)

print "Create a Pandas Excel writer using xlsxwriter as the engine."
bag.excel_fname = "files/simple.xlsx"
writer = pd.ExcelWriter(bag.excel_fname, engine='xlsxwriter')

mysheet = 'data'
print "Write dataframe to sheet", mysheet 
bag.df.to_excel(writer, sheet_name=mysheet)

print "Close the Pandas Excel writer and output the Excel file", bag.excel_fname
writer.save()

print "DONE"

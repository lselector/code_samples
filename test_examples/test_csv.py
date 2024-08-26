#! /bin/env python2.7


""" 
    Script to test reading CSV files into python
    integer numbers up to 16 digits are loaded as int64 without errors.
    Bigger numbers should probably be converted to float to avoid problems
"""


import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame, Series


lines = [
    "aa,bb",
    "1,2147483647,2147483647.0",
    "2,21474836470,21474836470.0",
    "3,214748364701,214748364701.0",
    "4,2147483647001,2147483647001.0",
    "5,12345678901234,12345678901234.0",
    "6,123456789012345,123456789012345.0",
    "7,1234567890123456,1234567890123456.0",
    "8,12345678901234567,12345678901234567.0",
    "9,123456789012345678,123456789012345678.0",
    "10,1234567890123456789,1234567890123456789.0",
    "11,4611686014132420609,4611686014132420609.0"
  , "12,10611686014132420611,9000000000000000000.0"
# ,"13,12345678901234567890,12345678901234567890.0"
    ]
txt = '\n'.join(lines) + '\n'


fname = 'files/junk.csv'
f = file(fname,'w')
f.write(txt)
f.close()


DF = pd.read_csv(fname,sep=',')
os.remove(fname)

print DF
print DF.dtypes
DF.bb = DF.bb.map(np.int)


#  output:
#  
#                       aa            bb
#  1            2147483647  2.147484e+09
#  2           21474836470  2.147484e+10
#  3          214748364701  2.147484e+11
#  4         2147483647001  2.147484e+12
#  5        12345678901234  1.234568e+13
#  6       123456789012345  1.234568e+14
#  7      1234567890123456  1.234568e+15
#  8     12345678901234568  1.234568e+16
#  9    123456789012345680  1.234568e+17
#  10  1234567890123456768  1.234568e+18
#  11  4611686014132420608  4.611686e+18
#  12  4611686014132420608  4.611686e+18
#  13 -9223372036854775808  1.234568e+19
#  aa      int64
#  bb    float64

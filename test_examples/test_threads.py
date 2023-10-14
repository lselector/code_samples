#! /bin/env python2.7

"""
# test_threads.py
# this script allows to easily see threads created by
# importing the pandas module.
# if you don't import pandas - there is only one thread
# if you import pandas (even if you don't use it),
# there may be several threads.
#
# Pandas prior to version 17 was not using threads.
# So the threads you see when using /usr/local/bin/python
# are there because of some pandas' dependencies
# (not sure which ones).
# 
# If you use anaconda - you use pandas version 17, which 
# releases GIL (Global Interpreter Lock) on groupby operations
# (for speed):
#   - https://www.continuum.io/content/pandas-releasing-gil
#
# to see the threads created while running this script,
# just open "htop" in another window, press F5 to see trees,
# and press <SHIFT>-h to toggle "view threads"
"""

import sys, os, time, platform
print("python: " + sys.executable)
print(sys.version.split("\n")[0] + "| " + str(platform.architecture()[0]))

# --------------------------------------------------------------
# uncomment next two line to control number of threads created in pandas
# os.environ["NUMEXPR_NUM_THREADS"] = "5"
# os.environ["OMP_NUM_THREADS"] = "5"

# --------------------------------------------------------------
import pandas # adding this line adds threads in HTOP
print pandas.__version__

# --------------------------------------------------------------
while True:
    time.sleep(1)
    print "Hello"


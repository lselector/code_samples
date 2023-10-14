#! /bin/env python2.7

""" 
# test_format.py
# a demo of how to use Python .format() feature
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

# ---------------------------------------------------------------
print "-"*30
ss1 = "dog"
ss2 = "mouse"
print "empty curlies1 {}".format(ss1)
print "empty curlies2 {} {}".format(ss1,ss2)
print "cat {0} {1} {0}".format(ss1,ss2)            # by index
print "cat {w1} {w2} {w1}".format(w1=ss1, w2=ss2)  # by name

mylist = range(5)
print mylist
print "[{4}, {3}, {2}, {1}, {0}]".format(*mylist)  # by index

print '{0}, {0}'.format('test')   # repeating same thing

# passing arguments to format using map()
mylist = [11, 22, 33, 44]
print map('number: {}'.format, mylist)  

# --------------------------------------
print "-"*30
print "using formats for date and time"
from datetime import datetime,timedelta
mydate = datetime(2010, 7, 1, 12, 0, 0)
mydelta = timedelta(days=13, hours=8,  minutes=20)
mygen =(mydate +xx*mydelta for xx in xrange(5))

print '\n'.join(map('{:%Y-%m-%d %H:%M:%S}'.format, mygen))

# --------------------------------------
print "-"*30
print "width and right/left aligning"
ss = 'mama'
print ">>>{:>10s}<<<".format(ss)       # >>>      mama<<<
print ">>>{:<10s}<<<".format(ss)       # >>>mama      <<<
print ">>>{0:<10s}<<<".format(ss)      # >>>mama      <<<
print ">>>{w1:<10s}<<<".format(w1=ss)  # >>>mama      <<<

num = 12.34567
for ii in [9,11,13,15]:
    fmt = "{0:0"+str(ii)+".2f}"
    print fmt.format(num)
    fmt = "{0:>"+str(ii)+".2f}"
    print fmt.format(num)
    fmt = "{0:<"+str(ii)+".2f}"
    print fmt.format(num)
    print "-"*30
# --------------------------------------
print "-"*30
print "f, e, and g formats"
num = 12.3456e-10
print "g   : >>>{:g}<<<".format(num)   # >>>1.23456e-09<<<
print "e   : >>>{:e}<<<".format(num)   # >>>1.23456e-09<<<
print "f   : >>>{:f}<<<".format(num)   # >>>0.000000<<<

print ".3g : >>>{:.3g}<<<".format(num)   # >>>1.23e-09<<<
print ".3e : >>>{:.3e}<<<".format(num)   # >>>1.235e-09<<<

# --------------------------------------
print "-"*30
print "testing what is faster:"
import timeit
rep=int(5e7)
timer1 = timeit.Timer("{0}, {1:.1f}".format(4, 2.2345))
t1 = timer1.timeit(rep)/rep
print "using format  (sec): %g" % t1
timer2 = timeit.Timer("%d, %.1f" %(4, 2.2345))
t2 = timer2.timeit(rep)/rep
print "using C-style (sec): %g" % t2
print "-"*30

# --------------------------------------
print "Be careful with unicode"
ss = '\xd0\xb9'    # byte array - string of 2 bytes
uu = u'\u0439'     # unicode string = string in Python3

print "%% ss prints OK: %s" % str(ss)  # '\xd0\xb9'
try:
    print "%% uu gives error: %s" % str(uu)  # u'\u0439'
except Exception as ee:
    print "% uu gives error:"
    print "ERROR >>>", ee

print "format(ss) OK: {}".format(ss)

try:
    print "format(uu) error: {}".format(uu)
except Exception as ee:
    print "format(uu) error:"
    print "ERROR >>>", ee

print "now let's try with unicode format string" 
print u"unicode format(uu) OK: {}".format(uu)

# --------------------------------------

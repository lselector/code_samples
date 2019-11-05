#! /bin/env python2.7

""" 
# script calculates 1000 digits of number pi
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1"

import myutil
reload(myutil)
from myutil import *

# --------------------------------------------------------------
def make_pi():
    """
        # the algorithm is described here:
        # http://mail.python.org/pipermail/edu-sig/2006-July/006810.html
        # http://www.cs.ox.ac.uk/people/jeremy.gibbons/publications/spigot.pdf
        # this procedure is a generator which on each call returns 
        # returns next digit of pi using   yield m
    """
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    for j in range(1000):
        if 4 * q + r - t < m * t:
            yield m
            q, r, t, k, m, x = 10*q, 10*(r-m*t), t,   k,   (10*(3*q+r))//t - 10*m, x
        else:
            q, r, t, k, m, x =  q*k,  (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2


# --------------------------------------------------------------
def make_pi2():
    """
        # 4.0*(1 - 1/3 + 1/5 - 1/7 + 1/9 - . . .)
    """
    N = int(1e6)
    nn = 1.0
    for ii in range(1,N):
        kk = 1.0/(2.0*ii+1.0)
        if ii % 2 == 1 :
            kk = -1.0 * kk
        # print kk
        nn = nn + kk
    return nn * 4.0


# ##############################################################
# main execution
# ##############################################################
digits   = make_pi()
pi_list  = []
my_array = []
# -------------------------------------
for i in make_pi(): 
    my_array.append(str(i))
my_array = my_array[:1] + ['.'] + my_array[1:]
print "make_pi(): " + "".join(my_array)
# -------------------------------------
pi2 = make_pi2()
print "make_pi2(): " + str(pi2)
# -------------------------------------

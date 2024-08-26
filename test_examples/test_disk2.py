#!env python2.7

"""
# simple script to test disk write speed
# Usage:
#   python  test_disk2.py 

"""
import time
import os
import subprocess

# ---------------------------------------------------------------
# set testpath
# ---------------------------------------------------------------
if os.path.exists('/bin'):
    unix_flag = True
#    testpath = os.environ['HOME']
#    testpath = "/dw_farm1"
    testpath = "/tmp"
else:
    unix_flag = False
    testpath = os.environ['userprofile']

print "path to write tmp file:", testpath
# ---------------------------------------------------------------
mycount = 1024
mystr   = "0123456789ABCDEF" * 65535 + "0123456789ABCDE\n" # 1MB
bytes_in_mb = 1024*1024
file_size = 1.0*len(mystr)*mycount/bytes_in_mb
fname = testpath+"/"+"junk_mytest.txt" 
if os.path.isfile(fname):
    os.remove(fname)
# ---------------------------------------------------------------
print "writing %.2f MB file %s" % (file_size, fname)
for tt in range(3):
    if unix_flag: subprocess.call("sync")
    t1 = time.time()
    fh = open(fname, "w")
    for ii in range(mycount):
      fh.write(mystr)
    fh.close()
    if unix_flag: subprocess.call("sync")
    dt = time.time() - t1
    speed = file_size / dt
    print "  write speed = %.3f MBytes/sec" % speed

# ---------------------------------------------------------------
print "Finished"
if os.path.isfile(fname):
    os.remove(fname)
# ---------------------------------------------------------------

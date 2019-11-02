#! /usr/bin/env python

""" 
# simple script to test disk write speed
# USB2   -     22 MBytes/sec 
# USB3   -     60 MBytes/sec (using PatriotSupersonic Magnum 128 GB)
# local HD -  300 MBytes/sec
# server   - 1000 MBytes/sec
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

import sys
import subprocess
import time

# --------------------------------------------------------------
def run_cmd(mycmd, verbose=True):
    """
    # simple wrapper to run a system command
    """
    if verbose :
        print(mycmd)
    rc = subprocess.call(mycmd, shell=True)
    return rc

# --------------------------------------------------------------
# main execution
# --------------------------------------------------------------
print("START")

disk1 = '/tmp'
disk2 = '/var/tmp'
# disk2 = '/Volumes/PATRIOT'

sname    = 'junk.img'
mb       = 1024*1024
fsize_mb = 512
fsize_b  = fsize_mb * mb # Bytes
N        = 10

print("creating temporary file %s/%s" % (disk1,sname))
mycmd = 'dd if=/dev/zero of=%s/%s bs=%d count=%d' % (disk1, sname, mb, fsize_mb)
run_cmd(mycmd)

print("starting the test")
mycmd = '/bin/cp -f -a %s/%s %s/' % (disk1, sname, disk2)
time_start = time.time()
for ii in range(1,N+1):
    run_cmd('sync', verbose=False)
    run_cmd(mycmd)
    run_cmd('sync', verbose=False)
    dt = time.time() - time_start
    speed = (1.0 * ii * fsize_b / dt) / mb  # in MBytes/sec
    print('(%2d of %2d) average %.2f MBytes/sec' % (ii,N,speed))

print("removing temporary files")
run_cmd('/bin/rm -f %s/%s' % (disk1, sname) )
run_cmd('/bin/rm -f %s/%s' % (disk2, sname) )

print('DONE')


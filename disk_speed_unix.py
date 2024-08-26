#! /usr/bin/env python

""" 
# disk_speed_unix.py
# Usage:
#     python disk_speed_unix.py
#
# simple script to test disk write speed
# depends on 
#     unix
#     python 3.6 or later
# script runs unix commands:
#     sync
#     cp -f -a /tmp/junk.img /var/tmp/junk.img
#     sync
"""

import os, os, subprocess, time
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

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
N        = 10  # times to repeat

# --------------------------------------------------------------
print(f"creating temporary file {disk1}/{sname} of size {fsize_mb} MBytes")
# mycmd = f"dd if=/dev/zero of={disk1}/{sname} bs={mb} count={fsize_mb}"
# run_cmd(mycmd)

# string 1 MBytes
mystr   = "0123456789ABCDEF" * 65535 + "0123456789ABCDE\n" # 1MB

fname = f"{disk1}/{sname}"
fh = open(fname, "w")
for ii in range(fsize_mb):
    fh.write(mystr)
fh.close()
# --------------------------------------------------------------
print("starting the test using the /bin/cp command")
mycmd = f"/bin/cp -f -a {disk1}/{sname} {disk2}/"
time_start = time.time()

for ii in range(1,N+1):
    run_cmd('sync', verbose=False)
    run_cmd(mycmd)
    run_cmd('sync', verbose=False)

    dt = time.time() - time_start
    speed = (1.0 * ii * fsize_b / dt) / mb  # in MBytes/sec
    print(f"({ii:2d} of {N:2d}) average {speed:.2f} MBytes/sec")

# --------------------------------------------------------------
print("removing temporary files")
run_cmd( f"/bin/rm -f {disk1}/{sname}" )
run_cmd( f"/bin/rm -f {disk2}/{sname}" )

print('DONE')

# --------------------------------------------------------------

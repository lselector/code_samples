#! python

""" 
# disk_speed_windows.py
# Usage:
#   open CMD window
#   go to the disk you want to test
#   run the script there
#     python  disk_speed_windows.py
#   Note - it will create temporary files
#          at that location
#
# This simple script to test disk write speed
# depends on
#     Windows
#     python 3.6 or later
# script runs dos commands:
#     copy /Y junk.img junk1.img
# the files are created in the same directory
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

sname1 = 'junk1.img'
sname2 = 'junk2.img'

mb       = 1024*1024
fsize_mb = 512
fsize_b  = fsize_mb * mb # Bytes
N        = 10  # times to repeat

# --------------------------------------------------------------
print(f"creating temporary file {sname1} of size {fsize_mb} MBytes")
# testpath = os.environ['userprofile']
# print "path to write tmp file:", testpath

# string 1 MBytes
mystr   = "0123456789ABCDEF" * 65535 + "0123456789ABCDE\n" # 1MB

fh = open(sname1, "w")
for ii in range(fsize_mb):
    fh.write(mystr)
fh.close()
# --------------------------------------------------------------
print("starting the test using the copy command")
mycmd = f"copy /Y {sname1} {sname2}"
time_start = time.time()

for ii in range(1,N+1):
    run_cmd(mycmd)
    dt = time.time() - time_start
    speed = (1.0 * ii * fsize_b / dt) / mb  # in MBytes/sec
    print(f"({ii:2d} of {N:2d}) average {speed:.2f} MBytes/sec")

# --------------------------------------------------------------
print("removing temporary files")
for fname in [sname1, sname2]:
    if os.path.isfile(fname):
        os.remove(fname)

print('DONE')

# --------------------------------------------------------------

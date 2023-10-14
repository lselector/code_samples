
"""
# kill_stale_ssh_remote_processes.py 
# 
# script to kill stale processes (like jupyter kernels)
# left behind on the server after using VS Code Remote SSH
#
# myutil and other modules are in different repo:
#   setup_computer/py_lib/
#
# by Lev Selector, 2022
"""

import os, sys, time, subprocess
import os.path
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
from myutil import *
from myutil_dt import *

# ---------------------------------------------------------------
def myrun(cmd):
    """ simple function to run shell command and return a string """
    try:
        txt = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        txt = e.output
    txt = txt.decode().strip()
    return txt

# ---------------------------------------------------------------
def our_processes(bag):
    """ show our non crontab and non web processes """
    print()
    cmd  = f"ps -eo user,pid,ppid,lstart,etime,args --sort start_time "
    cmd += f" | grep -P 'python -m ipykernel_launcher' "
    cmd += f" | grep -P '/home/dsadmin/.local/share/jupyter/runtime/kernel' "
    cmd += f" | grep -P '.json' | grep -v grep "
    run_lst = myrun(cmd).split("\n")
    for ww in run_lst:
        print(ww)
    print()
    run_lst = [i.strip() for i in run_lst if len(i.strip())]
    for ww in run_lst:
        print(ww)
    print()
    # -----------------------------
    def pid_json(ii):
        mylist = ii.split()
        return (mylist[1], mylist[-1])

    json_files = [ pid_json(ii) for ii in run_lst if len(ii)]
    for ww in json_files:
        print(ww)
    print()
    print("find and show missing json files (if any):")
    json_files = [ff for ff in json_files if not os.path.isfile(ff[1])]
    for ww in json_files:
        print(ww)
    print()
    mynum = len(json_files)
    if mynum > 0:
        print(f" {mynum} of ipykernel_launcher processes with missing json file:")
        cmd = "ps -eo user,pid,ppid,lstart,etime,args | head -1"
        txt = myrun(cmd)
        print(txt)
        for elem in json_files:
            pid = elem[0]
            fname = elem[1]
            print(f"killing pid {pid} for missing file {fname}")
            cmd = f"kill {pid}"
            ret = myrun(cmd)

# ---------------------------------------------------------------
def main(bag):
    """
    # main execution
    """
    our_processes(bag)
    print("-"*50)

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
if __name__ == "__main__":
    bag  = MyBunch()
    bag.mask_log_str = ""
    myinit(bag)
    main(bag)

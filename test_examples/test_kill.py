#! /bin/env python2.7

"""
# --------------------------------------------------------------
# test_kill.py (also test_kill_c.py)
# test of how to trap signals,
# and how to kill all child subprocesses
# (also how to run subprocesses with timeout).
#
# http://en.wikipedia.org/wiki/Unix_signal#POSIX_signals
# http://stackoverflow.com/questions/2148888/python-trap-all-signals
# http://unix.stackexchange.com/questions/124127/kill-all-descendant-processes
# http://unix.stackexchange.com/questions/68754/kill-a-group-of-processes-with-negative-pid
# http://www.linuxquestions.org/questions/programming-9/use-only-one-kill-to-kill-father-and-child-processes-665753/
# 
# --------------------------------------------------------------
# When you create a subprocess object using 
#   proc = subprocess.Popen(cmd,shell=True)
# you can later terminate it using
#   proc.terminate()
# Alternatively you can get its pid (as proc.pid)
# and then work with it (kill, check) using pid number.
# This script uses pid approach.
# --------------------------------------------------------------
# We will use unix "kill" command. 
# Here are some examples of using kill and pkill:
#     kill -l  (small L - to show the list of signals you can send)
#         SIGKILL = kill -9, can not be caught
#         SIGTERM = kill -15
#         SIGINT = ctrl-C = kill -2
#     kill PID      # SIGTERM
#     kill -15 PID  # same
#     kill -9  PID  # SIGKILL
#     kill -1 (one - to kill all processes of the user - dangerous)
#     kill -- -GPID - kill all processes in the same group as GPID
#         Note: if the first pid operand is negative, it should be preceded 
#               by "--" to keep it from being interpreted as an option
#     kill -TERM -- -GPID
#     pkill -TERM -g 28367
#     pkill -TERM -P PARENT_PID
#     pkill -P $$   ($$ expands to the PID of the current shell) - kill all children.
#     kill 0
#     setsid <your_program>     # will create new process group
#     kill $(ps -s $$ -o pid=)  # using SID
#
# --------------------------------------------------------------

# You can kill processes individually or by group
# I played with killing all processes in the group
# but it kills the parent before it gracefully printing the exit summary
# So I ended up using this sequence:
#     kill_pid(pid, 15)  # SIGTERM
#     remove_zombies()
#     time.sleep(2) # get some time for process to die
#     kill_pid(pid, 9)   # SIGKILL
#     remove_zombies()
# 
# --------------------------------------------------------------
# To poll/check on processes we will be using: 
#     os.kill(pid,0)
#     os.waitpid(pid, WNOHANG)
# --------------------------------------------------------------
# os.waitpid(pid, options)
#    Wait for completion of a child process given by process id pid, 
#    and return a tuple containing its process id and exit status 
#    indication (encoded as for wait()). 
#    normally options == 0
#    options=WNOHANG - will only return the status, will not wait
#    if pid > 0:
#        # processes this specific pid
#    elif pid ==0:
#        # processes any child of the same group
#    elif pid = -1:
#        # processes any child of the current process
#    elif pid < 0:
#        # processes any process in the process group -pid
# --------------------------------------------------------------
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys
import subprocess
import time
import signal

import myutil
reload(myutil)
from myutil import *

# --------------------------------------------------------------
def remove_zombies():
    """
    # prevents accumulating of child processes in defunct state
    # basically polling all processes in the group
    # the fact of pollins is enough to remove the zombie
    """
    try:
        ret = os.waitpid(-1, os.WNOHANG)
    except:
        print "in remove_zombies: no subprocesses left"
        return

# --------------------------------------------------------------
def check_pid(pid):        
    """ 
    # check for the existence of a pid.
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

# --------------------------------------------------------------
def kill_pid(pid, signum):
    """
    # uses system kill command
    """
    if not check_pid(pid):
        return
    mycmd = "kill -%d %d" % (signum, pid) 
    print mycmd
    ret = subprocess.call(mycmd, shell=True)
    remove_zombies()

# --------------------------------------------------------------
def check_list(pid_list):
    """
    # checks if pids exist
    # returns only a lsit of existing pids
    """
    newlist = []
    for pid in pid_list:
        if check_pid(pid):
            newlist.append(pid)
    return newlist

# --------------------------------------------------------------
def kill_list(pid_list, signum=15, verbose=False):
    """
    # kill_pid() for each member of the list
    """
    for pid in pid_list:
        if verbose:
            print "trying to kill -%d %d" % (signum, pid)
        kill_pid(pid, 15)  
    remove_zombies()

# --------------------------------------------------------------
def kill_child_procs(pid_list):
    """
    # kill all processes in the provided list
    """
    kill_list(pid_list) # SIGTERM
    plist = pid_list
    ii = 0
    while (ii < 2) and (len(plist)):
        time.sleep(3)
        plist = check_list(plist)
        kill_list(pid_list, signum=9, verbose=True) # SIGKILL
    plist = check_list(plist)
    if len(plist):
        print "ERROR - couldn't kill child processes", plist
        raise
    else:
        print "All subprocesses terminated OK"

# --------------------------------------------------------------
def myexit_handler(signal, frame):
    """
    # this is executed on Ctrl-C or kill
    # it kills all subprocesses before exiting.
    """
    global procs
    kill_child_procs(procs)
    raise

# --------------------------------------------------------------
# main execution
# --------------------------------------------------------------
if __name__ == "__main__":

    # ---------------------------------
    # set handler to get invoked on Ctrl-C and on "kill"
    # the handler should kill all subprocesses before exiting.
    signal.signal(signal.SIGTERM, myexit_handler)
    signal.signal(signal.SIGINT, myexit_handler)
    
    # ---------------------------------
    # start several subprocesses
    myscript = "test_kill_c.py"
    procs = []
    for ii in range(3):
        p = subprocess.Popen(myscript, shell=True)
        procs.append(p.pid)
    print "started processes", procs

    # ---------------------------------
    time.sleep(7)
    print "finished sleeping, time to kill"
    kill_child_procs(procs)

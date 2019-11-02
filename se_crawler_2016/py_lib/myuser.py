
"""
# myuser.py - functions to get user
# Created in Aug 2015 by Lev Selector
"""

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
import sys
if sys.version_info > (3,3):
    import importlib
 
import subprocess

myuser = os.environ['USER']

# --------------------------------------------------------------
def running_from_crontab():
    """
    # uses the fact that when running from crontab,
    # command 'who am i' returns empty string.
    """
    output = subprocess.check_output('who am i', shell=True)
    if len(output) <= 0:
        return True
    else:
        return False

# --------------------------------------------------------------
def my_real_user():
    """
    # shows your real personal user (even if you became other user)
    # uses the fact that command 'who am i' shows your real user name
    # (commands id, echo $USER, whoami will show sudo name)
    # Note - when running from crontab, command 'who am i'
    # returns empty string. So we use 'whoami' instead.
    """
    output = subprocess.check_output('who am i', shell=True)
    if len(output) <= 0:
        output = subprocess.check_output('whoami', shell=True)
    words = output.split()
    return words[0]


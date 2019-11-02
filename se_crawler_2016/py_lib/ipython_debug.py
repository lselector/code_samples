
"""
# import like this
#
# import ipython_debug
# reload(ipython_debug)
# from ipython_debug import debug_here
"""

import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"
import sys

# --------------------------------------------------------------
def run_from_ipython():
    """
    # boolean test if we are running from ipython
    """
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

# --------------------------------------------------------------
def sys_exit_1():
    """
    # this function is called instead of Tracer
    # when running script without iPython
    """
    print("debug_here() only works in iPython. Exiting...")
    sys.exit(1)

# --------------------------------------------------------------
# The code below is executed when importing this module
# It adds function debug_here() to enter iPython debugger
# When running without iPython, it will do sys.exit(1) isntead.
# --------------------------------------------------------------
if run_from_ipython():
    # import Tracer class
    from IPython.core.debugger import Tracer
    # get yourself a tracer
    debug_here = Tracer()
else:
    debug_here = sys_exit_1

#! env python

"""
# timeout implementation from python
#   pip install wrapt_timeout_decorator
# has two methods: signals and multiprocessing
"""

import time
from wrapt_timeout_decorator import *

N = 10
TIMEOUT = 3

# --------------------------------------------------------------
def run_mytest(message):
    print(message)
    for ii in range(1,10):
        time.sleep(1)
        print(f'{ii} seconds have passed')

# --------------------------------------------------------------
ss = f"Starting {N} cycles with timeout after {TIMEOUT}"

try:
    timeout(dec_timeout=TIMEOUT,use_signals=False)(run_mytest)(ss)
    print("OK")
except:
    print("ERROR - timeout")




"""Logging config in main.py"""

import logging
import myapp_logger as dl

logger = logging.getLogger("myapp")
dl.setup_logging(logger)
logging.basicConfig(level="INFO")
dl.example_logging(logger) 

# --------------------------------------------------------------
"""
in other files just add two lines at top:

import logging
logger = logging.getLogger("myapp")
"""
# --------------------------------------------------------------
"""
# Python logging 
# https://docs.python.org/3/library/logging.html

Python Logging Tutorisl (15 min)
https://www.youtube.com/watch?v=urrfJgHwIJA

Modern Python logging
https://www.youtube.com/watch?v=9L77QExPmI0
https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging
"""

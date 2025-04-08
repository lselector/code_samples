Examples of using Python logging

lesson1.py & lesson2.py - examples

files starting with "myapp_" show a practical example

usage:
in the main file of your app:

    import logging
    import myapp_logger as dl
    logger = logging.getLogger("myapp")
    dl.setup_logging(logger)
    logging.basicConfig(level="INFO")

in other files/modules of your app:

    import logging
    logger = logging.getLogger("myapp")

then you can do logger.info(), etc. everywhere

The config and utility functions are in two files;
    myapp_logger.py
    myapp_logger_config.json

Here are sources used in creating these examples:


Python logging docs
https://docs.python.org/3/library/logging.html

Python Logging Tutorisl (15 min)
https://www.youtube.com/watch?v=urrfJgHwIJA

Modern Python logging (21 min)
https://www.youtube.com/watch?v=9L77QExPmI0
https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging

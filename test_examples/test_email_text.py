#! /bin/env python2.7

""" 
# test_email_text.py
# using smtplib.SMTP.sendmail to send plain text message
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
from datetime import datetime
import smtplib

# appmail.randomhouse.com, mymail.randomhouse.com, rhmailer.rhbss.com
my_smtp_server = 'mymailer.mydomain.com' 
my_smtp_port   = 25
myemail = 'a@b.com'
myuser  = myemail
now_str = datetime.now().strftime("%H:%M:%S")
my_to   = myemail
my_from = myemail
chunks = [
    'To:' + my_to,
    'From: ' + my_from,
    'X-Priority:2',
    'Subject:testing',
    "test at %s\n\n" % now_str
]    
msg_str =  '\n'.join(chunks)

session = smtplib.SMTP(my_smtp_server, my_smtp_port)
# session.set_debuglevel(1)
session.sendmail(my_from, my_to, msg_str)
session.close()


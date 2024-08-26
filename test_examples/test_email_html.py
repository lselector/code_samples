#! /bin/env python2.7


""" 
# test_email_html.py
# send html or plain text message to several recepients
# http://stackoverflow.com/questions/882712/sending-html-email-in-python
# note - also includes a simple dataframe in the body of the message
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import socket

myhost=socket.gethostname()
my_smtp_server = 'mymailer.mydomain.com'
sender   = 'a@b.com'    # CHANGE THAT BEFORE RUNNING
to_list  = [sender]

# Create message container - the correct MIME type is multipart/alternative.
msg             = MIMEMultipart('alternative')
msg['Subject']  = "Email HTML with a link and pandas DataFrame data"
msg['From']     = sender
msg['To']       = ', '.join(to_list) # this is a comma-separated list

# Create the body of the message (a plain-text and an HTML version).
mytext = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
myhtml = """\
<html>
    <head></head>
    <body>
        <p>Hi!<br>
              <font color="FF3333">How are you?</font><br>
              Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
        Here is a dataframe:<br><br>
        __DATAFRAME1__
        <br>
        <p>
        Warm Regards<br>
        Lev Selector
        </p>
    </body>
</html>
"""

df = DataFrame({'Name':['Client1','Client2','Client3'],
                                'Clicks':[123456,np.nan,4567],
                                'Money':[123456,np.nan,4567]})

df_html = df.to_html(columns=['Name','Clicks','Money'],na_rep=' - ')

myhtml = myhtml.replace("__DATAFRAME1__", df_html)


# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(mytext, 'plain')
part2 = MIMEText(myhtml, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message is preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message
s = smtplib.SMTP(mysmtpserver)
s.sendmail(sender, to_list, msg.as_string())
s.quit()



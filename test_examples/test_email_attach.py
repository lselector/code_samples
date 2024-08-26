#! /bin/env python2.7

""" 
    # test_email_attach.py
    # sends one or more attachments
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import smtplib
import mimetypes
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import socket
myhost=socket.gethostname()
mysmtpserver = 'mymailer.mydomain.com'

# --------------------------------------------------------------
def construct_email_message(sender, to_list, cc_list, subject, attachment_list):
    outer = MIMEMultipart()
    outer['From'] = sender
    outer['To'] = ', '.join(to_list)
    outer['Cc'] = ', '.join(cc_list)
    outer['Subject'] = subject
    outer.preample = 'You will not see this in a MIME-aware mail reader.\n'
    outer.epilogue = ''

    # plain text body
    msg = MIMEText('Please see attached files.\n\n')
    msg.add_header('Content-Disposition', 'inline')
    outer.attach(msg)

    # file attachments
    # outer.add_header('Content-Transfer-Encoding', 'base64')
    for att in attachment_list:
        if not os.path.isfile(att):
            continue
        ctype, encoding = mimetypes.guess_type(att)
        maintype, subtype = ctype.split('/',1)
        fp = open(att, 'rb')
        msg = MIMEBase(maintype, subtype)
        # msg = MIMEBase('application', 'octet-stream')
        msg.set_payload(fp.read())
        Encoders.encode_base64(msg)
        basename = att.split('/')[-1]
        msg.add_header('Content-Disposition', 'attachment', filename=basename)
        outer.attach(msg)

    return outer

# --------------------------------------------------------------
def send_email_message(sender, recip_list, outer, smtp_server):
    s = smtplib.SMTP()
    s.connect(smtp_server)
    s.sendmail(sender, recip_list, outer.as_string())
    s.close()

# ##############################################################
# main execution
# ##############################################################
print 'sending email'
sender          = 'a@b.com'
to_list         = [sender] # list of recepients
cc_list         = []
subject         = 'test email to send attachment(s)'
attach_list     = ['files/simple.xlsx', 'files/fish.jpg'] # list of attachments

outer = construct_email_message(sender, to_list, cc_list, subject, attach_list)

send_email_message(sender, to_list + cc_list, outer, mysmtpserver)

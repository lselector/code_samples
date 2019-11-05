#! /bin/env python2.7

""" 
# Note - needs to by converted to python3
# emailme  file1  file2
# emailme -t 'some text'  file1  file2
# sends one or more attachments as a zip file
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 
import sys
import argparse
import zipfile                    # for creating zip files 
import zlib                       # for compressing contents of zip files
import re
import textwrap
import subprocess

import smtplib
import mimetypes
mimetypes.add_type('text/csv','.csv')
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import socket
myhost=socket.gethostname()
my_smtp_server = 'mymailer.mydomain.com'

import mybag
reload(mybag)
from mybag import *

import myutil
reload(myutil)
from myutil import *

# --------------------------------------------------------------
def construct_email_message(sender, to_list, cc_list, subject, mtext, attachment_list):
    """
    #
    """
    outer = MIMEMultipart()
    outer['From'] = sender
    outer['To'] = ', '.join(to_list)
    outer['Cc'] = ', '.join(cc_list)
    outer['Subject'] = subject
    outer.preample = 'You will not see this in a MIME-aware mail reader.\n'
    outer.epilogue = ''

    # plain text body
    msg = MIMEText(mtext+'\n\n')
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
# main execution
# --------------------------------------------------------------
if run_from_ipython():
    # print "RUNNING FROM IPYTHON - importing Tracer as debug_here()"
    from IPython.core.debugger import Tracer
    debug_here = Tracer()

parser = argparse.ArgumentParser(description='simple file(s) sender.')                     
parser.add_argument('-s', '-t', action="store", dest="subj",  help='store text for subject')
parser.add_argument('mfiles', nargs='*')

results = parser.parse_args()
if not results.mfiles:
    results.mfiles = []
mtext = ''
msubj = ''
mfiles=[]

myzip = 'mailme.zip'
if os.path.exists('tmp'):
    myzip = 'tmp/' + myzip

if results.subj: 
    msubj = results.subj
    mtext = msubj

if len(results.mfiles) : 
    mfiles = results.mfiles
    mtext = "sending " + mtext + " : "
    files_text_list = textwrap.wrap(', '.join(mfiles), 70)
    if len(files_text_list) > 1:
        mtext += "\n  " + '\n  '.join(files_text_list)
    else:
        mtext += files_text_list[0]
    mtext += "\n"
    zip_files(mfiles,myzip)
    
    msubj = mtext.replace('\n',' ')
    if len(msubj) > 75:
        msubj = msubj[:75] + ' ...'

# get email addresses from real user running this script
sender, to_list, cc_list = from_to_cc_realuser()

print
print "to  :  " + ','.join(to_list + cc_list)
print "subj:  " + msubj
print "text:  " + mtext

attach_list = []
if len(results.mfiles) :
    attach_list = [myzip] # list of attachments

outer = construct_email_message(sender, to_list, cc_list, msubj, mtext, attach_list)
send_email_message(sender, to_list + cc_list, outer, my_smtp_server)

if os.path.exists(myzip):
    os.remove(myzip)

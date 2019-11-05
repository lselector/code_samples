#! /bin/env python2.7

""" 
# test_ftp.py
# a demo of how to send a file via ftp
"""

import os 
os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

import ipython_debug
reload(ipython_debug)
from ipython_debug import *

import ftplib

myhost = "odsaux"
myport = 21
myuser = "USER"
mypass = "PASSWD"

session = ftplib.FTP()
print "connecting to FTP server %s:%d as %s" % (myhost, myport, myuser)
session.connect(host=myhost, port=myport, timeout=30)
print session.getwelcome()
try:
    print "Logging in..."
    session.login(myuser, mypass)
except:
    "failed to login"
    raise

src_dir  = "files"
src_file = "fish.jpg"
dst_dir  = "some_path/junk" 
dst_file = src_file
dst_tmp  = "tmp_" + dst_file

print "changing remote dir"
print "login dir   =", session.pwd()
session.cwd(dst_dir)
print "changed dir =", session.pwd()

src_file_full = src_dir + "/" + src_file
dst_tmp_full  = dst_dir + "/" + dst_tmp
print "sending file %s to %s" % (src_file_full, dst_tmp) 
fh = open(src_file_full, 'rb')             # file to send
session.storbinary("STOR " + dst_tmp, fh)  # send the file
fh.close()                                 # close file and FTP

print "renaming remote file from %s to %s" % (dst_tmp, dst_file)
session.rename(dst_tmp, dst_file)

print "double-checking that the file is there"
mylist = session.nlst()
if dst_file not in mylist:
    print "ERROR, file is not there"
    raise

session.quit()

# session methods and properties:
#    abort     file         maxline       rename         size
#    acct      getline      mkd           retrbinary     sock
#    af        getmultiline nlst          retrlines      storbinary
#    close     getresp      ntransfercmd  rmd            storlines
#    connect   getwelcome   passiveserver sanitize       timeout
#    cwd       host         port          sendcmd        transfercmd
#    debug     lastresp     putcmd        sendeprt       voidcmd
#    debugging login        putline       sendport       voidresp
#    delete    makepasv     pwd           set_debuglevel welcome
#    dir       makeport     quit          set_pasv       

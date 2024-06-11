
"""
# Send an HTML email with an embedded image for email clients supporting html
# and a plain text message for email clients that don't want to display the HTML.
# Note - if you want to run it - please change sender email in the script before running it
"""

import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
import socket

myhost=socket.gethostname()
my_smtp_server = 'mymailer.mydomain.com'

# Define these once; use them twice!
sender   = 'a@b.com'        # CHANGE THIS BEFORE RUNNING
listTo  = [sender] # list can contain many emails
strTo  = ', '.join(listTo)

# Create the root message and fill in the from, to, and subject headers
msg = MIMEMultipart('related')
msg['Subject'] = 'test HTML message with embeded images'
msg['From']    = sender
msg['To']      = strTo
msg.preamble   = 'This is a multi-part message in MIME format.'

# -------------------------------------
# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

# first add plain text
msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# then add html text (images referenced by id strings, for example: id_image_cat)
msgText = MIMEText("""
Example of sending html message with embedded images<br>
<b>Some <i><font color="#FF3333">HTML</font></i> text</b><br>
<table border="1" cellpadding="2" cellspacing="0">
    <tr><th>cat</th><th>fish</th></tr>
    <tr><td><img src="cid:id_image_cat"></td><td><img src="cid:id_image_fish"></td></tr>
</table>
<br>Nifty!""",
  'html')
msgAlternative.attach(msgText)

# -------------------------------------
# Read images from disk, associate with corresponding html id-s, and add to message
fp = open('files/cat.jpg', 'rb')
msg_image_cat = MIMEImage(fp.read())
fp.close()

fp = open('files/fish.jpg', 'rb')
msg_image_fish = MIMEImage(fp.read())
fp.close()

msg_image_cat.add_header('Content-ID', '<id_image_cat>')
msg.attach(msg_image_cat)
msg_image_fish.add_header('Content-ID', '<id_image_fish>')
msg.attach(msg_image_fish)

# -------------------------------------
# Send the email (this example assumes SMTP authentication is required)
smtp = smtplib.SMTP()
smtp.connect(my_smtp_server)
smtp.sendmail(sender, listTo, msg.as_string())
smtp.quit()

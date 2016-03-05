#!/usr/bin/python

import smtplib
import sys

HOST = "smtp.gmail.com"
SUBJECT = "alert from server"
TO = "*********@qq.com"
FROM = "***********@gmail.com"

try:
    TEXT = sys.argv[1]
except IndexError as e:
    TEXT = e

BODY = '\r\n'.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        TEXT,
))

smtp = smtplib.SMTP()
smtp.connect(HOST, "25")
smtp.starttls()
smtp.login(FROM, "yourpassword")
smtp.sendmail(FROM, [TO], BODY)
smtp.quit()

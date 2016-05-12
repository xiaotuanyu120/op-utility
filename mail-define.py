#!/usr/bin/python

import smtplib
import sys


def send_email(subject, content):
    HOST = "smtp.gmail.com"
    TO = "igameyunwei2@gmail.com"
    FROM = "igameyunwei@gmail.com"

    SUBJECT = subject
    TEXT = content

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
    try:
        smtp.login(FROM, "bendan.521")
    except smtplib.SMTPAuthenticationError as login_error:
        print login_error
        smtp.quit()
        return login_error

    try:
        smtp.sendmail(FROM, [TO], BODY)
    except:
        e = sys.exc_info()[0]
        print "error" + e
    finally:
        smtp.quit()
    return

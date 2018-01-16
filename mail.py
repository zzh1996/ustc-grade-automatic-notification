#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import *


def send_email(subject, html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = smtp_to
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    if smtp_ssl:
        s = smtplib.SMTP_SSL(smtp_server)
    else:
        s = smtplib.SMTP(smtp_server)
    s.login(smtp_username, smtp_password)
    s.sendmail(smtp_username, smtp_to, msg.as_string())
    s.quit()

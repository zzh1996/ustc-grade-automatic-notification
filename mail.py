import smtplib
from email.mime.text import MIMEText
from config import *


def send_email(subject, text):
    msg = MIMEText(text)
    msg.add_header('Subject', subject)
    msg.add_header('From', smtp_username)
    msg.add_header('To', smtp_to)
    if smtp_ssl:
        s = smtplib.SMTP_SSL(smtp_server)
    else:
        s = smtplib.SMTP(smtp_server)
    s.login(smtp_username, smtp_password)
    s.sendmail(smtp_username, smtp_to, msg.as_string())
    s.quit()

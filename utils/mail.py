import smtplib
from email.mime.text import MIMEText
from email.header import Header

import logging
import config


def send_mail(email, mail_from, msg, msg_type='plain'):
    receivers = [email]
    message = MIMEText(msg, msg_type, 'utf-8')
    message['From'] = Header('【Toutiao】' + mail_from, 'utf-8')
    message['To'] = Header(email, 'utf-8')
    message['Subject'] = Header('【Toutiao】' + mail_from, 'utf-8')

    try:
        smtp_obj = smtplib.SMTP_SSL(config.Mail_host, 465)
        smtp_obj.ehlo()
    except Exception as e:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(config.Mail_host, 25)

    try:
        smtp_obj.login(config.Mail_user, config.Mail_pass)
        smtp_obj.sendmail(config.Mail_user, receivers, message.as_string())
    except Exception as e:
        logging.error(e)
    finally:
        smtp_obj.quit()
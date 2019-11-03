import os

Env_mail_host = os.environ.get('mail_host')
Env_mail_user = os.environ.get('mail_user')
Env_mail_pass = os.environ.get('mail_pass')

Mail_host = Env_mail_host if Env_mail_host is not None else 'smtp.qq.com'
Mail_user = Env_mail_user if Env_mail_user is not None else ''
Mail_pass = Env_mail_pass if Env_mail_pass is not None else ''

Toutiao_cookie_str = ""

Toutiao_cookie = {}
for c in Toutiao_cookie_str.split('; '):
    k, v = c.split('=')
    Toutiao_cookie[k] = v


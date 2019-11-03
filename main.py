import json
import logging

import config
from utils.request import get
from utils.toutiao import Toutiao
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.mail import send_mail

tt = None
try_count = 0


def get_content():
    res = get('https://api.apiopen.top/getJoke', {
        'type': 'text',
        'count': 20
    })
    html = ''
    if res is not None and res.get('code') == 200:
        content_list = res.get('result')
        for index, item in enumerate(content_list):
            html += '<b>{}</b><p>{}</p><p></p><br>'.format(
                index + 1,
                json.dumps(item.get('text').replace('\n', '<br>')).replace('"', '')
            )
        return html
    else:
        return None


def task():
    global tt, try_count
    if tt is not None:
        try:
            html = get_content()
            tt.write_article(html)
            try_count = 0
            print('发送成功')
        except Exception as e:
            try_count += 1
            if try_count < 5:
                task()
            else:
                logging.error(e)
                try_count = 0
                send_mail(config.Mail_user, '发送文章失败', '发送文章失败')
    else:
        # 浏览器实例不存在
        send_mail(config.Mail_user, '浏览器实例不存在', '浏览器实例不存在，需要重启服务')


if __name__ == "__main__":
    tt = Toutiao('https://mp.toutiao.com')
    tt.set_cookie()
    task()

    scheduler = BlockingScheduler()
    scheduler.add_job(task, 'cron', hour='8', minute='30')

    try:
        scheduler.start()
    except Exception as e:
        print('*' * 100)
        print('toutiao was stop')
        print('*' * 100)
        send_mail(config.Mail_user, '服务已停止', '服务已停止')

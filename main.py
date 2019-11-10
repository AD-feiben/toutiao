import json
import logging

import config
from utils.request import get
from utils.toutiao import Toutiao
# from apscheduler.schedulers.blocking import BlockingScheduler
from utils.mail import send_mail

tt = None
try_count = 0


def str_unicode_html(content):
    return json.dumps(content.replace('\n', '<br>')).replace('"', '')


def get_content():
    res = get('https://api.apiopen.top/getJoke', {
        'type': 'gif',
        'count': 20
    })
    html = ''
    if res is not None and res.get('code') == 200:
        content_list = res.get('result')
        for index, item in enumerate(content_list):
            # html += '<b>{}</b><p>{}</p>'.format(
            #     index + 1,
            #     str_unicode_html(item.get('text'))
            # )
            src = item.get('images')
            if get(src, format=False).status_code != 200:
                continue
            print(index)
            html += '<p><strong>{}</strong></p>'.format(str_unicode_html(item.get('text')))
            if item.get('top_comments_content') is not None:
                html += '<p>神评论：{}</p>'.format(str_unicode_html(item.get('top_comments_content')))
            html += '<p><img src={}></p><p> </p><p> </p><br><br>'.format(src)

        return html
    else:
        return None


def task():
    global tt, try_count
    if tt is not None:
        try:
            html = get_content()
            tt.write_article(html)
            # tt.close()
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

    # scheduler = BlockingScheduler()
    # scheduler.add_job(task, 'cron', hour='*/1')
    #
    # try:
    #     scheduler.start()
    # except Exception as e:
    #     print('*' * 100)
    #     print('toutiao was stop')
    #     print('*' * 100)
    #     send_mail(config.Mail_user, '服务已停止', '服务已停止')

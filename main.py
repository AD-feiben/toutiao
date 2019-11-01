from utils.request import get
from utils.toutiao import Toutiao


def get_content():
    res = get('https://api.apiopen.top/getJoke', {
        'type': 'text',
        'page': 1,
        'count': 20
    })
    html = ''
    if res is not None and res.get('code') == 200:
        content_list = res.get('result')

        title = content_list[0].get('text')[:30]

        for i in content_list:
            html += '<p>{}</p><br><br>\n\n'.format(i.get('text').replace('\n', '<br>'))

        return title, html
    else:
        return None


if __name__ == "__main__":
    # res = get_content()
    # print(res)
    tt = Toutiao('https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/')
    tt.click_by_xpath('//*[@id="login-type-account"]')
    tt.login('1323123123', '123456')
    # tt.close()

import time
from urllib import request

import config
from utils.browser import Browser
import cv2 as cv
from selenium.common.exceptions import StaleElementReferenceException
from utils.mail import send_mail


def find_pic(bg_path, slide_path):
    img_bg = cv.imread(bg_path)
    img_bg_gray = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)

    img_slider_gray = cv.imread(slide_path, 0)

    res = cv.matchTemplate(img_bg_gray, img_slider_gray, cv.TM_CCOEFF_NORMED)
    value = cv.minMaxLoc(res)

    return value[2:][0][0], value[2:][1][0]


# 返回两个数组：一个用于加速拖动滑块，一个用于减速拖动滑块
def generate_tracks(distance):
    # 给距离加上20，这20像素用在滑块滑过缺口后，减速折返回到缺口
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5  # 减速阀值
    while current < distance:
        if current < mid:
            a = 2  # 加速度为+2
        else:
            a = -3  # 加速度-3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1]
    return forward_tracks, back_tracks


class Toutiao(Browser):
    def login(self, account, pwd):
        self.send_keys_by_xpath('//*[@id="user-name"]', account)
        self.send_keys_by_xpath('//*[@id="password"]', pwd)
        self.click_by_xpath('//*[@id="bytedance-login-submit"]')
        self.slide_validator()

    def slide_validator(self):
        time.sleep(5)

        bg_image_name = './img_bg.png'
        slider_image_name = './img_slider.png'

        # 获取滑块背景图
        bg_image = self.wait_located('//div[@class="validate-main"]/img[1]')
        bg_image_url = bg_image.get_attribute('src')

        # 下载背景图
        request.urlretrieve(bg_image_url, bg_image_name)

        # 获取滑块图标
        slider = self.wait_located('//div[@class="validate-main"]/img[2]')
        slider_url = slider.get_attribute('src')

        request.urlretrieve(slider_url, slider_image_name)

        v1, v2 = find_pic(bg_image_name, slider_image_name)

        # 获取滑动按钮
        button = self.wait_located('//div[@class="validate-drag-button"]/img')
        try:
            self.action.click_and_hold(button).perform()
        except StaleElementReferenceException as e:
            print(e)

        self.action.reset_actions()
        forward_tracks, back_tracks = generate_tracks(v2)

        for x in forward_tracks:
            self.action.move_by_offset(x, 0)  # 前进移动滑块

        print('#' * 50)

        for x in back_tracks:
            self.action.move_by_offset(x, 0)  # 后退移动滑块

        self.action.release().perform()

    def set_cookie(self):
        for k in config.Toutiao_cookie:
            self.driver.add_cookie({
                'domain': '.toutiao.com',  # 此处xxx.com前，需要带点
                'name': k,
                'value': config.Toutiao_cookie[k],
                'path': '/',
                'expires': None
            })

    def write_article(self, content):
        self.driver.get('https://mp.toutiao.com/profile_v3/graphic/publish')
        time.sleep(3)
        if 'https://mp.toutiao.com/auth/page/login/' in self.driver.current_url:
            send_mail(config.Mail_user, '需要重新登录', '需要更新 cookie')
        else:
            self.send_keys_by_xpath('//*[@id="graphic"]/div/div[2]/div/div[1]/div[3]/div/div/div/textarea', '每日一笑！')
            self.wait_visible('//*[@id="graphic"]/div/div[2]/div/div[1]/div[4]/div/div')
            js = 'document.querySelector(".ProseMirror").innerHTML="{}"'.format(content)
            self.driver.execute_script(js)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            # 选择无图
            self.click_by_xpath('//*[@id="graphic"]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/label[3]/div')
            time.sleep(10)
            # 发表
            self.click_by_xpath('//*[@id="publish"]')




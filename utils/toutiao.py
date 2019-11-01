from utils.browser import Browser


class Toutiao(Browser):
    def login(self, account, pwd):
        self.send_keys_by_xpath('//*[@id="user-name"]', account)
        self.send_keys_by_xpath('//*[@id="password"]', pwd)
        self.click_by_xpath('//*[@id="bytedance-login-submit"]')
        # offset = get_gap_offset(self.drive)
        # drag_and_drop(browser, offset)

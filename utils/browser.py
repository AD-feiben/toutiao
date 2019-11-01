from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class Browser(object):
    def __init__(self, url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)

    def wait_visible(self, xpath):
        Wait(self.driver, 60).until(
            expected_conditions.visibility_of_element_located((By.XPATH, xpath))
        )

    def wait_clickable(self, xpath):
        Wait(self.driver, 60).until(
            expected_conditions.element_to_be_clickable((By.XPATH, xpath))
        )

    def send_keys_by_xpath(self, xpath, keys):
        self.wait_visible(xpath)
        self.driver.find_element_by_xpath(xpath).send_keys(keys)

    def click_by_xpath(self, xpath):
        self.wait_visible(xpath)
        self.driver.find_element_by_xpath(xpath).click()

    def close(self):
        self.driver.close()

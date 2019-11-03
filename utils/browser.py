import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


class Browser(object):
    def __init__(self, url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)
        self.wait = Wait(self.driver, 10)
        self.action = ActionChains(self.driver)

    def wait_visible(self, xpath):
        return self.wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, xpath))
        )

    def wait_clickable(self, xpath):
        return self.wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, xpath))
        )

    def wait_located(self, xpath):
        return self.wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )

    def send_keys_by_xpath(self, xpath, keys):
        try:
            self.click_by_xpath(xpath)
            self.driver.find_element_by_xpath(xpath).clear()
            self.driver.find_element_by_xpath(xpath).send_keys(keys)
        except Exception as e:
            logging.error(e)

    def click_by_xpath(self, xpath):
        try:
            self.wait_visible(xpath)
            self.driver.find_element_by_xpath(xpath).click()
        except Exception as e:
            logging.error(e)

    def close(self):
        self.driver.close()

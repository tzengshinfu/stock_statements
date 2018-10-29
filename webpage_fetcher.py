from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebpageFetcher():
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--ignore-ssl-errors')
        option.add_argument('--allow-running-insecure-content')
        option.add_argument('--no-sandbox')
        prefs = {'profile.managed_default_content_settings.images': 2}
        option.add_experimental_option('prefs', prefs)

        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['acceptSslCerts'] = True
        caps['acceptInsecureCerts'] = True

        self.browser = webdriver.Chrome(
            executable_path='chromedriver.exe', chrome_options=option, desired_capabilities=caps)
        self.wait = WebDriverWait(self.browser, 30)

    def go_to(self, url):
        self.browser.get(url)

    def exit(self):
        self.browser.quit()

    def close(self):
        self.browser.close()

    def switch_to_default_content(self):
        self.browser.switch_to.default_content()

    def execute_script(self, script_name):
        self.browser.execute_script(script_name)

    def switch_to_window(self, window):
        self.browser.switch_to.window(window)

    def find_element(self, element_xpath):
        item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, element_xpath)))
        return item

    def switch_to_frame(self, element_xpath):
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                       element_xpath)))
        return self

    def store_window_position(self):
        """儲存父子視窗定位以跳轉操作"""
        while True:
            if len(self.browser.window_handles) == 2:
                self.main_window = self.browser.window_handles[0]
                self.sub_window = self.browser.window_handles[1]
                break

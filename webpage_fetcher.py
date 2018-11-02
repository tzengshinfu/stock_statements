from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import tempfile
import subprocess
import sys
import lazy_object_proxy


class WebpageFetcher():
    tempfile_path = tempfile.gettempdir()
    scripts_path = '\\'.join(sys.executable.split('\\')[0:-1]) + '\\Scripts'

    def __init__(self):
        self.browser = lazy_object_proxy.Proxy(self.initial_browser)
        self.wait = lazy_object_proxy.Proxy(self.initial_wait)
        self.main_window = None
        self.sub_window = None

    def initial_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--incognito')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-translate')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--no-sandbox')
        options.add_argument('--no-referrers')
        options.add_argument('--disk-cache-dir="' + self.tempfile_path + '"')
        options.add_argument('--download-whole-document')
        options.add_argument('--deterministic-fetch')
        options.add_argument('--log-level=3')
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.sound': 2,
            'profile.managed_default_content_settings.flash_data': 2,
            'download.default_directory': self.tempfile_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
        }
        options.add_experimental_option('prefs', prefs)
        return webdriver.Chrome(
            executable_path='chromedriver.exe', chrome_options=options)

    def initial_wait(self):
        return WebDriverWait(driver=self.browser, timeout=30)

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
            EC.presence_of_element_located((By.XPATH, element_xpath)))
        return item

    def find_elements(self, element_xpath):
        item = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, element_xpath)))
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

    def get_response(self, url, method: 'get/post/download', data=None):
        def get_browser_headers():
            """取得瀏覽器Request Header"""
            browser_headers = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
            return browser_headers

        if method == 'get':
            response = requests.get(
                url, params=data, headers=get_browser_headers(), verify=False)
        elif method == 'post':
            response = requests.post(
                url, data=data, headers=get_browser_headers(), verify=False)
        elif method == 'download':
            response = requests.get(
                url, headers=get_browser_headers(), verify=False, stream=True)
        return response

    def download_file(self, url):
        file_path = self.tempfile_path + '\\' + url.split('/')[-1]
        response = self.get_response(url, 'download')
        with open(file_path, 'wb') as stream:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    stream.write(chunk)
        return file_path

    def get_pdf_text(self, pdf_path):
        return subprocess.check_output(
            ['python', self.scripts_path + '\\' + 'pdf2txt.py', '-t', 'xml', pdf_path],
            shell=False)

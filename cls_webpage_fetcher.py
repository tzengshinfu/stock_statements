import requests
import tempfile
from lxml import etree
from retry import retry
import time
import random
from typing import List


class ClsWebpageFetcher():
    def __init__(self):
        self.tempdir_path = tempfile.gettempdir()
        self.response = None
        self.tree = None

    @retry((ConnectionError, ConnectionRefusedError), tries=3, delay=10)
    def go_to(self, url: str, method: str = 'get', data: str = None):
        """取得瀏覽器回應

            Arguments:
                url {str} -- 網址
                method {str} -- get/post/download

            Keyword Arguments:
                data {str} -- 附加資料 (default: {None})
        """

        def get_browser_headers() -> dict:
            """取得瀏覽器Request Header"""
            browser_headers = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
            return browser_headers

        session = requests.session()
        session.keep_alive = False

        if method == 'get':
            response = session.get(url, params=data, headers=get_browser_headers(), verify=False)
            response.encoding = response.apparent_encoding
            self.response = response
            self.tree = etree.HTML(self.response.text)
        elif method == 'post':
            response = session.post(url, data=data, headers=get_browser_headers(), verify=False)
            response.encoding = response.apparent_encoding
            self.response = response
            self.tree = etree.HTML(self.response.text)
        elif method == 'download':
            response = requests.get(url, headers=get_browser_headers(), verify=False, stream=True)
            self.response = response
        else:
            raise ValueError('method值只能是(get/post/download)其中之一')

    def download_file(self, url: str) -> str:
        """下載檔案

            Arguments:
                url {str} -- 檔案所在URL

            Returns:
                str -- 下載後的本機路徑
        """
        file_path = self.tempdir_path + '\\' + url.split('/')[-1]
        self.go_to(url, 'download')
        with open(file_path, 'wb') as stream:
            for chunk in self.response.iter_content(chunk_size=1024):
                if chunk:
                    stream.write(chunk)
        return file_path

    def find_element(self, element_xpath: str) -> List[etree._Element]:
        """尋找符合條件的第1個網頁元素

            Arguments:
                element_xpath {str} -- XPATH條件

            Returns:
                List[etree._Element] -- 網頁元素
        """
        elements = self.find_elements(element_xpath)
        return next(iter(elements or []), None)

    def find_elements(self, elements_xpath: str) -> List[etree._Element]:
        """尋找符合條件的網頁元素集合

            Arguments:
                element_xpath {str} -- XPATH條件

            Returns:
                List[etree._Element] -- 網頁元素
        """
        elements = self.tree.xpath(elements_xpath)
        return elements

    def wait(self, at_least_seconds: int, at_most_seconds: int):
        """暫停隨機秒數

            Arguments:
                at_least_seconds {int} -- 至少暫停秒數
                at_most_seconds {int} -- 最多暫停秒數
        """
        time.sleep(random.randint(at_least_seconds, at_most_seconds))

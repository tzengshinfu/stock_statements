import requests
from lxml import etree
from retry import retry
import time
import random
from typing import List


class ClsWebpageFetcher():
    def __init__(self):
        pass

    @retry((ConnectionError, ConnectionRefusedError), tries=3, delay=600, back_off=2)
    def _get_response(self, url: str, method: str, data: str) -> requests.Response:
        """
        取得瀏覽器回應

        Arguments:
        url -- 網址
        method -- get/post/download

        Keyword Arguments:
        data -- 附加資料

        Returns:
        瀏覽器回應
        """

        def get_browser_headers() -> dict:
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
            return response
        elif method == 'post':
            response = session.post(url, data=data, headers=get_browser_headers(), verify=False)
            response.encoding = response.apparent_encoding
            return response
        elif method == 'download':
            response = requests.get(url, headers=get_browser_headers(), verify=False, stream=True)
            return response
        else:
            raise ValueError('method值只能是(get/post/download)其中之一')

    def download_file(self, url: str, path: str) -> str:
        """
        下載檔案

        Arguments:
        url -- 檔案所在URL

        Returns:
        下載後的本機路徑
        """
        response = self._get_response(url, 'download')

        file_path = path + '\\' + url.split('/')[-1]
        with open(file_path, 'wb') as stream:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    stream.write(chunk)

        return file_path

    def find_element(self, html: etree.HTML, element_xpath: str) -> List[etree._Element]:
        """
        尋找符合條件的第1個網頁元素

        Arguments:
        html -- etree.HTML物件
        element_xpath -- XPATH條件

        Returns:
        網頁元素
        """
        elements = self.find_elements(html, element_xpath)
        return next(iter(elements or []), None)

    def find_elements(self, html: etree.HTML, elements_xpath: str) -> List[etree._Element]:
        """
        尋找符合條件的網頁元素集合

        Arguments:
        html -- etree.HTML物件
        element_xpath -- XPATH條件

        Returns:
        網頁元素集合
        """
        elements = html.xpath(elements_xpath)
        return elements

    def wait(self, least_seconds: int, most_seconds: int):
        """
        暫停隨機秒數

        Arguments:
        least_seconds -- 至少暫停秒數
        most_seconds -- 最多暫停秒數
        """
        time.sleep(random.randint(least_seconds, most_seconds))

    def download_html(self, url: str, method: str = 'get', data: str = None) -> etree.HTML:
        """
        下載網頁Html

        Arguments:
        url -- 網址
        method -- get/post (default: 'get')

        Keyword Arguments:
        data -- 附加資料 (default: None)

        Returns:
        網頁Html
        """
        response = self._get_response(url, method, data)
        return etree.HTML(response.text)

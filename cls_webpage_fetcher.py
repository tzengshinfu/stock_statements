import requests
import tempfile
import lazy_object_proxy
from lxml import etree
from retry import retry


class ClsWebpageFetcher():
    def __init__(self):
        self.request = lazy_object_proxy.Proxy(self.__Request)
        self.tempdir_path = tempfile.gettempdir()

    class __Request():
        def __init__(self):
            self.response = None
            self.tree = None

        @retry((ConnectionError, ConnectionRefusedError), tries=3, delay=10)
        def go_to(self, url, method='get', data=None):
            """取得瀏覽器回應

                Arguments:
                    url {str} -- 網址
                    method {str} -- get/post/download

                Keyword Arguments:
                    data {str} -- 附加資料 (default: {None})
            """

            def get_browser_headers():
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
                response = requests.get(
                    url, headers=get_browser_headers(), verify=False, stream=True)
                self.response = response

        def download_file(self, url):
            file_path = self.tempdir_path + '\\' + url.split('/')[-1]
            self.go_to(url, 'download')
            with open(file_path, 'wb') as stream:
                for chunk in self.response.iter_content(chunk_size=1024):
                    if chunk:
                        stream.write(chunk)
            return file_path

        def find_element(self, element_xpath):
            element = self.tree.xpath(element_xpath)
            return element

        def find_elements(self, elements_xpath):
            return self.find_element(elements_xpath)

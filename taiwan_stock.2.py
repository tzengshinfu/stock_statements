import requests
from lxml import etree
from bs4 import BeautifulSoup
import public_function
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)


class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

class TaiwanStock():
    function = public_function.PublicFunction()

    def get_stock_list(self):
        """取得台股上巿股票列表頁面"""
        stock_list = []
        response = self.get_response(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch')
        if response is not ConnectionError:
            tree = etree.HTML(response.text)
            code_list = tree.xpath('//table[@class="grid"]//a/text()')
            for code in code_list:
                stock_list.append([code[0:4], code[4:]])
            return stock_list

    def get_detail_data(self):
        response = self.post_response(
            'https://www.cnyes.com/twstock/financial4.aspx')
        if response is not ConnectionError:
            tree = etree.HTML(response[1].text)
            detail_list = tree.xpath(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr/td[1]/string(.)'
            )
            return detail_list

    def get_response(self, url):
        try:
            response = requests.get(
                url, headers=self.function.get_browser_headers(url))
            return response
        except Exception as ex:
            return ex

    def post_response(self, url):
        try:
            session = requests.Session()
            session.headers.update(self.function.get_browser_headers(url))
            
            session.mount(url, HTTPAdapter)
            response = session.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            form_data = {
                '__VIEWSTATE':
                soup.find('input', attrs={'name': '__VIEWSTATE'})['value'],
                "__EVENTTARGET":
                "",
                "__EVENTARGUMENT":
                "",
                'ctl00$ContentPlaceHolder1$D1':
                'T',
                'ctl00$ContentPlaceHolder1$D2':
                'ALL',
                'ctl00$ContentPlaceHolder1$D3':
                '2018Q2'
            }
            response = session.post(url=url, data=form_data)
            return response
        except Exception as ex:
            return ex

import requests
from lxml import etree
import public_function
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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
        response = self.get_response(
            'https://www.cnyes.com/twstock/financial4.aspx')
        __VIEWSTATE=response.search('id="__VIEWSTATE" value="(.*?)"',response.content).group(1)

        if response is not ConnectionError:
            tree = etree.HTML(response[1].text)
            detail_list = tree.xpath(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr/td[1]/string(.)'
            )
            return detail_list

    def get_response(self, url):
        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount(url, adapter)

            response = session.get(url)

            return response
        except Exception as ex:
            return ex

    def post_response(self, url):
        try:
            form_data = {
                '__VIEWSTATE':
                '',
                '__EVENTTARGET':
                '',
                '__EVENTARGUMENT':
                '',
                'ctl00$ContentPlaceHolder1$D1':
                'T',
                'ctl00$ContentPlaceHolder1$D2':
                'ALL',
                'ctl00$ContentPlaceHolder1$D3':
                '2018Q2'
            }
            response = requests.get(url=url)
            return response
        except Exception as ex:
            return ex

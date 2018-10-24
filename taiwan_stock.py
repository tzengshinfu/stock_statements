import requests
from lxml import etree
import public_function
from time import sleep


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

        if response is not ConnectionError:
            tree = etree.HTML(response[1].text)
            detail_list = tree.xpath(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr/td[1]/string(.)'
            )
            return detail_list

    def get_response(self, url):
        while 1:
            try:
                s = requests.session()
                s.keep_alive = False
                response = s.get(url, headers=self.function.get_browser_headers(url), verify=False)

                return response
            except Exception as ex:
                sleep(5)
                continue

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

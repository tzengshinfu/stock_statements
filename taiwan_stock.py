import requests
from lxml import etree
import public_function


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
        # response = requests.get(
        #     'https://www.cnyes.com/twstock/financial4.aspx',
        #     headers=self.function.get_browser_headers(
        #         'https://www.cnyes.com/twstock/financial4.aspx'),
        #     verify=False)

        response = requests.get(
            'https://www.cnyes.com',
            headers=self.function.get_browser_headers(
                'https://www.cnyes.com'),
            verify=False)

        if response is not ConnectionError:
            tree = etree.HTML(response[1].text)
            detail_list = tree.xpath(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr/td[1]/string(.)'
            )
            return detail_list

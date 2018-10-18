import requests
from lxml import etree

import public_function


class TaiwanStock():
    function = public_function.PublicFunction()

    def get_stock_list(self):
        """取得台股上巿股票列表頁面"""
        stock_list = []
        response = requests.get(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch',
            headers=self.function.get_browser_headers(
                'http://www.twse.com.tw/zh/stockSearch/stockSearch'))
        tre = etree.HTML(response.text)
        code_list = tre.xpath('//table[@class="grid"]//a/text()')
        for code in code_list:
            stock_list.append([code[0:4], code[4:]])
        return stock_list

    def get detail_data(self):
        # https://www.cnyes.com/twstock/financial4.aspx
        # //table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr/td[1]/string(.)
        return ''
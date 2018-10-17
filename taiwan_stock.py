import requests
import json
from lxml import etree
import public_function


class TaiwanStock():
    function = public_function.PublicFunction()

    def get_stock_list(self):
        """取得台股上巿股票列表頁面"""
        response = requests.get(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch',
            headers=self.function.get_browser_headers(
                'http://www.twse.com.tw/zh/stockSearch/stockSearch'))
        html = etree.HTML(response.text)
        code_list = html.xpath('//table[@class="grid"]//a/substring(text(), 1, 4)')
        return code_list
        
import requests
import json
import public_function


class TaiwanStock():
    function = public_function.PublicFunction()

    def get_stock_list(self):
        """取得台股上巿股票列表頁面"""
        response = requests.get(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch',
            headers=self.function.get_browser_headers(
                'http://www.twse.com.tw/zh/stockSearch/stockSearch'))
        text = response.text.replace('callback', '')
        text = text[1:]
        text = text[:len(text) - 1]
        objects = json.loads(text)

        return objects    
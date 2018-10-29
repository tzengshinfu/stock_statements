import requests
from lxml import etree
import webpage_fetcher


class TaiwanStock():
    function = public_function.WebPageFetcher()

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
        try:
            response = requests.get(
                'https://www.cnyes.com/twstock/financial4.aspx/',
                headers=self.function.get_browser_headers('https://www.cnyes.com/twstock/financial4.aspx/'),
                verify=False)
            print(response)
        except OSError as e:
            print(e)
        # while True:
        #     try:
        #         session = requests.Session()
        #         session.mount('www.google.com', DESAdapter())
        #         response = session.get(
        #             'https://www.google.com/',
        #             headers=self.function.get_browser_headers(
        #                 'https://www.google.com/'))
        #         print(response.json())
        #     except OSError as e:
        #         print(e)
        #         time.sleep(10)

        # response = requests.get(
        #    'https://www.cnyes.com/twstock/financial4.aspx',
        #    headers=self.function.get_browser_headers('https://www.cnyes.com/twstock/financial4.aspx'),
        #    verify=False)

        # response = requests.get(
        #    'https://www.reporo.com/',
        #    headers=self.function.get_browser_headers(
        #        'https://www.reporo.com/'))

        # if response is not ConnectionError:
        #    tree = etree.HTML(response[1].text)
        #    detail_list = tree.xpath(
        #        '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr/td[1]/string(.)'
        #    )
        #    return detail_list

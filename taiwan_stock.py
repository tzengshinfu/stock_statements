import webpage_fetcher
import time
from lxml import etree


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_stock_data(self):
        stock_basic = self.get_stock_basic('1110')
        print(stock_basic)
        # stock_codes = self.get_stock_codes()
        # stock_eps = self.get_stock_eps()
        # print(stock_codes)
        # print(stock_eps)
        self.fetcher.exit()

    def get_stock_codes(self):
        """取得台股上巿股票列表"""
        stock_codes = []
        response = self.fetcher.get_response(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch', 'GET')
        tree = etree.HTML(response.text)
        codes = tree.xpath('//table[@class="grid"]//a/text()')
        for code in codes:
            stock_codes.append([code[0:4], code[4:]])
        return stock_codes

    def get_stock_basic(self, stock_id):
        """取得台股上巿股票基本資料"""
        stock_basic = []
        response = self.fetcher.get_response(
            'http://mops.twse.com.tw/mops/web/t05st03', 'POST', data='firstin=1&co_id=' + stock_id)
        tree = etree.HTML(response.text)
        establishment_date = tree.xpath('//table[@class="hasBorder"]//tr[position()=8]/td[@class="lColor" and position()=1]')
        capital_amount = tree.xpath('//table[@class="hasBorder"]//tr[position()=9]/td[@class="lColor" and position()=1]')
        industry = tree.xpath('//table[@class="hasBorder"]//tr[position()=1]/td[@class="lColor" and position()=2]')
        stock_basic.append(stock_id)
        stock_basic.append(industry[0].text.strip())
        stock_basic.append(establishment_date[0].text.strip())
        stock_basic.append(capital_amount[0].text.strip().replace('元', '').replace(',', ''))
        # stock_links = self.fetcher.find_elements('//table[@class="grid"]//a')
        return stock_basic

    def get_stock_eps(self):
        def get_years():
            """取得EPS年度"""
            result = []
            year_tags = self.fetcher.find_elements(
                '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option')
            for tag in year_tags:
                result.append(tag.text)
            return result

        def get_records(year):
            """取得EPS資料"""
            result = []
            eps_records = self.fetcher.find_elements(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr[not(@align)]'
            )
            for record in eps_records:
                eps = []
                eps.append(year)
                eps_fields = record.find_elements_by_tag_name('td')
                for field in eps_fields:
                    eps.append(field.text)
                result.append(eps)
            return result

        def get_current_table_content():
            """取得EPS表格內容"""
            return self.fetcher.find_element(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]').text

        stock_eps = []
        self.fetcher.go_to('https://www.cnyes.com/twstock/financial4.aspx')
        eps_years = get_years(self)
        previous_eps_table_content = ''
        for year in eps_years:
            self.fetcher.find_element(
                '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option[text()="'
                + year + '"]').click()
            # 因為當年度的EPS表格是以AJAX載入,所以要反覆取得跟前次表格內容比對以判斷載入是否完成
            current_eps_table_content = get_current_table_content()
            while current_eps_table_content == previous_eps_table_content:  # 重新執行直到取得當年度的資料
                time.sleep(0.2)
                current_eps_table_content = get_current_table_content()
            stock_eps.append(get_records(year))
            previous_eps_table_content = get_current_table_content()
        return stock_eps

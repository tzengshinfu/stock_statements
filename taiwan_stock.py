import webpage_fetcher
import time


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_stock_details(self):
        stock_codes = self.get_stock_codes()
        stock_eps = self.get_stock_eps()
        print(stock_codes)
        print(stock_eps)
        self.fetcher.exit()

    def get_stock_codes(self):
        """取得台股上巿股票列表"""
        self.fetcher.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
        result = []
        stock_links = self.fetcher.find_elements('//table[@class="grid"]//a')
        for link in stock_links:
            code = link.text
            result.append([code[0:4], code[4:]])
        return result

    def get_stock_eps(self):
        def get_eps_years(self):
            """取得EPS年度"""
            result = []
            year_tags = self.fetcher.find_elements('//select[@id="ctl00_ContentPlaceHolder1_D3"]/option')
            for tag in year_tags:
                result.append(tag.text)
            return result

        def get_eps_data(self, year):
            """取得EPS資料"""
            result = []
            eps_records = self.fetcher.find_elements('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr[not(@align)]')
            for record in eps_records:
                eps = []
                eps.append(year)
                eps_fields = record.find_elements_by_tag_name('td')
                for field in eps_fields:
                    eps.append(field.text)
                result.append(eps)
            return result

        def get_eps_table_content(self, year):
            """取得EPS表格內容作為判斷是否已載入完成"""
            return self.fetcher.find_element('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]').text

        self.fetcher.go_to('https://www.cnyes.com/twstock/financial4.aspx')
        eps_years = get_eps_years(self)
        previous_eps_table_content = ''
        s = []
        for year in eps_years:
            self.fetcher.find_element('//select[@id="ctl00_ContentPlaceHolder1_D3"]/option[text()="' + year + '"]').click()
            current_eps_table_content = get_eps_table_content(self, year)
            while current_eps_table_content == previous_eps_table_content:  # 重新執行直到取得當年度的資料
                time.sleep(0.2)
                current_eps_table_content = get_eps_table_content(self, year)
            s.append(get_eps_data(self, year))
            previous_eps_table_content = get_eps_table_content(self, year)
        return s

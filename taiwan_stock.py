import webpage_fetcher
import time


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get(self):
        # self.get_stock_codes()
        self.get_stock_eps()
        self.fetcher.exit()

    def get_stock_codes(self):
        """取得台股上巿股票列表"""
        self.fetcher.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
        stock_codes = []
        stock_links = self.fetcher.find_elements('//table[@class="grid"]//a')
        for link in stock_links:
            code = link.text
            stock_codes.append([code[0:4], code[4:]])
        return stock_codes

    def get_stock_eps(self):
        def get_years(self):
            years = []
            year_tags = self.fetcher.find_elements('//select[@id="ctl00_ContentPlaceHolder1_D3"]/option')
            for year in year_tags:
                years.append(year.text)
            return years

        def get_eps_data(self):
            """取得台股上巿股票EPS"""
            stock_eps = []
            eps_records = self.fetcher.find_elements('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr[not(@align)]')
            for record in eps_records:
                eps = []
                eps.append('2018Q3')
                eps_fields = record.find_elements_by_tag_name('td')
                for field in eps_fields:
                    eps.append(field.text)
                stock_eps.append(eps)
            return stock_eps

        def get_table_data(self, year):
            """取得台股上巿股票EPS"""
            return self.fetcher.find_element('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]').text

        self.fetcher.go_to('https://www.cnyes.com/twstock/financial4.aspx')
        years = get_years(self)
        pre_eps_table_text = ''
        for year in years:
            self.fetcher.find_element('//select[@id="ctl00_ContentPlaceHolder1_D3"]/option[text()="' + year + '"]').click()
            current_eps_table_text = get_table_data(self, year)
            while current_eps_table_text == pre_eps_table_text:
                time.sleep(0.2)
                current_eps_table_text = get_table_data(self, year)

            pre_eps_table_text = get_table_data(self, year)

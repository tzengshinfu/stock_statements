import webpage_fetcher
import time
from lxml import etree


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_stock_data(self):
        stock_basic = self.get_stock_basic('1110')
        print(stock_basic)
        # stock_codes = self.get_stock_codes()
        stock = self.StockSheet(
            'https://www.cnyes.com/twstock/financial4.aspx',
            '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option'
            '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]')
        stock_sheet = self.get_stock_sheet(stock)
        # print(stock_codes)
        # print(stock_eps)
        self.fetcher.exit()

    def get_stock_codes(self):
        """取得台股上巿股票列表"""
        stock_codes = []
        response = self.fetcher.get_response(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch', 'get')
        tree = etree.HTML(response.text)
        codes = tree.xpath('//table[@class="grid"]//a/text()')
        for code in codes:
            stock_codes.append([code[0:4], code[4:]])
        return stock_codes

    def get_stock_basic(self, stock_id):
        """取得台股上巿股票基本資料"""
        stock_basic = []
        response = self.fetcher.get_response(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            data='firstin=1&co_id=' + stock_id)
        tree = etree.HTML(response.text)
        establishment_date = tree.xpath(
            '//table[@class="hasBorder"]//tr[position()=8]/td[@class="lColor" and position()=1]'
        )
        capital_amount = tree.xpath(
            '//table[@class="hasBorder"]//tr[position()=9]/td[@class="lColor" and position()=1]'
        )
        industry = tree.xpath(
            '//table[@class="hasBorder"]//tr[position()=1]/td[@class="lColor" and position()=2]'
        )
        stock_basic.append(stock_id)
        stock_basic.append(industry[0].text.strip())
        stock_basic.append(establishment_date[0].text.strip())
        stock_basic.append(capital_amount[0].text.strip().replace('元',
                                                                  '').replace(
                                                                      ',', ''))
        return stock_basic

    def get_stock_eps(self):
        stock_eps = []
        self.fetcher.go_to('https://www.cnyes.com/twstock/financial4.aspx')
        eps_years = self.get_years(
            '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option')
        previous_eps_table_content = ''
        for year in eps_years:
            self.fetcher.find_element(
                '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option[text()="'
                + year + '"]').click()
            # 因為當年度的EPS表格是以AJAX載入,所以要反覆取得跟前次表格內容比對以判斷載入是否完成
            current_eps_table_content = self.get_table_content(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]')
            while current_eps_table_content == previous_eps_table_content:  # 重新執行直到取得當年度的資料
                time.sleep(0.2)
                current_eps_table_content = self.get_table_content(
                    '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]')
            stock_eps.append(
                self.get_records(
                    year,
                    '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr[not(@align)]'
                ))
            previous_eps_table_content = self.get_table_content(
                '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]')
        return stock_eps

    @dataclass
    class StockSheet:
        url: str
        years: str
        table: str

    # TODO(tzengshinfu@gmail.com): 與方法[get_stock_eps]合併。
    def get_stock_balance_sheet(self):
        stock_balance_sheet = []
        stock = self.StockSheet(
            'https://www.cnyes.com/twstock/financial4.aspx',
            '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option'
            '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]')
        stock_balance_sheet = self.get_stock_sheet(stock)

    def get_table_content(self, element_xpath):
        """取得表格內容"""
        table_content = self.fetcher.find_element(element_xpath).text
        return table_content

    def get_years(self, element_xpath):
        """取得年度"""
        years = []
        year_tags = self.fetcher.find_elements(element_xpath)
        for tag in year_tags:
            years.append(tag.text)
        return years

    def get_records(self, year, element_xpath):
        """取得資料"""
        records = []
        eps_records = self.fetcher.find_elements(element_xpath)
        for record in eps_records:
            eps = []
            eps.append(year)
            eps_fields = record.find_elements_by_tag_name('td')
            for field in eps_fields:
                eps.append(field.text)
            records.append(eps)
        return records

    def get_stock_sheet(self, stock_sheet1):
        stock_sheet = []
        self.fetcher.go_to(stock_sheet1.url)
        eps_years = self.get_years(
            stock_sheet1.years)
        previous_eps_table_content = ''
        for year in eps_years:
            self.fetcher.find_element(
                stock_sheet1.years + '[text()="'
                + year + '"]').click()
            # 因為當年度的EPS表格是以AJAX載入,所以要反覆取得跟前次表格內容比對以判斷載入是否完成
            current_eps_table_content = self.get_table_content(
                stock_sheet1.table)
            while current_eps_table_content == previous_eps_table_content:  # 重新執行直到取得當年度的資料
                time.sleep(0.2)
                current_eps_table_content = self.get_table_content(
                    stock_sheet1.table)
            stock_sheet.append(
                self.get_records(
                    year,
                    stock_sheet1.table + '//tr'
                ))
            previous_eps_table_content = self.get_table_content(
                stock_sheet1.table)
        return stock_sheet

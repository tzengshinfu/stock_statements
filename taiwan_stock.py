import webpage_fetcher
import time
from lxml import etree


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_financial_statements(self):
        # stock_codes = self.get_stock_codes()
        # stock_basic = self.get_stock_basic('1110')
        # print(stock_basic)

        balance_sheet = self.get_balance_sheet()
        print(balance_sheet)
        # print(stock_eps)
        self.fetcher.exit()

    def get_codes(self):
        """取得台股上巿股票列表"""
        codes = []
        response = self.fetcher.get_response(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch', 'get')
        tree = etree.HTML(response.text)
        codes = tree.xpath('//table[@class="grid"]//a/text()')
        for code in codes:
            codes.append([code[0:4], code[4:]])
        return codes

    # TODO https://stackoverflow.com/questions/25964194/iterate-through-all-the-rows-in-a-table-using-python-lxml-xpath/26014263#26014263
    def get_basic(self, stock_id):
        """取得台股上巿股票基本資料"""
        basic = []
        response = self.fetcher.get_response(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            data='firstin=1&co_id=' + stock_id)
        html = etree.HTML(response.text)
        rows_xpath = etree.XPath('//table[@class="hasBorder"]//tr')
        title_xpath = etree.XPath('th[1]/text()')
        value_xpath = etree.XPath('td[1]/text()')
        for row in rows_xpath(html):
            pass
            # basic.append(stock_id)
            # basic.append(industry[0].text.strip())
            # basic.append(establishment_date[0].text.strip())
            # basic.append(capital_amount[0].text.strip().replace('元',
            #                                                        '').replace(
            #                                                            ',', ''))
            # establishment_date = tree.xpath(
            #     '//table[@class="hasBorder"]//tr[position()=8]/td[@class="lColor" and position()=1]'
            # )
            # capital_amount = tree.xpath(
            #     '//table[@class="hasBorder"]//tr[position()=9]/td[@class="lColor" and position()=1]'
            # )
            # industry = tree.xpath(
            #     '//table[@class="hasBorder"]//tr[position()=1]/td[@class="lColor" and position()=2]'
            # )

        return basic

    def get_eps(self):
        url = 'https://www.cnyes.com/twstock/financial4.aspx'
        year = '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option'
        table = '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]'
        eps = self.get_table(url, year, table)
        return eps

    def get_balance_sheet(self):
        url = 'http://www.cnyes.com/twstock/bs/1101.htm'
        year = '//select[@id="ctl00_ContentPlaceHolder1_DropDownList1"]/option'
        table = '//table[@id="ctl00_ContentPlaceHolder1_htmltb1"]'
        balance_sheet = self.get_table(url, year, table)
        return balance_sheet

    def get_table(self, url, years_xpath, table_xpath):
        def get_contents(self, table_xpath):
            """取得表格內容"""
            contents = self.fetcher.find_element(table_xpath).text
            return contents

        def get_years(self, years_xpath):
            """取得年度"""
            years = []
            year_tags = self.fetcher.find_elements(years_xpath)
            for tag in year_tags:
                years.append(tag.text)
            return years

        def get_records(self, year, rows_xpath):
            """取得資料"""
            records = []
            rows = self.fetcher.find_elements(rows_xpath)
            for row in rows:
                record = []
                record.append(year)
                fields = row.find_elements_by_tag_name('td')
                for field in fields:
                    record.append(field.text)
                records.append(record)
            return records

        table = []
        self.fetcher.go_to(url)
        years = self.get_years(years_xpath)
        previous_contents = ''
        for year in years:
            self.fetcher.find_element(years_xpath + '[text()="' + year +
                                      '"]').click()
            # 因為當年度的表格是以AJAX載入,所以要反覆取得跟前次表格內容比對以判斷載入是否完成
            current_contents = get_contents(
                table_xpath)
            while current_contents == previous_contents:  # 重新執行直到取得當年度的資料
                time.sleep(0.2)
                current_contents = get_contents(
                    table_xpath)
            records = self.get_records(year, table_xpath + '//tr')
            table.append(records)
            previous_contents = get_contents(table_xpath)
        return table

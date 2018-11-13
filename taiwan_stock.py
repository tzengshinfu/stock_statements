import webpage_fetcher
import time
from lxml import etree


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_financial_statements(self):
        # do something
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

    # TODO 資料整理
    def get_basics(self, stock_id):
        """取得台股上巿股票基本資料"""
        basic = []
        response = self.fetcher.get_response(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            data='firstin=1&co_id=' + stock_id)
        html = etree.HTML(response.text)
        rows_xpath = etree.XPath('//table[@class="hasBorder"]//tr')
        head1_xpath = etree.XPath('th[1]/text()')
        body1_xpath = etree.XPath('td[1]/text()')
        head2_xpath = etree.XPath('th[2]/text()')
        body2_xpath = etree.XPath('td[2]/text()')
        for row in rows_xpath(html):
            head1 = head1_xpath(row)
            body1 = body1_xpath(row)
            basic.append(head1)
            basic.append(body1)
            head2 = head2_xpath(row)
            body2 = body2_xpath(row)
            basic.append(head2)
            basic.append(body2)
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

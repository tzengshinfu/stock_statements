import webpage_fetcher
import time
from lxml import etree


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_financial_statements(self):
        # TODO do something
        self.fetcher.exit()

    def get_codes(self):
        """取得台股上巿股票代號/名稱列表"""
        codes = []
        response = self.fetcher.get_response(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch', 'get')
        tree = etree.HTML(response.text)
        codes = tree.xpath('//table[@class="grid"]//a/text()')
        for code in codes:
            codes.append([code[0:4], code[4:]])
        return codes

    def get_basicinfo(self, stock_id):
        """取得台股上巿股票基本資料"""
        basic = []
        response = self.fetcher.get_response(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            data='firstin=1&co_id=' + stock_id)
        html = etree.HTML(response.text)
        rows_xpath = etree.XPath('//table[@class="hasBorder"]//tr')
        dic = {}
        title = ''
        for row in rows_xpath(html):
            if (row[0].text.strip() == '本公司'):
                dic[row[2].text.strip()] = row[1].text.strip()
                dic[row[5].text.strip()] = row[4].text.strip()
            if (row[0].text.strip() == '本公司採'):
                dic['會計年度月制(現)'] = row[1].text.strip()
            if (row[0].text.strip() == '本公司於'):
                dic['會計年度月制(前)'] = row[3].text.strip()
                dic['會計年度月制轉換'] = row[1].text.strip()
            if (row[0].text.strip() == '編製財務報告類型'):
                report_type = row[1].text.strip()
                dic[row[0].text.strip()] = report_type[1:3] if report_type[
                    0] == '●' else report_type[4:6]
            else:
                for index in range(len(row)):
                    field = row[index]
                    if (index % 2 == 0):
                        if (field.tag == 'th'):
                            title = field.text.strip()
                            dic[title] = ''
                    if (index % 2 == 1):
                        if (field.tag == 'td'):
                            dic[title] = field.text.strip()
        return basic

    def get_eps(self):
        url = 'https://www.cnyes.com/twstock/financial4.aspx'
        years = self.get_years('//select[@id="ctl00_ContentPlaceHolder1_D3"]/option')
        table_xpath = '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]'
        eps = self.get_table(url, years, table_xpath)
        return eps

    def get_balance_sheet(self):
        url = 'http://www.cnyes.com/twstock/bs/1101.htm'
        years = self.get_years('//select[@id="ctl00_ContentPlaceHolder1_DropDownList1"]/option')
        table_xpath = '//table[@id="ctl00_ContentPlaceHolder1_htmltb1"]'
        balance_sheet = self.get_table(url, years, table_xpath)
        return balance_sheet

    def get_years(self, years_xpath):
        """取得年度

        Arguments:
            years_xpath {str} -- 年度下拉清單的XPATH

        Returns:
            {list} -- 年度清單
        """
        years = []
        year_tags = self.fetcher.find_elements(years_xpath)
        for tag in year_tags:
            years.append(tag.text)
        return years

    def get_table(self, url, years, table_xpath):
        """取得表格內容

        Arguments:
            url {str} -- 來源網址
            years {list} -- 年度清單, 如['2018Q3', '2018Q2']
            table_xpath {str} -- 表格的XPATH
        """
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
        previous_contents = ''
        for year in years:
            self.fetcher.find_element(years + '[text()="' + year +
                                      '"]').click()
            # 因為當年度的表格是以AJAX載入,所以要反覆取得跟前次表格內容比對以判斷載入是否完成
            current_contents = self.fetcher.find_element(table_xpath).text
            while current_contents == previous_contents:  # 重新執行直到取得當年度的資料
                time.sleep(0.2)
                current_contents = self.fetcher.find_element(table_xpath).text
            records = get_records(self, year, table_xpath + '//tr')
            table.append(records)
            previous_contents = self.fetcher.find_element(table_xpath).text
        return table

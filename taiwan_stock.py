import webpage_fetcher
import time
from lxml import etree


class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()

    def get_financial_statements(self):
        # TODO do something
        self.fetcher.exit()

    def get_codes(self):
        """取得台股上巿股票代號/名稱列表

        Returns:
            {list} -- 股票代號/名稱列表
        """
        codes = []
        response = self.fetcher.get_response(
            'http://www.twse.com.tw/zh/stockSearch/stockSearch', 'get')
        tree = etree.HTML(response.text)
        codes = tree.xpath('//table[@class="grid"]//a/text()')
        for code in codes:
            codes.append([code[0:4], code[4:]])
        return codes

    def get_basicinfo(self, stock_id):
        """取得台股上巿股票基本資料

        Arguments:
            stock_id {str} -- 股票代碼

        Returns:
            {dict} -- 基本資料
        """
        basic = {}
        response = self.fetcher.get_response(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            data='firstin=1&co_id=' + stock_id)
        html = etree.HTML(response.text)
        rows_xpath = etree.XPath('//table[@class="hasBorder"]//tr')
        title = ''
        for row in rows_xpath(html):
            if (row[0].text.strip() == '本公司'):
                basic[row[2].text.strip()] = row[1].text.strip()
                basic[row[5].text.strip()] = row[4].text.strip()
            if (row[0].text.strip() == '本公司採'):
                basic['會計年度月制(現)'] = row[1].text.strip()
            if (row[0].text.strip() == '本公司於'):
                basic['會計年度月制(前)'] = row[3].text.strip()
                basic['會計年度月制轉換'] = row[1].text.strip()
            if (row[0].text.strip() == '編製財務報告類型'):
                report_type = row[1].text.strip()
                basic[row[0].text.strip()] = report_type[1:3] if report_type[
                    0] == '●' else report_type[4:6]
            else:
                # TODO 改用enumerate, start=1
                for index in range(len(row)):
                    field = row[index]
                    if (index % 2 == 0):
                        if (field.tag == 'th'):
                            title = field.text.strip()
                            basic[title] = ''
                    if (index % 2 == 1):
                        if (field.tag == 'td'):
                            basic[title] = field.text.strip()
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

    def get_table(self, url, option_xpath, top_n_count, table_xpath):
        """取得表格內容

        Arguments:
            url {str} -- 來源網址
            option_xpath {str} -- 年度下拉清單的XPATH
            top_n_count {int} -- 取前n個選項, 輸入0=全取
            table_xpath {str} -- 表格的XPATH

        Returns:
            {list} -- 表格內容
        """
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
        years = get_years(option_xpath)
        # TODO 修正
        for index, year in enumerate(years, start=1):
            self.fetcher.find_element(option_xpath + '[text()="' + year +
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

import webpage_fetcher
import excel_handler


# TODO 財務附註 http://mops.twse.com.tw/server-java/t164sb01
# http://mops.twse.com.tw/server-java/t164sb01
# http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2018&SSEASON=3&REPORT_ID=C
# http://mops.twse.com.tw/mops/web/t05st22_q1
# EPS改用程式計算
class TaiwanStock():
    fetcher = webpage_fetcher.WebpageFetcher()
    handler = excel_handler.ExcelHandler()

    def get_financial_statements(self):
        code_list = self.get_code_list()
        self.handler.sheet.range('A1').value = code_list
        self.handler.save_workbook('C:\\code_list.xlsx')
        self.handler.exit()

    def get_code_list(self):
        """取得台股上巿股票代號/名稱列表

        Returns:
            {list} -- 股票代號/名稱列表
        """
        code_list = []
        self.fetcher.request.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
        codes = self.fetcher.request.find_elements('//table[@class="grid"]//a/text()')
        for code in codes:
            code_list.append([code[0:4], code[4:]])
        return code_list

    def get_basic_info(self, stock_id):
        """取得台股上巿股票基本資料

        Arguments:
            stock_id {str} -- 股票代碼

        Returns:
            {dict} -- 基本資料
        """
        basic_info = {}
        self.fetcher.request.go_to(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            cell='firstin=1&co_id=' + stock_id)
        row_tags = self.fetcher.request.find_elements('//table[@class="hasBorder"]//tr')
        title = ''
        for row_tag in row_tags:
            if (row_tag[0].text.strip() == '本公司'):
                basic_info[row_tag[2].text.strip()] = row_tag[1].text.strip()
                basic_info[row_tag[5].text.strip()] = row_tag[4].text.strip()
            if (row_tag[0].text.strip() == '本公司採'):
                basic_info['會計年度月制(現)'] = row_tag[1].text.strip()
            if (row_tag[0].text.strip() == '本公司於'):
                basic_info['會計年度月制(前)'] = row_tag[3].text.strip()
                basic_info['會計年度月制轉換'] = row_tag[1].text.strip()
            if (row_tag[0].text.strip() == '編製財務報告類型'):
                report_type = row_tag[1].text.strip()
                basic_info[row_tag[0].text.strip()] = report_type[1:3] if report_type[
                    0] == '●' else report_type[4:6]
            else:
                for index, cell in enumerate(row_tag, start=1):
                    if (index % 2 == 1):
                        if (cell.tag == 'th'):
                            title = cell.text.strip()
                            basic_info[title] = ''
                    else:
                        if (cell.tag == 'td'):
                            basic_info[title] = cell.text.strip()
        return basic_info

    def get_table(self, url, top_n_count):
        """取得表格內容

        Arguments:
            url {str} -- 來源網址
            table_xpath {str} -- 表格的XPATH

        Returns:
            {list} -- 表格內容
        """
        def get_options(self, options_xpath):
            """取得下拉清單內容的list

            Arguments:
                tags_xpath {str} -- 下拉清單的XPATH

            Returns:
                {list} -- 下拉清單內容
            """
            options = []
            option_tags = self.fetcher.request.find_elements(options_xpath)
            for option_tag in option_tags:
                options.append(option_tag.text)
            return options

        self.fetcher.request.go_to('http://mops.twse.com.tw/server-java/t164sb01')
        years = self.fetcher.request.find_elements('//select[@id="SYEAR"]//option/@value')
        seasons = self.fetcher.request.find_elements('//select[@id="SSEASON"]//option/@value')

        return None

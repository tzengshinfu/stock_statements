from cls_webpage_fetcher import ClsWebpageFetcher
from cls_excel_handler import ClsExcelHandler
import datetime
import time
import random
from collections import namedtuple


# TODO 財務附註 http://mops.twse.com.tw/server-java/t164sb01
# http://mops.twse.com.tw/server-java/t164sb01
# http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2018&SSEASON=3&REPORT_ID=C
# http://mops.twse.com.tw/mops/web/t05st22_q1
# EPS改用程式計算
class ClsTaiwanStock():
    fetcher = ClsWebpageFetcher()
    excel = ClsExcelHandler()

    def get_financial_statement_files(self):
        result = self.excel.show_config_form()
        if result.action == 'Submit':
            self.excel.create_books_path(result.drive_letter + '\\' + result.directory_name)
            code_list = self.get_code_list()
            self.get_basic_info_files(code_list)
            self.get_statment_files(code_list)
            self.excel.show_popup('建立完成。')
            self.excel.close_config_form()
        else:
            self.excel.show_popup('取消建立!')
            self.excel.close_config_form()

    def get_basic_info_files(self, code_list: list):
        for code in code_list:
            book_path = self.excel.books_path + '\\' + code.id + '(' + code.name + ')' + '.xlsx'
            if not self.excel.is_book_existed(book_path):
                self.excel.add_book()
                basic_info = self.__get_basic_info(code.id)
                self.excel.write_to_sheet(basic_info)
                self.excel.save_book(book_path)
                time.sleep(random.randint(2, 7))

    def get_code_list(self) -> list:
        """取得台股上巿股票代號/名稱列表

            Returns:
                {list} -- 股票代號/名稱列表
        """
        code_list = []
        self.fetcher.request.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
        codes = self.fetcher.request.find_elements('//table[@class="grid"]//a/text()')
        stock_code = namedtuple('stock_code', 'id name')
        for code in codes:
            stock_code.id = code[0]
            stock_code.name = code[1]
            code_list.append(stock_code)
        return code_list

    def __get_basic_info(self, stock_id: str) -> list:
        """取得台股上巿股票基本資料

            Arguments:
                stock_id {str} -- 股票代碼

            Returns:
                {list} -- 基本資料
        """
        basic_info = {}
        self.fetcher.request.go_to('http://mops.twse.com.tw/mops/web/t05st03', 'post', 'firstin=1&co_id=' + stock_id)
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
                basic_info[row_tag[0].text.strip()] = report_type[1:3] if report_type[0] == '●' else report_type[4:6]
            else:
                for index, cell in enumerate(row_tag, start=1):
                    if (index % 2 == 1):
                        if (cell.tag == 'th'):
                            title = cell.text.strip()
                            basic_info[title] = ''
                    else:
                        if (cell.tag == 'td'):
                            basic_info[title] = cell.text.strip()
        basic_info_list = self.__convert_to_list(basic_info)
        return basic_info_list

    def __get_options(self, options_xpath: str) -> list:
        """取得下拉清單內容的list

            Arguments:
                options_xpath {str} -- 下拉清單的XPATH

            Returns:
                {list} -- 下拉清單內容
        """
        options = []
        option_tags = self.fetcher.request.find_elements(options_xpath)
        for option_tag in option_tags:
            options.append(option_tag.text)
        return options

    def __get_seasons(self) -> list:
        def get_mapping(month) -> dict:
            mapping = {
                '1': '1',
                '2': '1',
                '3': '1',
                '4': '2',
                '5': '2',
                '6': '2',
                '7': '3',
                '8': '3',
                '9': '3',
                '10': '4',
                '11': '4',
                '12': '4'
            }
            return mapping.get(month)

        self.fetcher.request.go_to('http://mops.twse.com.tw/server-java/t164sb01')
        years = self.fetcher.request.find_elements('//select[@id="SYEAR"]//option/@value')
        current_year = str(datetime.datetime.now().year)
        current_season = get_mapping(str(datetime.datetime.now().month))
        seasons = []
        for year in reversed(years):
            for season in reversed(['1', '2', '3', '4']):
                if str(year + season) >= str(current_year + current_season):
                    continue
                seasons.append([year, season])
        return seasons

    def get_table(self, stock_id: str, top_n_seasons_count: int = 0) -> list:
        """取得表格內容

            Arguments:
                stock_id {str} -- 股票代碼
                top_n_seasons_count {int} -- 取得前n季(0=全部)

            Returns:
                {list} -- 表格內容
        """
        seasons = self.__get_seasons()

        for index, season in enumerate(seasons, start=1):
            if top_n_seasons_count != 0:
                if index > top_n_seasons_count:
                    break
            self.fetcher.request.go_to('http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID={0}&SYEAR={1}&SSEASON={2}&REPORT_ID=C'.format(stock_id, season[0], season[1]))
            row_tags = self.fetcher.request.find_elements('//table[@class="result_table hasBorder"]//tr[not(th)]')
            records = []
            for row_tag in row_tags:
                record = []
                cell_tags = row_tag.xpath('./td[position() <= 2]')
                for cell_tag in cell_tags:
                    record.append(cell_tag.text)
                records.append(record)
            # TODO 寫入EXCEL

        return seasons

    def get_statment_files(self, code_list):
        for code in code_list:
            if not self.excel.is_book_existed(code[0], code[1]):
                # TODO 開啟活頁簿
                # TODO 檢查SEASON
                # TODO 開啟工作表
                # TODO 寫入excel
                pass

    def __convert_to_list(self, original_dict: dict)->list:
        converted_list = []
        for key, value in original_dict.items():
            converted_list.append([key, value])
        return converted_list

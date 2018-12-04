from app_webpage_fetcher import AppWebpageFetcher
from app_excel_handler import AppExcelHandler
import datetime
import PySimpleGUI as gui
import os
import time
import random


# TODO 財務附註 http://mops.twse.com.tw/server-java/t164sb01
# http://mops.twse.com.tw/server-java/t164sb01
# http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2018&SSEASON=3&REPORT_ID=C
# http://mops.twse.com.tw/mops/web/t05st22_q1
# EPS改用程式計算
class AppTaiwanStock():
    fetcher = AppWebpageFetcher()
    handler = AppExcelHandler()
    work_directory = None

    def get_financial_statement_files(self):
        self.get_basic_info_files()

    def get_basic_info_files(self):
        form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [
                [gui.Text('請輸入下載Excel存放的磁碟代號及目錄名')],
                [gui.Text('Drive', size=(15, 1)), gui.InputText('C')],
                [gui.Text('Folder', size=(15, 1)), gui.InputText('Excel')],
                [gui.Submit(), gui.Cancel()]
                ]
        button, values = form.Layout(layout).Read()

        if button == 'Submit':
            self.work_directory = values[0] + ':\\' + values[1] + '\\'
            if not os.path.exists(self.work_directory):
                os.makedirs(self.work_directory)

            code_list = self.__get_code_list()
            for code in code_list:
                excel_path = self.work_directory + code[0] + '(' + code[1] + ').xlsx'
                if not os.path.exists(excel_path):
                    basic_info = self.__get_basic_info(code[0])
                    self.handler.sheet.range('A1').value = basic_info
                    self.handler.save_workbook(excel_path)
                    time.sleep(random.randint(2, 5))
            gui.Popup('建立完成。')

            self.handler.exit()
        else:
            gui.Popup('取消建立!')

    def __get_code_list(self) -> list:
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

    def __get_basic_info(self, stock_id: str) -> dict:
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
            'firstin=1&co_id=' + stock_id)
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

    def get_options(self, options_xpath: str) -> list:
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

    def get_seasons(self) -> list:
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
        seasons = self.get_seasons()

        for index, season in enumerate(seasons, start=1):
            if top_n_seasons_count != 0:
                if index > top_n_seasons_count:
                    break
            self.fetcher.request.go_to('http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID={0}&SYEAR={1}&SSEASON={2}&REPORT_ID=C'.format(stock_id, season[0], season[1]))
            row_tags = self.fetcher.request.find_elements('//table[@class="result_table hasBorder"]//tr[not(th)]')
            records = []
            for row_tag in row_tags:
                record = []
                cell_tags = row_tag.xpath('./td')
                for cell_tag in cell_tags:
                    record.append(cell_tag.text)
                records.append(record)
            # TODO 寫入EXCEL

        return seasons

from cls_webpage_fetcher import ClsWebpageFetcher
from cls_excel_handler import ClsExcelHandler
import datetime
import typing
from lxml import etree
from typing import List
from typing import Union
import PySimpleGUI as gui


class ClsTaiwanStock():
    fetcher = ClsWebpageFetcher()
    excel = ClsExcelHandler()
    current_process: int = 0
    total_processes: int = 0
    table_count: int = 8  # 每個股票要擷取的Excel表格總數

    def main(self):
        config = self.show_config_form()
        if config.action == 'Submit':
            self.show_running_process()
            self.excel.open_books_directory(config.drive_letter + '\\' + config.directory_name)
            stock_list = self.get_stock_list()
            self.set_total_processes(stock_list)
            self.get_basic_info_files(stock_list)
            self.get_statment_files(stock_list)
            self.get_analysis_files(stock_list)
            self.get_dividend_files(stock_list)
            self.show_popup('建立完成。')
        else:
            self.show_popup('取消建立!')

    def get_basic_info_files(self, stock_list: List[typing.NamedTuple('stock', [('id', str), ('name', str)])]):
        """取得台股上巿股票基本資料檔案

            Arguments:
                stock_list {List[typing.NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        for stock in stock_list:
            book_path = self.excel.books_path + '\\' + stock.id + '(' + stock.name + ')_基本資料' + '.xlsx'
            if not self.excel.is_book_existed(book_path):
                self.excel.open_book(book_path)
                self.fetcher.wait(2, 7)
                basic_info = self.__get_basic_info(stock.id)
                self.excel.write_to_sheet(basic_info)
                self.excel.save_book(book_path)
                self.current_process += 1

    def get_stock_list(self) -> List[typing.NamedTuple('stock', [('id', str), ('name', str)])]:
        """取得台股上巿股票代號/名稱列表

            Returns:
                {List[typing.NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        stock_list = []
        self.fetcher.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
        stock_datas = self.fetcher.find_elements('//table[@class="grid"]//a/text()')
        stock = typing.NamedTuple('stock', [('id', str), ('name', str)])
        for stock_data in stock_datas:
            stock.id = stock_data[0:4]
            stock.name = stock_data[4:]
            stock_list.append(stock)
        return stock_list

    def __get_basic_info(self, stock_id: str) -> List:
        """取得台股上巿股票基本資料

            Arguments:
                stock_id {str} -- 股票代碼

            Returns:
                {list} -- 基本資料
        """
        basic_info = {}
        self.fetcher.go_to('http://mops.twse.com.tw/mops/web/t05st03', 'post', 'firstin=1&co_id=' + stock_id)
        row_tags = self.fetcher.find_elements('//table[@class="hasBorder"]//tr')
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
        basic_info_list = self.__to_list(basic_info)
        return basic_info_list

    def __get_periods(self, top_n_seasons_count: int = 0) -> List:
        def get_season(month: str) -> str:
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

        self.fetcher.go_to('http://mops.twse.com.tw/server-java/t164sb01')
        years = self.fetcher.find_elements('//select[@id="SYEAR"]//option/@value')
        current_year = str(datetime.datetime.now().year)
        current_season = get_season(str(datetime.datetime.now().month))
        periods = []
        period = typing.NamedTuple('period', [('year', str), ('season', str)])
        index = 0
        for year in reversed(years):
            for season in reversed(['1', '2', '3', '4']):
                if str(year + season) >= str(current_year + current_season):
                    continue
                index += 1
                if top_n_seasons_count != 0 and index > top_n_seasons_count:
                    return periods
                period.year = year
                period.season = season
                periods.append(period)
        return periods

    def __get_statment_table(self, table_type: str) -> List[str]:
        """取得表格內容

            Arguments:
                table_type {str} -- 股票代碼

            Returns:
                {List[str]} -- 表格內容
        """
        if table_type == '資產負債表':
            item_xpath = '//table[@class="result_table hasBorder"]//tr[not(th)]'
        elif table_type == '總合損益表':
            item_xpath = '//table[@class="main_table hasBorder"]//tr[not(th)]'
        elif table_type == '現金流量表':
            item_xpath = '//table[@class="main_table hasBorder"]//tr[not(th)]'
        elif table_type == '股東權益表':
            item_xpath = '//table[@class="result_table1 hasBorder"]//tr[not(th)]'
        elif table_type == '財務備註':
            item_xpath = '//table[@class="main_table hasBorder"]//tr[not(th)]'
        else:
            raise ValueError('類型只能是[資產負債表/總合損益表/股東權益表/現金流量表/財務備註]其中之一')

        row_tags = self.fetcher.find_elements(item_xpath)
        records = []
        for row_tag in row_tags:
            record = []
            cell_tags = row_tag.xpath('./td[position() <= 2]')
            for cell_tag in cell_tags:
                record.append(cell_tag.text)
            records.append(record)
        return records

    def get_statment_files(self, stock_list: List[typing.NamedTuple('stock', [('id', str), ('name', str)])]):
        """取得資產負債表/總合損益表/股東權益表/現金流量表/財務備註內容

            Arguments:
                stock_list {List[typing.NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        def get_statment_file(stock: typing.Namedtuple, period: typing.Namedtuple, table_type: str):
            book_path = self.excel.books_path + '\\' + stock.id + '(' + stock.name + ')_{0}'.format(table_type) + '.xlsx'
            self.excel.open_book(book_path)
            sheet_name = period.year + '_' + period.season
            if not self.excel.is_sheet_existed(sheet_name):
                self.excel.open_sheet(sheet_name)
                table = self.__get_statment_table(table_type)
                self.excel.write_to_sheet(table)
            self.excel.save_book(book_path)
            self.current_process += 1

        periods = self.__get_periods(0)

        for stock in stock_list:
            for period in periods:
                self.fetcher.wait(2, 7)
                self.fetcher.go_to('http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID={0}&SYEAR={1}&SSEASON={2}&REPORT_ID=C'.format(stock.id, period.year, period.season))
                get_statment_file(stock, period, '資產負債表')
                get_statment_file(stock, period, '總合損益表')
                get_statment_file(stock, period, '股東權益表')
                get_statment_file(stock, period, '現金流量表')
                get_statment_file(stock, period, '財務備註')

    def __to_list(self, source: Union[dict, etree.Element]) -> List[str]:
        result = []
        if type(source) is dict:
            for key, value in source.items():
                result.append([key, value])
            return result
        elif type(source) is etree._Element:
            for row in source:
                record = []
                for cell in row:
                    record.append(cell.text)
                result.append(record)
            return result
        else:
            raise ValueError('source型態只能是[dict/etree._Element]其中之一')

    def get_analysis_files(self, stock_list: List[typing.NamedTuple('stock', [('id', str), ('name', str)])]):
        """取得財務分析

            Arguments:
                stock_list {List[typing.NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        periods = self.__get_periods(0)
        for stock in stock_list:
            for period in periods:
                self.fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st22', 'post', data='encodeURIComponent=1&run=Y&step=1&TYPEK=sii&year={1}&isnew=true&co_id={0}&firstin=1&off=1&ifrs=Y'.format(stock.id, period.year))
                table = self.fetcher.find_elements('//table[@class="hasBorder"]')
                list1 = self.__to_list(table)
                self.excel.write_to_sheet(list1)
                book_path = self.excel.books_path + '\\' + stock.id + '(' + stock.name + ')_財務分析.xlsx'
                self.excel.save_book(book_path)
                self.current_process += 1

    def get_dividend_files(self, stock_list: List[typing.NamedTuple('stock', [('id', str), ('name', str)])]):
        """取得股利分派情形

            Arguments:
                stock_list {List[typing.NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        periods = self.__get_periods(0)
        for stock in stock_list:
            for period in periods:
                self.fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st09', 'post', data='encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=true&co_id={0}&year={1}'.format(stock.id, period.year))
                table = self.fetcher.find_elements('//table[@class="hasBorder"]')
                list1 = self.__to_list(table)
                self.excel.write_to_sheet(list1)
                book_path = self.excel.books_path + '\\' + stock.id + '(' + stock.name + ')_股利分派情形.xlsx'
                self.excel.save_book(book_path)
                self.current_process += 1

    def show_config_form(self) -> typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)]):
        """開啟設定介面

            Returns:
                typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)]) -- 執行動作/磁碟代號/目錄名稱
        """
        self.form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [[gui.Text('請輸入下載Excel存放的磁碟代號及目錄名稱')], [gui.Text('Drive', size=(15, 1)), gui.InputText('Z')], [gui.Text('Folder', size=(15, 1)), gui.InputText('Excel')], [gui.Submit(), gui.Cancel()]]
        result = typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)])
        window = self.form.Layout(layout)
        return_values = window.Read()
        window.Close()
        result.action = return_values[0]
        result.drive_letter = return_values[1][0]
        result.directory_name = return_values[1][1]
        return result

    def show_popup(self, message: str):
        """顯示跳顯訊息

            Arguments:
                message {str} -- 訊息文字
        """
        gui.Popup(message)

    def show_running_process(self):
        self.form = gui.FlexForm('處理中')
        layout = [[gui.Text('完成進度')], [gui.Text('完成進度', key='current_processing')], [gui.ProgressBar(self.total_processes, orientation='h', size=(20, 20), key='progressbar')], [gui.Cancel()]]
        window = self.form.Layout(layout)
        while True:
            event, values = window.Read(timeout=0)
            if event is None or event == 'Cancel':
                gui.Popup('下載已中止')
                raise SystemExit()
            if self.total_processes > 0 and self.current_process > 0 and self.total_processes == self.current_process:
                break
            window.FindElement('progressbar').UpdateBar(str(self.current_process))
            window.FindElement('current_processing').Update(str(self.current_process) + '/' + str(self.total_processes))
        window.Close()

    def set_total_processes(self, stock_list: List[typing.NamedTuple('stock', [('id', str), ('name', str)])]):
        self.total_processes = len(stock_list) * self.table_count

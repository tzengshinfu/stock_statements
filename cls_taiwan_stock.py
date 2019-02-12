from cls_webpage_fetcher import ClsWebpageFetcher
from cls_excel_handler import ClsExcelHandler
import datetime
from lxml import etree
from typing import List
from typing import Union
from typing import NamedTuple
import PySimpleGUI as gui
import asyncio


class ClsTaiwanStock():
    def __init__(self):
        self._fetcher = ClsWebpageFetcher()
        self._excel = ClsExcelHandler()
        self._current_process: int = 0
        self._total_processes: int = 0
        self._sheet_count: int = 8  # 每個股票要擷取的Excel表格總數
        self._task_runner = None
        self._current_stock_index: int = 0

    def main(self):
        config = self.show_config_form()
        if config.action == 'Submit':
            self._excel.open_books_directory(config.drive_letter + ':\\' + config.directory_name)
            stock_list = self.get_stock_list()
            self.set_total_processes(stock_list)
            self._task_runner = asyncio.get_event_loop()
            self._task_runner.create_task(self.show_running_process())
            tasks = self._get_chained_tasks([
                [self.get_basic_info_files, {'stock_list': stock_list}],
                [self.get_statment_files, {'stock_list': stock_list, 'top_n_seasons': int(config.top_n_seasons)}],
                [self.get_analysis_files, {'stock_list': stock_list, 'top_n_seasons': int(config.top_n_seasons)}],
                [self.get_dividend_files, {'stock_list': stock_list, 'top_n_seasons': int(config.top_n_seasons)}]
                ])
            self._task_runner.create_task(tasks)
            self._task_runner.run_forever()
            self.show_popup('建立完成。')
        else:
            self.show_popup('取消建立!')

    async def get_basic_info_files(self, **kwargs):
        """
        取得台股上巿股票基本資料檔案

        Arguments:
            stock_list {List[NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        def get_basic_info(stock_id: str) -> List[List[str]]:
                """
                取得台股上巿股票基本資料

                Arguments:
                    stock_id {str} -- 股票代碼

                Returns:
                    {List[List[str]]} -- 基本資料
                """
                basic_info = dict()
                self._fetcher.go_to('http://mops.twse.com.tw/mops/web/t05st03', 'post', 'firstin=1&co_id=' + stock_id)
                rows = self._fetcher.find_elements('//table[@class="hasBorder"]//tr')
                title = ''
                for row in rows:
                    if (row[0].text.strip() == '本公司'):
                        basic_info[row[2].text.strip()] = row[1].text.strip()
                        basic_info[row[5].text.strip()] = row[4].text.strip()
                    if (row[0].text.strip() == '本公司採'):
                        basic_info['會計年度月制(現)'] = row[1].text.strip()
                    if (row[0].text.strip() == '本公司於'):
                        basic_info['會計年度月制(前)'] = row[3].text.strip()
                        basic_info['會計年度月制轉換'] = row[1].text.strip()
                    if (row[0].text.strip() == '編製財務報告類型'):
                        report_type = row[1].text.strip()
                        basic_info[row[0].text.strip()] = report_type[1:3] if report_type[0] == '●' else report_type[4:6]
                    else:
                        for index, cell in enumerate(row, start=1):
                            if (index % 2 == 1):
                                if (cell.tag == 'th'):
                                    title = cell.text.strip()
                                    basic_info[title] = ''
                            else:
                                if (cell.tag == 'td'):
                                    basic_info[title] = cell.text.strip()
                basic_info_list = self._to_list(basic_info)
                return basic_info_list

        stock = kwargs['stock_list'][self._current_stock_index]
        book_path = self._excel._books_path + '\\' + stock.id + '(' + stock.name + ')_基本資料' + '.xlsx'
        if not self._excel.is_book_existed(book_path):
            self._excel.open_book(book_path)
            self._fetcher.wait(1, 2)
            basic_info = get_basic_info(stock.id)
            self._excel.write_to_sheet(basic_info)
            self._excel.save_book(book_path)
        self._current_process += 1
        self._current_stock_index += 1
        if self._current_stock_index < (len(kwargs['stock_list']) - 1):
            await asyncio.sleep(0)
        else:
            self._current_stock_index = 0
            if 'next_task' in kwargs:
                asyncio.ensure_future(kwargs['next_task'])

    def get_stock_list(self) -> List[NamedTuple('stock', [('id', str), ('name', str)])]:
        """
        取得台股上巿股票代號/名稱列表

        Returns:
            {List[NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
        """
        stock_list = list()
        self._fetcher.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
        stock_datas = self._fetcher.find_elements('//table[@class="grid"]//a/text()')
        stock = NamedTuple('stock', [('id', str), ('name', str)])
        for stock_data in stock_datas:
            stock.id = stock_data[0:4]
            stock.name = stock_data[4:]
            stock_list.append(stock)
        return stock_list

    def _get_periods(self, top_n_seasons: int = 0) -> List[NamedTuple('period', [('year', str), ('season', str)])]:
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

        self._fetcher.go_to('http://mops.twse.com.tw/server-java/t164sb01')
        years = self._fetcher.find_elements('//select[@id="SYEAR"]//option/@value')
        current_year = str(datetime.datetime.now().year)
        current_season = get_season(str(datetime.datetime.now().month))
        periods = list()
        period = NamedTuple('period', [('year', str), ('season', str)])
        index = 0
        for year in reversed(years):
            for season in reversed(['1', '2', '3', '4']):
                if str(year + season) >= str(current_year + current_season):
                    continue
                index += 1
                if top_n_seasons != 0 and index > top_n_seasons:
                    return periods
                period.year = year
                period.season = season
                periods.append(period)
        return periods

    async def get_statment_files(self, **kwargs):
        """
        取得資產負債表/總合損益表/股東權益表/現金流量表/財務備註內容

        Arguments:
            stock_list {List[NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
            top_n_seasons {int} -- 前n季(0=不限)
        """
        def get_statment_file(stock: NamedTuple('stock', [('id', str), ('name', str)]), period: NamedTuple('period', [('year', str), ('season', str)]), table_type: str):
            def get_statment_table(table_type: str) -> List[str]:
                """
                取得表格內容

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
                    raise ValueError('table_type值只能是(資產負債表/總合損益表/股東權益表/現金流量表/財務備註)其中之一')

                rows = self._fetcher.find_elements(item_xpath)
                records = list()
                for row in rows:
                    record = list()
                    cells = row.xpath('./td[position() <= 2]')
                    for cell in cells:
                        record.append(cell.text)
                    records.append(record)
                return records

            book_path = self._excel._books_path + '\\' + stock.id + '(' + stock.name + ')_{0}'.format(table_type) + '.xlsx'
            self._excel.open_book(book_path)
            sheet_name = period.year + '_' + period.season
            if not self._excel.is_sheet_existed(sheet_name):
                self._excel.open_sheet(sheet_name)
                table = self._get_statment_table(table_type)
                self._excel.write_to_sheet(table)
            self._excel.save_book(book_path)
            self._current_process += 1

        periods = self._get_periods(kwargs['top_n_seasons'])
        stock = kwargs['stock_list'][self._current_stock_index]
        for period in periods:
            self._fetcher.wait(1, 2)
            self._fetcher.go_to('http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID={0}&SYEAR={1}&SSEASON={2}&REPORT_ID=C'.format(stock.id, period.year, period.season))
            get_statment_file(stock, period, '資產負債表')
            get_statment_file(stock, period, '總合損益表')
            get_statment_file(stock, period, '股東權益表')
            get_statment_file(stock, period, '現金流量表')
            get_statment_file(stock, period, '財務備註')
        self._current_process += 1
        self._current_stock_index += 1
        if self._current_stock_index < (len(kwargs['stock_list']) - 1):
            await asyncio.sleep(0)
        else:
            self._current_stock_index = 0
            if 'next_task' in kwargs:
                asyncio.ensure_future(kwargs['next_task'])

    def _to_list(self, source: Union[dict, etree.Element]) -> List[List[str]]:
        result = list()
        if type(source) is dict:
            for key, value in source.items():
                result.append([key, value])
            return result
        elif type(source) is etree._Element:
            for row in source:
                record = list()
                for cell in row:
                    record.append(cell.text)
                result.append(record)
            return result
        else:
            raise ValueError('source型別只能是(dict/etree._Element)其中之一')

    async def get_analysis_files(self, **kwargs):
        """
        取得財務分析

        Arguments:
            stock_list {List[NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
            top_n_seasons {int} -- 前n季(0=不限)
        """
        periods = self._get_periods(kwargs['top_n_seasons'])
        stock = kwargs['stock_list'][self._current_stock_index]
        for period in periods:
            self._fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st22', 'post', data='encodeURIComponent=1&run=Y&step=1&TYPEK=sii&year={1}&isnew=true&co_id={0}&firstin=1&off=1&ifrs=Y'.format(stock.id, period.year))
            table = self._fetcher.find_elements('//table[@class="hasBorder"]')
            rows = self._to_list(table)
            self._excel.write_to_sheet(rows)
            book_path = self._excel._books_path + '\\' + stock.id + '(' + stock.name + ')_財務分析.xlsx'
            self._excel.save_book(book_path)
        self._current_process += 1
        self._current_stock_index += 1
        if self._current_stock_index < (len(kwargs['stock_list']) - 1):
            await asyncio.sleep(0)
        else:
            self._current_stock_index = 0
            if 'next_task' in kwargs:
                asyncio.ensure_future(kwargs['next_task'])

    async def get_dividend_files(self, **kwargs):
        """
        取得股利分派情形

        Arguments:
            stock_list {List[NamedTuple('stock', [('id', str), ('name', str)])]} -- 股票代號/名稱列表
            top_n_seasons {int} -- 前n季(0=不限)
        """
        periods = self._get_periods(kwargs['top_n_seasons'])
        stock = kwargs['stock_list'][self._current_stock_index]
        for period in periods:
            self._fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st09', 'post', data='encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=true&co_id={0}&year={1}'.format(stock.id, period.year))
            table = self._fetcher.find_elements('//table[@class="hasBorder"]')
            rows = self._to_list(table)
            self._excel.write_to_sheet(rows)
            book_path = self._excel._books_path + '\\' + stock.id + '(' + stock.name + ')_股利分派情形.xlsx'
            self._excel.save_book(book_path)
        self._current_process += 1
        self._current_stock_index += 1
        if self._current_stock_index < (len(kwargs['stock_list']) - 1):
            await asyncio.sleep(0)
        else:
            self._current_stock_index = 0
            if 'next_task' in kwargs:
                asyncio.ensure_future(kwargs['next_task'])

    def show_config_form(self) -> NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str), ('top_n_seasons', str)]):
        """
        開啟設定介面

        Returns:
            NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str), ('top_n_seasons', str)]) -- 執行動作/磁碟代號/目錄名稱/前n季
        """
        form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [[gui.Text('請輸入下載Excel存放的磁碟代號及目錄名稱')], [gui.Text('磁碟代號', size=(15, 1), key='Drive'), gui.InputText('Z')], [gui.Text('目錄名稱', size=(15, 1), key='Folder'), gui.InputText('Excel')], [gui.Text('請輸入前n季(0=不限)')], [gui.Text('季數', size=(15, 1), key='TopNSeasons'), gui.InputText('1')], [gui.Submit(), gui.Cancel()]]
        window = form.Layout(layout)
        return_values = window.Read()
        window.Close()
        result = NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str), ('top_n_seasons', str)])
        result.action = return_values[0]
        result.drive_letter = return_values[1][0]
        result.directory_name = return_values[1][1]
        result.top_n_seasons = return_values[1][2]
        return result

    def show_popup(self, message: str):
        """
        顯示跳顯訊息

        Arguments:
            message {str} -- 訊息文字
        """
        gui.Popup(message)

    async def show_running_process(self):
        form = gui.FlexForm('處理中')
        layout = [[gui.Text('完成進度', key='current_processing')], [gui.ProgressBar(self._total_processes, orientation='h', size=(20, 20), key='progressbar')], [gui.Cancel()]]
        window = form.Layout(layout)
        while True:
            event, values = window.Read(timeout=10)
            if event is None or event == 'Cancel':
                gui.Popup('下載已中止')
                raise SystemExit('使用者中止')
            if self._total_processes > 0 and self._current_process > 0 and self._total_processes == self._current_process:
                break
            window.FindElement('progressbar').UpdateBar(self._current_process)
            window.FindElement('current_processing').Update('完成進度' + str(self._current_process / self._total_processes) + '/' + '100')
            await asyncio.sleep(0)
        self._task_runner.stop()
        window.Close()

    def set_total_processes(self, stock_list: List[NamedTuple('stock', [('id', str), ('name', str)])]):
        self._total_processes = len(stock_list) * self._sheet_count

    def _get_chained_tasks(self, tasks):
        tasks.reverse()
        chained_tasks = None
        for task in tasks:
            func = task[0]
            param = task[1]
            if chained_tasks is not None:
                param['next_task'] = chained_tasks
            chained_tasks = func(**param)
        return chained_tasks

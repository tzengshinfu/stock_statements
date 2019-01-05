from openpyxl import Workbook
from openpyxl.compat import range
import os
import PySimpleGUI as gui
import tempfile
from typing import Union
from typing import List
import typing
from openpyxl import load_workbook
import PySimpleGUIQt as sg


class ClsExcelHandler():
    def __init__(self):
        self.books_path = tempfile.gettempdir()

    def __add_book(self):
        """新增活頁簿"""
        self.book = Workbook()
        self.sheet = self.book.active

    def save_book(self, book_path: str):
        """儲存活頁簿

            Arguments:
                book_path {str} -- 本機路徑
        """
        self.book.save(book_path)

    def write_to_sheet(self, values: Union[List[str], str]):
        """寫入工作表

            Arguments:
                values {Union[List[str], str]} -- 要寫入的值
        """
        if type(values) is List:
            for row in range(1, len(values)):
                self.sheet.append(values[row])
        elif type(values) is str:
            self.sheet.append(values)
        else:
            raise ValueError('values型態只能是(List[str]/str)其中之一')

    def open_books_directory(self, books_path: str):
        """開啟活頁簿預設儲存目錄

            Arguments:
                books_path {str} -- 本機路徑
        """
        if not os.path.exists(books_path):
            os.makedirs(books_path)
        self.books_path = books_path

    def show_config_form(self) -> typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)]):
        """開啟設定介面

            Returns:
                typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)]) -- 執行動作/磁碟代號/目錄名稱
        """
        self.form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [[gui.Text('請輸入下載Excel存放的磁碟代號及目錄名稱')], [gui.Text('Drive', size=(15, 1)), gui.InputText('Z')], [gui.Text('Folder', size=(15, 1)), gui.InputText('Excel')], [gui.Submit(), gui.Cancel()]]
        result = typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)])
        return_values = self.form.Layout(layout).Read()
        result.action = return_values[0]
        result.drive_letter = return_values[1][0]
        result.directory_name = return_values[1][1]
        return result

    def show_config_form2(self) -> typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)]):
        """開啟設定介面

            Returns:
                typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)]) -- 執行動作/磁碟代號/目錄名稱
        """
        self.form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [[gui.Text('請輸入下載Excel存放的磁碟代號及目錄名稱')], [gui.Text('Drive', size=(15, 1)), gui.InputText('Z')], [gui.Text('Folder', size=(15, 1)), gui.InputText('Excel')], [gui.Submit(), gui.Cancel()]]
        # result = typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)])
        while True:
            event, values = self.form.Layout(layout).Read()
            if event is None or event == 'Exit':
                break

    def show_popup(self, message: str):
        """顯示跳顯訊息

            Arguments:
                message {str} -- 訊息文字
        """
        gui.Popup(message)

    def close_config_form(self):
        """關閉設定介面"""
        self.form.close()

    def open_book(self, book_path: str):
        """開啟活頁簿(不存在則先建立)

            Arguments:
                book_path {str} -- 本機路徑
        """
        if not self.is_book_existed(book_path):
            self.__add_book()
        else:
            self.book = load_workbook(book_path)
            self.sheet = self.book.active

    def __add_sheet(self, sheet_name: str):
        """新增工作表

            Arguments:
                sheet_name {str} -- 工作表名稱
        """
        self.book.create_sheet(sheet_name)

    def open_sheet(self, sheet_name: str):
        """開啟工作表(不存在則先建立)

        Arguments:
            sheet_name {str} -- 工作表名稱
        """
        if not self.is_sheet_existed():
            self.__add_sheet(sheet_name)
        self.book.active = self.book.worksheets.index(self.get_sheet_by_name(sheet_name))

    def is_book_existed(self, book_path: str) -> bool:
        """判斷活頁簿是否存在

            Arguments:
                book_path {str} -- 本機路徑

            Returns:
                bool -- 回傳結果
        """
        return os.path.exists(book_path)

    def is_sheet_existed(self, sheet_name: str) -> bool:
        """判斷工作表是否存在

            Arguments:
                sheet_name {str} -- 工作表名稱

            Returns:
                bool -- 回傳結果
        """
        if sheet_name in self.book.sheetnames:
            return True
        else:
            return False

    def show_tray_icon(self):
        menu_def = ['BLANK', ['&Open', '---', '&Save', ['1', '2', ['a', 'b']], '&Properties', 'E&xit']]

        tray = sg.SystemTray(menu=menu_def, filename=r'1274834.ico')

        while True:  # The event loop
            menu_item = tray.Read()
            print(menu_item)
            if menu_item == 'Exit':
                break
            elif menu_item == 'Open':
                sg.Popup('Menu item chosen', menu_item)

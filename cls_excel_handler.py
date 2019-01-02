from openpyxl import Workbook
from openpyxl.compat import range
import os
import PySimpleGUI as gui
import tempfile
from typing import Union
import typing
from openpyxl import load_workbook


class ClsExcelHandler():
    def __init__(self):
        self.books_path = tempfile.gettempdir()

    def __add_book(self):
        self.book = Workbook()
        self.sheet = self.book.active

    def save_book(self, book_path: str):
        """儲存活頁簿

            Arguments:
                book_path {str} -- 本機路徑
        """
        self.book.save(book_path)

    def write_to_sheet(self, values: Union[list, str]):
        """寫入工作表

            Arguments:
                values {Union[list, str]} -- 要寫入的值
        """
        if type(values) is list:
            for row in range(1, len(values)):
                self.sheet.append(values[row])
        else:
            self.sheet.append(values)

    def open_books_directory(self, books_path: str):
        """開啟活頁簿預設儲存目錄

            Arguments:
                books_path {str} -- 本機路徑
        """
        if not os.path.exists(books_path):
            os.makedirs(books_path)
        self.books_path = books_path

    def show_config_form(self) -> typing.NamedTuple:
        """開啟設定介面

            Returns:
                typing.NamedTuple -- 執行動作/磁碟代號/目錄名稱
        """
        self.form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [[self.gui.Text('請輸入下載Excel存放的磁碟代號及目錄名稱')], [self.gui.Text('Drive', size=(15, 1)), self.gui.InputText('Z')], [self.gui.Text('Folder', size=(15, 1)), self.gui.InputText('Excel')], [self.gui.Submit(), self.gui.Cancel()]]
        result = typing.NamedTuple('result', [('action', str), ('drive_letter', str), ('directory_name', str)])
        return_values = self.form.Layout(layout).Read()
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

    def close_config_form(self):
        """關閉設定介面"""
        self.form.close()

    def open_book(self, book_path: str):
        """開啟活頁簿(不存在則先建立)

            Arguments:
                book_path {str} -- 本機路徑
        """
        if not self.is_book_existed():
            self.__add_book(book_path)
        self.book = load_workbook(book_path)
        self.sheet = self.book.active

    def __add_sheet(self, sheet_name: str):
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

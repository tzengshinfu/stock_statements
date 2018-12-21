from openpyxl import Workbook
from openpyxl.compat import range
import os
from collections import namedtuple
import PySimpleGUI as gui
import tempfile
from typing import Union
from openpyxl import load_workbook


class ClsExcelHandler():
    def __init__(self):
        self.books_path = tempfile.gettempdir()

    def __add_book(self):
        self.book = Workbook()
        self.sheet = self.book.active

    def save_book(self, book_path: str):
        self.book.save(book_path)

    def write_to_sheet(self, values: Union[list, str]):
        if type(values) is list:
            for row in range(1, len(values)):
                self.sheet.append(values[row])
        else:
            self.sheet.append(values)

    def open_books_directory(self, books_path: str):
        if not os.path.exists(books_path):
            os.makedirs(books_path)
        self.books_path = books_path

    def show_config_form(self) -> namedtuple:
        self.form = gui.FlexForm('設定台股上巿股票Excel存放路徑')
        layout = [[self.gui.Text('請輸入下載Excel存放的磁碟代號及目錄名')], [self.gui.Text('Drive', size=(15, 1)), self.gui.InputText('Z')], [self.gui.Text('Folder', size=(15, 1)), self.gui.InputText('Excel')], [self.gui.Submit(), self.gui.Cancel()]]
        result = namedtuple('result', 'action drive_letter directory_name')
        return_values = self.form.Layout(layout).Read()
        result.action = return_values[0]
        result.drive_letter = return_values[1][0]
        result.directory_name = return_values[1][1]
        return result

    def show_popup(self, message: str):
        gui.Popup(message)

    def close_config_form(self):
        self.form.close()

    def open_book(self, book_path: str):
        if not self.is_book_existed():
            self.__add_book(book_path)
        self.book = load_workbook(book_path)
        self.sheet = self.book.active

    def __add_sheet(self, sheet_name: str):
        self.book.create_sheet(sheet_name)

    def open_sheet(self, sheet_name: str):
        if not self.is_sheet_existed():
            self.__add_sheet(sheet_name)
        self.book.active = self.book.worksheets.index(self.get_sheet_by_name(sheet_name))

    def is_book_existed(self, book_path: str) -> bool:
        return os.path.exists(book_path)

    def is_sheet_existed(self, sheet_name: str) -> bool:
        if sheet_name in self.book.sheetnames:
            return True
        else:
            return False

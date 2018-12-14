from openpyxl import Workbook
from openpyxl.compat import range
import os
from collections import namedtuple
import PySimpleGUI as gui
import tempfile
from typing import Union


class ClsExcelHandler():
    def __init__(self):
        self.books_path = tempfile.gettempdir()

    def add_book(self):
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

    def create_books_path(self, books_path: str):
        self.books_path = books_path
        if not os.path.exists(self.books_path):
            os.makedirs(self.books_path)

    def is_book_existed(self, book_path: str):
        return os.path.exists(book_path)

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

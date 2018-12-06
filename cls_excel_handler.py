from openpyxl import Workbook
from openpyxl.compat import range
import os
import tempfile


class ClsExcelHandler():
    work_directory = tempfile.gettempdir()

    def __init__(self):
        pass

    def add_book(self):
        self.book = Workbook()
        self.sheet = self.book.active

    def save_book(self, stock_id, stock_name):
        self.book.save(self.get_book_path(stock_id, stock_name))

    def write_values(self, values):
        if type(values) is list:
            for row in range(1, len(values.items())):
                self.sheet.append(values[row])
        else:
            self.sheet.append(values)

    def create_work_directory(self, drive_letter: str, directory_name: str):
        self.work_directory = drive_letter + ':\\' + directory_name + '\\'
        if not os.path.exists(self.work_directory):
            os.makedirs(self.work_directory)

    def get_book_path(self, stock_id: str, stock_name: str)->str:
        return self.work_directory + stock_id + '(' + stock_name + ').xlsx'

    def is_book_existed(self, stock_id: str, stock_name: str):
        return os.path.exists(self.get_book_path(stock_id, stock_name))

    def convert_to_list(self, original_dict: dict)->list:
        converted_list = []
        for key, value in original_dict.items():
            converted_list.append([key, value])
        return converted_list

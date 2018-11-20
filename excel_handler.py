import xlwings as xw
import lazy_object_proxy


class ExcelHandler():
    def __init__(self):
        self.handler = lazy_object_proxy.Proxy(self.initial_handler)

    def initial_handler(self):
        return xw.App(visible=False)

    def save_workbook(self):
        book = self.handler.books[0]
        sheet = self.handler.sheets[0]

        sheet.range('A1').value = 73913

        book.save('d:\\desktop\\book.xlsx')
        self.exit()
        return 'd:\\desktop\\book.xlsx'

    def exit(self):
        self.handler.kill()
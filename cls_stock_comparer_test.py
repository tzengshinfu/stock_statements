import unittest
from pathlib import Path
import os
import fnmatch
from cls_excel_handler import ClsExcelHandler


class ClsStockComparerTest(unittest.TestCase):
    excel_handler = ClsExcelHandler()

    # region 初始方法
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
    # endregion

    def test_get_ebit(self):
        stock_ids = list()
        pathlist = Path('D:\\Excel').glob('**/*.xlsx')
        for path in pathlist:
            stock_id = str(path.name)[0:4]
            if stock_id not in stock_ids:
                stock_ids.append(stock_id)
        for file in os.listdir('D:\\Excel'):
            income_before_tax = 0
            if fnmatch.fnmatch(file, stock_id + '*_總合損益表.xlsx'):
                self.excel_handler.open_book('D:\\Excel\\' + file)
                for row in range(1, self.excel_handler._sheet.max_row):
                    if '稅前淨利' in self.excel_handler._sheet.cell(row, 1).value:
                        income_before_tax = self.excel_handler._sheet.cell(row, 2).value.replace(",", "")
        for file in os.listdir('D:\\Excel'):
            interest = 0
            if fnmatch.fnmatch(file, stock_id + '*_現金流量表.xlsx'):
                self.excel_handler.open_book('D:\\Excel\\' + file)
                for row in range(1, self.excel_handler._sheet.max_row):
                    if '利息費用' in self.excel_handler._sheet.cell(row, 1).value:
                        interest = self.excel_handler._sheet.cell(row, 2).value.replace(",", "")
        ebit = (int(income_before_tax) + int(interest)) / int(interest) if int(interest) > 0 else 0
        self.excel_handler.open_book('D:\\Excel\\' + stock_id + ".xlsx")
        self.excel_handler._sheet.cell(row, 1).value = ebit
        pass

    def test_get_roa(self):
            stock_ids = list()
            pathlist = Path('D:\\Excel').glob('**/*.xlsx')
            for path in pathlist:
                stock_id = str(path.name)[0:4]
                if stock_id not in stock_ids:
                    stock_ids.append(stock_id)
            for file in os.listdir('D:\\Excel'):
                income_before_tax = 0
                if fnmatch.fnmatch(file, stock_id + '*_總合損益表.xlsx'):
                    self.excel_handler.open_book('D:\\Excel\\' + file)
                    for row in range(1, self.excel_handler._sheet.max_row):
                        if '稅前淨利' in self.excel_handler._sheet.cell(row, 1).value:
                            income_before_tax = self.excel_handler._sheet.cell(row, 2).value.replace(",", "")
            for file in os.listdir('D:\\Excel'):
                capital = 0
                current_liabilities = 0
                current_finance_liabilities = 0
                if fnmatch.fnmatch(file, stock_id + '*_資產負債表.xlsx'):
                    self.excel_handler.open_book('D:\\Excel\\' + file)
                    for row in range(1, self.excel_handler._sheet.max_row):
                        if '資產總額' in self.excel_handler._sheet.cell(row, 1).value:
                            capital = self.excel_handler._sheet.cell(row, 2).value.replace(",", "")
                        if '流動負債合計' in self.excel_handler._sheet.cell(row, 1).value:
                            current_liabilities = self.excel_handler._sheet.cell(row, 2).value.replace(",", "")
                        if '透過損益按公允價值衡量之金融負債－流動' in self.excel_handler._sheet.cell(row, 1).value:
                            current_finance_liabilities = self.excel_handler._sheet.cell(row, 2).value.replace(",", "")
            roa = int(income_before_tax) / (int(capital) - (int(current_liabilities) + int(current_finance_liabilities))) if (int(capital) - (int(current_liabilities) + int(current_finance_liabilities))) > 0 else 0
            self.excel_handler.open_book('D:\\Excel\\' + stock_id + ".xlsx")
            self.excel_handler._sheet.cell(row, 1).value = roa
            pass


if __name__ == '__main__':
    tests = ['test_get_ebit']
    suite = unittest.TestSuite(map(ClsStockComparerTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

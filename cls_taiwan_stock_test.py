import unittest
from cls_taiwan_stock import ClsTaiwanStock
from cls_excel_handler import ClsExcelHandler
import typing
import glob
import tempfile
import os


class ClsTaiwanStockTest(unittest.TestCase):
    taiwan_stock = ClsTaiwanStock()
    excel_handler = ClsExcelHandler()

    # region 初始方法
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(self):


        self.stock_list = []
        stock = typing.NamedTuple('stock', [('id', str), ('name', str)])
        stock.id = '1101'
        stock.name = '亞泥'
        self.stock_list.append(stock)
        self.periods = []
        period = typing.NamedTuple('period', [('year', str), ('season', str)])
        period.year = '107'
        period.season = '03'
        self.periods.append(period)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
    # endregion

    def test_get_basic_info_files(self):
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            self.taiwan_stock.get_basic_info_files(stock)

    def test_get_statment_files_資產負債表(self):
        self.clear_file('資產負債表')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('資產負債表', stock, period)

    def test_get_statment_files_總合損益表(self):
        self.clear_file('總合損益表')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('總合損益表', stock, period)

    def test_get_statment_files_現金流量表(self):
        self.clear_file('現金流量表')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('現金流量表', stock, period)

    def test_get_statment_files_權益變動表(self):
        self.clear_file('權益變動表')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('權益變動表', stock, period)

    def test_get_statment_files_財報附註(self):
        self.clear_file('財報附註')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('財報附註', stock, period)

    def test_get_statment_files_財務分析(self):
        self.clear_file('財務分析')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('財務分析', stock, period)

    def test_get_statment_files_股利分配(self):
        self.clear_file('股利分配')
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock.get_statment_file('股利分配', stock, period)

    def clear_file(self, file_type):
        fileList = glob.glob(tempfile.gettempdir() + '\\*' + file_type + '.xlsx')
        for filePath in fileList:
                os.remove(filePath)


if __name__ == '__main__':
    tests = ['test_get_statment_files_現金流量表']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

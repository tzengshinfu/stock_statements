import unittest
from cls_taiwan_stock import ClsTaiwanStock
from cls_excel_handler import ClsExcelHandler
import typing


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

    def test_get_statment_files(self):
        self.taiwan_stock._total_process_count = 1
        for stock in self.stock_list:
            for period in self.periods:
                self.get_statment_files(stock, period)


if __name__ == '__main__':
    tests = ['test_get_basic_info_files']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

import unittest
from cls_taiwan_stock import ClsTaiwanStock


class ClsTaiwanStockTest(unittest.TestCase):
    stock = ClsTaiwanStock()

    # region 初始方法
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
    # endregion

    def test_get_basic_info_files(self):
        self.stock.get_basic_info_files()

    def test_get_table(self):
        self.stock.__get_statment_table('1101', 2)

    def test_setExcelPath(self):
        self.stock.set_excel_path()

    def test_get_financial_statement_files(self):
        self.stock.get_financial_statement_files()

    def test_get_analysis_files(self):
        stock_list = []
        self.stock.get_analysis_files(stock_list)


if __name__ == '__main__':
    tests = ['test_get_analysis_files']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

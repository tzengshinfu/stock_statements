import unittest
from cls_taiwan_stock import ClsTaiwanStock
from collections import namedtuple


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
        stock = namedtuple('stock', 'id name')
        stock.id = '1101'
        stock.name = '亞泥'
        stock_list.append(stock)
        periods = []
        period = namedtuple('period', 'year season')
        period.year = '2018'
        period.season = '1'
        periods.append(period)

        for stock in stock_list:
            for period in periods:
                self.fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st22', 'post', data='encodeURIComponent=1&run=Y&step=1&TYPEK=sii&year={1}&isnew=true&co_id={0}&firstin=1&off=1&ifrs=Y'.format(stock.id, period.year))
                print(self.fetcher.response)


if __name__ == '__main__':
    tests = ['test_get_analysis_files']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

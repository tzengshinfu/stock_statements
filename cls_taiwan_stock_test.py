import unittest
from cls_taiwan_stock import ClsTaiwanStock
import typing


class ClsTaiwanStockTest(unittest.TestCase):
    stock = ClsTaiwanStock()

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
        period.year = '2018'
        period.season = '1'
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
        self.stock.get_basic_info_files()

    def test_get_table(self):
        self.stock.__get_statment_table('1101', 2)

    def test_setExcelPath(self):
        self.stock.set_excel_path()

    def test_get_financial_statement_files(self):
        self.stock.get_financial_statement_files()

    def test_get_analysis_files(self):
        for stock in self.stock_list:
            for period in self.periods:
                self.stock.fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st22', 'post', data='encodeURIComponent=1&run=Y&step=1&TYPEK=sii&year={1}&isnew=true&co_id={0}&firstin=1&off=1&ifrs=Y'.format(stock.id, period.year))
                print(self.stock.fetcher.response)

    def test_get_dividend_files(self):
        for stock in self.stock_list:
            for period in self.periods:
                self.stock.fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st22', 'post', data='encodeURIComponent=1&run=Y&step=1&TYPEK=sii&year={1}&isnew=true&co_id={0}&firstin=1&off=1&ifrs=Y'.format(stock.id, period.year))
                print(self.stock.fetcher.find_elements('//table[@class="hasBorder"]//tr'))


if __name__ == '__main__':
    tests = ['test_get_dividend_files']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

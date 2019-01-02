import unittest
from cls_taiwan_stock import ClsTaiwanStock
from cls_excel_handler import ClsExcelHandler
import typing


class ClsTaiwanStockTest(unittest.TestCase):
    stock = ClsTaiwanStock()
    excel = ClsExcelHandler()

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
                self.stock.fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st09', 'post', data='encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=true&co_id={0}&year={1}'.format(stock.id, period.year))
                dividend_info = self.stock.fetcher.find_elements('//table[@class="hasBorder"]//tr')
                self.excel.write_to_sheet(dividend_info)
                self.excel.save_book('D:\\Desktop\\a.xlsx')


if __name__ == '__main__':
    tests = ['test_get_dividend_files']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

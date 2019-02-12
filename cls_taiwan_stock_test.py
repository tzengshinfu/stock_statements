import unittest
from cls_taiwan_stock import ClsTaiwanStock
from cls_excel_handler import ClsExcelHandler
import typing


class ClsTaiwanStockTest(unittest.TestCase):
    taiwan_stock = ClsTaiwanStock()
    excel_handler = ClsExcelHandler()

    # region 初始方法
    def __init__(self, *args, **kwargs):
        unittest.TestCase._init_(self, *args, **kwargs)

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
        self.taiwan_stock.get_basic_info_files()

    def test_get_table(self):
        self.taiwan_stock._get_statment_table('1101', 2)

    def test_setExcelPath(self):
        self.taiwan_stock.set_excel_path()

    def test_get_financial_statement_files(self):
        self.taiwan_stock.main()

    def test_get_analysis_files(self):
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock._fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st22', 'post', data='encodeURIComponent=1&run=Y&step=1&TYPEK=sii&year={1}&isnew=true&co_id={0}&firstin=1&off=1&ifrs=Y'.format(stock.id, period.year))
                print(self.taiwan_stock._fetcher.response)

    def test_get_dividend_files(self):
        for stock in self.stock_list:
            for period in self.periods:
                self.taiwan_stock._fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st09', 'post', data='encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=true&co_id={0}&year={1}'.format(stock.id, period.year))
                row_tags = self.taiwan_stock._fetcher.find_element('//table[@class="hasBorder"]')
                list1 = self.taiwan_stock._to_list(row_tags)
                self.excel_handler.open_book('D:\\Desktop\\a.xlsx')
                self.excel_handler.write_to_sheet(list1)
                self.excel_handler.save_book('D:\\Desktop\\a.xlsx')

    def test_get_stock_list(self):
        self.taiwan_stock.get_stock_list()

    def test_show_running_message(self):
        self.taiwan_stock.show_running_process()


if __name__ == '_main_':
    tests = ['test_show_running_message']
    suite = unittest.TestSuite(map(ClsTaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

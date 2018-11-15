import unittest
import taiwan_stock


class TaiwanStockTest(unittest.TestCase):
    stock = taiwan_stock.TaiwanStock()

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

    def test_get_codes(self):
        codes = self.stock.get_codes()
        self.assertNotEqual(codes, None)

    def test_get_basicinfo_1101(self):
        basics = self.stock.get_basicinfo('1101')
        self.assertNotEqual(basics, None)

    def test_get_eps(self):
        url = 'https://www.cnyes.com/twstock/financial4.aspx'
        years = ['2018Q3', '2018Q2']
        table_xpath = '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]'
        eps = self.stock.get_table(url, years, table_xpath)
        self.assertNotEqual(eps, None)

    def test_get_balance_sheet(self):
        balance_sheet = self.stock.get_balance_sheet()
        self.assertNotEqual(balance_sheet, None)


if __name__ == '__main__':
    tests = ['test_get_basicinfo_1101']
    suite = unittest.TestSuite(map(TaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

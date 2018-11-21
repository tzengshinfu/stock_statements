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
        codes = self.stock.get_code_list()
        self.assertNotEqual(codes, [])

    def test_get_basicinfo_1101(self):
        basics = self.stock.get_basic_info('1101')
        self.assertNotEqual(basics, {})

    def test_get_eps_2seasons(self):
        url = 'https://www.cnyes.com/twstock/financial4.aspx'
        years_xpath = '//select[@id="ctl00_ContentPlaceHolder1_D3"]/option'
        table_xpath = '//table[@id="ctl00_ContentPlaceHolder1_GridView1"]'
        eps = self.stock.get_table(url, years_xpath, 2, table_xpath)
        self.assertNotEqual(eps, [])

    def test_get_balance_sheet_2seasons(self):
        url = 'http://www.cnyes.com/twstock/bs/1101.htm'
        years_xpath = '//select[@id="ctl00_ContentPlaceHolder1_DropDownList1"]/option'
        table_xpath = '//table[@id="ctl00_ContentPlaceHolder1_htmltb1"]'
        balance_sheet = self.stock.get_table(url, years_xpath, 2, table_xpath)
        self.assertNotEqual(balance_sheet, [])

    def test_get_financial_statements(self):
        self.stock.get_financial_statements()


if __name__ == '__main__':
    tests = ['test_get_balance_sheet_2seasons']
    suite = unittest.TestSuite(map(TaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

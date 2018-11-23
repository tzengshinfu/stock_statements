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
        eps = self.stock.get_eps(2)
        self.assertNotEqual(eps, [])

    def test_get_balance_sheet_2seasons(self):
        balance_sheet = self.stock.get_balance_sheet('1101', 2)
        self.assertNotEqual(balance_sheet, [])

    def test_get_financial_statements(self):
        self.stock.get_financial_statements()


if __name__ == '__main__':
    tests = ['test_get_balance_sheet_2seasons']
    suite = unittest.TestSuite(map(TaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

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

    def test_get_basics_1101(self):
        basics = self.stock.get_basics('1101')
        self.assertNotEqual(basics, None)

    def test_get_eps(self):
        eps = self.stock.get_eps()
        self.assertNotEqual(eps, None)

    def test_get_balance_sheet(self):
        balance_sheet = self.stock.get_balance_sheet()
        self.assertNotEqual(balance_sheet, None)


if __name__ == '__main__':
    tests = ['test_get_eps']
    suite = unittest.TestSuite(map(TaiwanStockTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

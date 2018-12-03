import unittest
from app_taiwan_stock import AppTaiwanStock


class TestAppTaiwanStock(unittest.TestCase):
    stock = AppTaiwanStock()

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

    def test_get_table(self):
        self.stock.get_table('1101', 2)

    def test_get_excel(self):
        self.stock.get_excel()


if __name__ == '__main__':
    tests = ['test_get_excel']
    suite = unittest.TestSuite(map(TestAppTaiwanStock, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

import unittest
import taiwan_stock


class TestTaiwanStock(unittest.TestCase):
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

    def test_get_table(self):
        self.stock.get_table('http://mops.twse.com.tw/server-java/t164sb01', 2)


if __name__ == '__main__':
    tests = ['test_get_table']
    suite = unittest.TestSuite(map(TestTaiwanStock, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

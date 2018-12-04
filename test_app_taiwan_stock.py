import unittest
from app_taiwan_stock import AppTaiwanStock


class TestAppTaiwanStock(unittest.TestCase):
    stock = AppTaiwanStock()

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


if __name__ == '__main__':
    tests = ['test_get_basic_info_files']
    suite = unittest.TestSuite(map(TestAppTaiwanStock, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

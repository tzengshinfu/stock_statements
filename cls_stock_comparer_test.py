import unittest
from pathlib import Path
import os
import fnmatch


class ClsStockComparerTest(unittest.TestCase):

    # region 初始方法
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
    # endregion

    def test_get_stock(self):
        stock_ids = list()
        pathlist = Path('D:\\Excel').glob('**/*.xlsx')
        for path in pathlist:
            stock_id = str(path.name)[0:4]
            if stock_id not in stock_ids:
                stock_ids.append(stock_id)
        for file in os.listdir('D:\\Excel'):
            if fnmatch.fnmatch(file, stock_id + '*_現金流量表.xlsx'):
                print(file)


if __name__ == '__main__':
    tests = ['test_get_stock']
    suite = unittest.TestSuite(map(ClsStockComparerTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

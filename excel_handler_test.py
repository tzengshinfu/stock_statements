import unittest
import excel_handler


class ExcelHandlerTest(unittest.TestCase):
    handler = excel_handler.ExcelHandler()

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

    def test_save_workbook(self):
        excel_path = self.handler.save_workbook()
        self.assertNotEqual(excel_path, 'd:\\desktop\\book.xlsx')


if __name__ == '__main__':
    tests = ['test_save_workbook']
    suite = unittest.TestSuite(map(ExcelHandlerTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

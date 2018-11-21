import unittest
import excel_handler
import fnmatch
import os


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
        self.handler.save_workbook('d:\\desktop\\book.xlsx')
        file_existed = False

        for file in os.listdir('d:\\desktop'):
            if fnmatch.fnmatch(file, 'book.xlsx'):
                file_existed = True
        self.assertTrue(file_existed)
        self.handler.exit()

    def test_paste_array_to_sheet(self):
        self.handler.sheet.range('A1').value = [[1, 2], [3, 4], [5, 6]]
        self.handler.save_workbook('d:\\desktop\\book.xlsx')
        self.handler.exit()


if __name__ == '__main__':
    tests = ['test_paste_array_to_sheet']
    suite = unittest.TestSuite(map(ExcelHandlerTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

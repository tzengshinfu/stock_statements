import unittest
from cls_excel_handler import ClsExcelHandler
import fnmatch
import os


class ClsExcelHandlerTest(unittest.TestCase):
    handler = ClsExcelHandler()

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

    def test_save_book(self):
        self.handler.save_book('d:\\desktop\\book.xlsx')
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
    tests = ['test_save_book']
    suite = unittest.TestSuite(map(ClsExcelHandlerTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

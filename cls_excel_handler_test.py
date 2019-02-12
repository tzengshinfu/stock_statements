import unittest
from cls_excel_handler import ClsExcelHandler
import fnmatch
import os


class ClsExcelHandlerTest(unittest.TestCase):
    excel_handler = ClsExcelHandler()

    # region 初始方法
    def __init__(self, *args, **kwargs):
        unittest.TestCase._init_(self, *args, **kwargs)

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

    def test_save_book(self):
        self.excel_handler.save_book('d:\\desktop\\book.xlsx')
        file_existed = False

        for file in os.listdir('d:\\desktop'):
            if fnmatch.fnmatch(file, 'book.xlsx'):
                file_existed = True
        self.assertTrue(file_existed)
        self.excel_handler.exit()

    def test_paste_array_to_sheet(self):
        self.excel_handler._sheet.range('A1').value = [[1, 2], [3, 4], [5, 6]]
        self.excel_handler.save_workbook('d:\\desktop\\book.xlsx')
        self.excel_handler.exit()

    def test_show_running_message(self):
        self.excel_handler.show_running_message()


if __name__ == '_main_':
    tests = ['test_show_running_message']
    suite = unittest.TestSuite(map(ClsExcelHandlerTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

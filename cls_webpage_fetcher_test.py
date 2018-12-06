import unittest
from cls_webpage_fetcher import ClsWebpageFetcher


class ClsWebpageFetcherTest(unittest.TestCase):
    fetcher = ClsWebpageFetcher()

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

    def test_go_to(self):
        self.fetcher.go_to('https://www.google.com')

    def test_download_file(self):
        pdf_path = self.fetcher.download_file(
            'http://doc.twse.com.tw/pdf/201801_1101_AI1_20181108_084034.pdf')
        self.assertEqual(pdf_path,
                         'D:\\Temp\\201801_1101_AI1_20181108_084034.pdf')

    def test_find_elements(self):
        self.fetcher.request.go_to(
            'http://mops.twse.com.tw/mops/web/t05st03',
            'post',
            'firstin=1&co_id=' + '1101')
        trs = self.fetcher.request.find_elements('//table[@class="hasBorder"]//tr')
        for tr in trs:
            print(tr.value)
        pass


if __name__ == '__main__':
    tests = ['test_download_file']
    suite = unittest.TestSuite(map(ClsWebpageFetcherTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

import unittest
from cls_webpage_fetcher import ClsWebpageFetcher


class ClsWebpageFetcherTest(unittest.TestCase):
    webpage_fetcher = ClsWebpageFetcher()

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

    def test_go_to(self):
        self.webpage_fetcher.go_to('https://www.google.com')

    def test_download_file(self):
        pdf_path = self.webpage_fetcher.download_file('http://doc.twse.com.tw/pdf/201801_1101_AI1_20181108_084034.pdf')
        self.assertEqual(pdf_path, 'D:\\Temp\\201801_1101_AI1_20181108_084034.pdf')

    def test_find_elements(self):
        self.webpage_fetcher.go_to('http://mops.twse.com.tw/mops/web/t05st03', 'post', 'firstin=1&co_id=' + '1101')
        trs = self.webpage_fetcher.find_elements('//table[@class="hasBorder"]//tr')
        for tr in trs:
            print(tr.value)
        pass

    def test_to_list(self):
        self.webpage_fetcher.go_to('http://mops.twse.com.tw/mops/web/ajax_t05st09', 'post', data='encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=true&co_id={0}&year={1}'.format('1101', '2018'))
        table = self.webpage_fetcher.find_element('//table[@class="hasBorder"]')
        a = self.webpage_fetcher.to_list(table)
        print(a)


if __name__ == '__main__':
    tests = ['test_to_list']
    suite = unittest.TestSuite(map(ClsWebpageFetcherTest, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)

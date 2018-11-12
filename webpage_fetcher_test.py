import unittest
import webpage_fetcher


class WebpageFetcherTest(unittest.TestCase):
    fetcher = webpage_fetcher.WebpageFetcher()

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def test_download_file(self):
        pdf_path = self.fetcher.download_file(
            'http://doc.twse.com.tw/pdf/201801_1101_AI1_20181108_084034.pdf')
        self.assertEqual(pdf_path,
                         'D:\\Temp\\201801_1101_AI1_20181108_084034.pdf')

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main(exit=False)

import webpage_fetcher
from lxml import etree


if __name__ == '__main__':
    fetcher = webpage_fetcher.WebpageFetcher()
    # path = fetcher.download_file('http://www.twse.com.tw/downloads/zh/about/company/Annual/90/32.pdf')
    text = fetcher.get_pdf_text('D:\\Temp\\32.pdf')
    tree = etree.fromstring(text)
    fetcher.exit()
    print(text)

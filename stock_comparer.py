import webpage_fetcher
from lxml import etree
import pytesseract
from wand.image import Image as image_converter
import glob
from PIL import Image


if __name__ == '__main__':
    fetcher = webpage_fetcher.WebpageFetcher()
    # path = fetcher.download_file('http://www.twse.com.tw/downloads/zh/about/company/Annual/90/32.pdf')
    # xml = fetcher.get_xml_from_pdf('D:\\Temp\\32.pdf')
    # tree = etree.fromstring(xml)
    # fetcher.exit()
    # print(xml)
    file_list = fetcher.get_images_from_pdf('D:\\Temp\\a.pdf')
    print(file_list)
    # code = pytesseract.image_to_string(Image.open(file_list[1]), lang='chi_tra+eng')
    # print(code)
    # pdf = Image(filename='D:\\Temp\\32.pdf', resolution=300)
    # image = pdf.convert('jpg')
    # image.save(filename="D:\\Temp\\99.jpg")
    # print(jpg)

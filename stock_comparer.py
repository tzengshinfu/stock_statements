import webpage_fetcher


if __name__ == '__main__':
    # taiwan_stock = taiwan_stock.TaiwanStock()
    # stock_list = taiwan_stock.get_detail_data()
    # print(stock_list)
    fetcher = webpage_fetcher.WebpageFetcher()
    # fetcher.go_to('https://www.cnyes.com/twstock/financial4.aspx')
    fetcher.go_to('http://www.twse.com.tw/zh/stockSearch/stockSearch')
    # btnI = fetcher.find_element('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//a')
    # btnI = fetcher.find_element('//a[@class="submenu-title"]').get_attribute("href")
    list_table = fetcher.find_element('//table[@class="grid"]')
    links = list_table.find_elements_by_tag_name('a')
    stock_list = []
    for link in links:
        code = link.get_property('text')
        stock_list.append([code[0:4], code[4:]])
        print(code)

    fetcher.exit()

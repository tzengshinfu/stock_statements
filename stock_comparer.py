import webpage_fetcher


# taiwan_stock = taiwan_stock.TaiwanStock()
# stock_list = taiwan_stock.get_detail_data()
# print(stock_list)
fetcher = webpage_fetcher.WebpageFetcher()
fetcher.go_to('https://www.cnyes.com/twstock/financial4.aspx')
btnI = fetcher.find_element('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]//tr')
print(btnI)
fetcher.exit()

class PublicFunction():
    def get_browser_headers(self):
        """取得瀏覽器Request Header"""
        chrome_header = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':
            'gzip, deflate',
            'Accept-Language':
            'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control':
            'max-age=0',
            'Connection':
            'keep-alive',
            'DNT':
            '1',
            'Host':
            'www.twse.com.tw',
            'Upgrade-Insecure-Requests':
            '1',
            'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

        return chrome_header

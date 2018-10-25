class PublicFunction():
    def get_browser_headers(self, url):
        """取得瀏覽器Request Header"""
        headers = {
            'Accept':
            '*/*',
            'Accept-Encoding':
            'gzip, deflate, br',
            'Accept-Language':
            'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control':
            'no-cache',
            'Connection':
            'keep-alive',
            'Content-Length':
            '42746',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'DNT':
            '1',
            'Host':
            'www.cnyes.com',
            'Origin':
            'https://www.cnyes.com',
            'Referer':
            'https://www.cnyes.com/twstock/financial4.aspx',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'X-MicrosoftAjax':
            'Delta=true',
            'Upgrade-Insecure-Requests':
            '1'
        }
        if 'twse.com.tw' in url:
            headers = {
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
        if 'cnyes.com' in url:
            headers = {
                'Accept':
                '*/*',
                'Accept-Encoding':
                'gzip, deflate, br',
                'Accept-Language':
                'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control':
                'no-cache',
                'Connection':
                'keep-alive',
                'Content-Length':
                '42746',
                'Content-Type':
                'application/x-www-form-urlencoded',
                'DNT':
                '1',
                'Host':
                'www.cnyes.com',
                'Origin':
                'https://www.cnyes.com',
                'Referer':
                'https://www.cnyes.com/twstock/financial4.aspx',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'X-MicrosoftAjax':
                'Delta=true',
                'Upgrade-Insecure-Requests':
                '1'
            }

        return headers

import urllib.request
import urllib.parse
import urllib
import time
from urllib.error import HTTPError, URLError
import requests


def http_get(url, data={}, timeout=15, charset='gb2312', cookie=''):
    """
    发送http请求，返回响应内容
    """
    header_req = {
        'Cookie': cookie,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    }
    print('get:', url)
    if data != '':
        ret = requests.post(url, data=data,headers=header_req)
        return ret.text
    else:
        ret = requests.post(url, headers=header_req)
        return ret.text

def http_get_cookie(url, data={}, timeout=15, charset='gb2312', cookie=''):
    """
    发送http请求，返回响应内容
    """
    url = urllib.parse.quote(url, safe='/:?=&')
    data = urllib.parse.urlencode(data)
    if data != '':
        method = 'POST'
    else:
        method = 'GET'
    data = data.encode('ascii')
    header_req = {'Cookie': cookie}
    request = urllib.request.Request(url, data=data, method=method, headers=header_req)
    while True:
        print('get:', url)
        try:
            res = urllib.request.urlopen(request, timeout=timeout)
            header_cookie = res.getheader("Set-Cookie")
            return res.read().decode(charset, 'replace'), header_cookie
        except HTTPError as err:
            print('request error, error code:', err.code)
        except URLError as err:
            print('request error, reason:', err.reason)
        print('5秒后重新发起.')
        time.sleep(5)
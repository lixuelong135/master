import requests


DEFAULT_REQUEST_HEADERS = {

'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
#'Cookie':'__cdnuid=713e04c47f93070d828c97e375a957f1; PHPSESSID=0u71au7irrgkhih8h29c3e1ne6',
'Host':'m.biquyun.com',
'Referer':'https://m.biquyun.com/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }


url = 'http://m.biquyun.com/'
response = requests.post(url,headers=DEFAULT_REQUEST_HEADERS)

response = response.cookies
print(response)
cookie = requests.utils.dict_from_cookiejar(response)
print(cookie)
ck_jar = requests.utils.cookiejar_from_dict(cookie)
print(ck_jar)
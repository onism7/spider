import requests

url = 'http://www.renren.com/PLogin.do'
data = {
    "email": "970138074@qq.com", "password": "pythonspider"
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

session = requests.Session()
session.post(url,data=data,headers = headers)
res = session.get("http://www.renren.com/880151247/profile")
with open('renren.html','w',encoding='utf-8') as f:
    f.write(res.text)
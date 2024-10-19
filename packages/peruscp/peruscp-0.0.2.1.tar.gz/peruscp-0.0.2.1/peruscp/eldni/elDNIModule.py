import requests
from bs4 import BeautifulSoup

def requisitos():

    headers = {
        "Host": "eldni.com",
        "Accept-Language": "es-ES,es;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }

    t = requests.get('https://eldni.com/',headers=headers)

    cookies = 'XSRF-TOKEN='+str(t.cookies.get("XSRF-TOKEN"))+'; laravel_session='+str(t.cookies.get("laravel_session"))

    soup = BeautifulSoup(t.text,'html.parser')
    token = soup.find('input',{'name':'_token'})['value']

    return token,cookies

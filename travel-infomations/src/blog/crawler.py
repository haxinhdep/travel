import requests
from bs4 import BeautifulSoup


def url_link_spider(url_link):
    url = url_link
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    i = 1
    for h1 in soup.findAll('p'):
        mo_ta = h1.string
        if mo_ta is not None:
            print(mo_ta)
        i += 1


def trade_spider():
    url = 'http://tourism.danang.vn/khach-san'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    i = 1
    for div in soup.findAll('div', {'class': 'post-thumb preload image-loading zoom-img-in'}):
        title = str(i)+"-"+div.a.get('title')
        href = div.a.get('href')
        img = div.img.get('src')
        print(title)
        print(img)
        print(href)
        url_link_spider(href)
        i += 1

trade_spider()
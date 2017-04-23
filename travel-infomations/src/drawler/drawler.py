import requests
from bs4 import BeautifulSoup


def url_link_spider(url_link, title, img):
    url = url_link
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    i = 1
    for h4 in soup.findAll('h4', {'style': 'text-align: justify;'}):
        content = h4.string
        if content is not None:
            print(content)
        i += 1
    i = 1
    for p in soup.findAll('p', {'style': 'text-align: justify;'}):
        content = p.string
        if content is not None:
            print(content)
        i += 1
    i = 1
    for p in soup.findAll('p'):
        content = p.string
        if content is not None:
            print(content)
    i += 1
    for date in soup.find('div', {'class': 'date'}):
        date = date.string
        if date is not None:
            print(date)
        i += 1
    print(img)


def trade_spider():
    url = 'http://tourism.danang.vn/su-kien-noi-bat'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    # draw = Post()
    i = 1
    for div in soup.findAll('div', {'class': 'post-thumb preload image-loading zoom-img-in'}):
        title = div.img.get('alt')
        href = div.a.get('href')
        img = div.img.get('src')
        # date = soup.findAll('div', {'class': 'date'})
        # draw.title = title
        # draw.image = img
        # print(title)
        # print(img)
        # print(href)
        # print(date)
        url_link_spider(href, title, img)
        i += 1


trade_spider()

trade_spider()
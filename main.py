import requests
from bs4 import BeautifulSoup

URL =  "https://auto.ria.com/uk/newauto/marka-mazda/"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 YaBrowser/20.11.3.179 Yowser/2.5 Safari/537.36", "accent":"*/*"}
HOST = 'https://auto.ria.com'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='proposition_link')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='size16')
        if uah_price:
            uah_price = uah_price.get_text().replace(' • ', '')
        else:
            uah_price = 'Цену уточняйте'
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST + item.get('href'),
             'usd_price': item.find('span', class_='green').get_text(),
            'uah_price': uah_price,
             'city': item.find('span', class_='item region').get('title'),
        })
    return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
        print(cars)
    else:
        print('Error')


parse()
import pprint
import requests
from bs4 import BeautifulSoup


URL = "https://www.point2homes.com/CA/Apartments-For-Rent/BC.html"
HOST = "https://www.point2homes.com"
HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}


def get_request(url, params=''):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(response):
    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.find_all("div", class_="item-cnt")

    for card in cards:
        title = card.find('div', class_="address-container").text.strip()

        try:
            area = card.find('li', class_="ic-sqft").text.strip()[:-4]
        except AttributeError:
            area = None

        try:
            bath = card.find('li', class_="ic-baths").text.strip()[:-2]
        except AttributeError:
            bath = None

        try:
            beds = card.find('li', class_="ic-beds").text.strip()
        except AttributeError:
            beds = None
        else:
            beds = beds.replace('Bds', '')
            beds = beds.replace('Bd', '')

        dct = {
            "title": title[:title.index("\r")].replace('  ', ''),
            'address': card.find('div', class_="address-container").get("data-address"),
            'price': card.find("div", class_="price has-rental-term").get('data-price'),
            'link': HOST + card.find("div", class_="inner-right").find("a").get("href"),
            'img_link': card.find("div", class_="lslide active").find('img').get('src'),
            'apartments_type': card.find("li", class_="property-type ic-proptype").text.strip(),
            "area": area,
            "bath": bath,
            "beds": beds
        }
        yield dct


if __name__ == '__main__':
    response = get_request(URL)
    for i in get_content(response):
        pprint.pprint(i)

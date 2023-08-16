import requests
from bs4 import BeautifulSoup


URL = "https://www.point2homes.com/CA/Apartments-For-Rent/BC.html"
HOST = "https://www.point2homes.com/"
HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}


def get_request(url, params=''):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(response):
    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.find_all("div", class_="item-cnt")

    for card in cards:
        title = card.find('div', class_="address-container").text.strip()

        dct = {
            "title": title[:title.index("\r")].replace('  ', ''),
            'address': None
        }
        yield dct


if __name__ == '__main__':
    response = get_request(URL)
    for i in get_content(response):
        print(i)

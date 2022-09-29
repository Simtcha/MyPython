from bs4 import BeautifulSoup
from numpy import trim_zeros
import requests
from csv import writer

url= "https://www.pararius.com/apartments/amsterdam?ac=1"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('section', class_="listing-search-item")

with open('housing.csv', 'w', encoding='utf-8', newline='') as f:
    thewriter = writer(f)
    header = ['Title', 'Location', 'Price', 'Area']
    thewriter.writerow(header)

    for list in lists:
        title = list.find('a', class_="listing-search-item__link--title").text.replace('\n', '')
        title = title.strip()
        location = list.find('div', class_="listing-search-item__sub-title").text.replace('\n', '')
        location = location.strip()
        price = list.find('div', class_="listing-search-item__price").text.replace('\n', '')
        price = price.strip()
        area = list.find('li', class_="illustrated-features__item--surface-area").text.replace('\n', '')
        area = area.strip()

        info = [title, location, price, area]
        thewriter.writerow(info)
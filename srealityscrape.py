from typing import ParamSpecKwargs
from bs4 import BeautifulSoup
import requests
from csv import writer

url = 'https://www.sreality.cz/hledani/prodej/byty/praha?velikost=3%2Bkk'
page = requests.get(url)

soup = BeautifulSoup(page.content,'html.parser')
#lists = soup.find_all('span', class_= "basic")
lists = soup.find_all('div', class_= "ng-if")

with open('sreality.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Title', 'Location','Price', 'Area']
    thewriter.writerow(header)

    for list in lists:
        location = list.find('span', class_="locality ng-binding").text.replace('\n','')
        price = list.find('span', class_="price ng-scope").text.replace('\n','')
        price2 = list.find('spn', class_="norm-price ng-binding").text.replace('\n','')
        some_labels = list.find('span', class_="labels ng-scope").text.replace('\n','')
        name = list.find('span',class_= "name ng-binding").text.replace('\n','')
        info = [location, price, price2, some_labels, name]
        thewriter.writerow(info)

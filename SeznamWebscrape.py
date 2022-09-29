from cgi import print_directory
from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.seznam.cz/")
soup = BeautifulSoup(response.text,"html.parser")
articles = soup.find_all(class_="article__title")
#print(articles)
#print(len(articles))
looking_for = input('O jakem tematu hledas clanek?:')
with open("seznam.txt", "w") as file:
    for one_article in articles:
        one_article_text = one_article.getText()
        one_article_link = one_article.get("href")
        #print(one_article_text)
        #print(one_article_link)
        if looking_for in one_article_text:
            #print(one_article_text)
            #print(one_article_link)
            #file.write("\n")
            file.write(one_article_text)
            #file.write("\n")
            file.write(one_article_link)
        



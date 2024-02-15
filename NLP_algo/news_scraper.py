#import libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import datetime
from article import Article


#--------------------------------------------------------------------
#finviz

url = "https://finviz.com/news.ashx"

#create page object and print connection response
session = HTMLSession()
response = session.get(url)

articles = response.html.xpath("//tr[@class='styled-row is-hoverable is-bordered is-rounded is-border-top is-hover-borders has-color-text news_table-row']")

soup = BeautifulSoup(articles[0].html, "html.parser")
print(soup.prettify())
print("\n")
print(soup.find)
"""
article_list = []

for article in articles:
    soup = BeautifulSoup(article.html)
    
    #a = Article(soup.a.text, article.absolute_links)
    article_list.append(soup.find('a', class_="tab-link").text)

for article in article_list:
    print(article)
    """
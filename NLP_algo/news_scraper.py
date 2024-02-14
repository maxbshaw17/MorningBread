#import libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#----------------------
#finviz
#----------------------

url = "https://finviz.com/news.ashx"

#create page object and render javascript to readable html
session = HTMLSession()
response = session.get(url)
print(response)

articles = response.html.xpath("//a[@class='tab-link']")

article_text = []

for article in articles:
    article_text.append(article.text)

print(article_text)
#import libraries
import requests
from bs4 import BeautifulSoup

#investing.com

#url of source
url = "https://www.investing.com/news/latest-news"

#create beatifulsoup object using the url
page = BeautifulSoup(requests.get(url).content, "html.parser")

print(page)

articles = page.find_all("article", class_="js-article-item articleItem     ")
for article in articles:
    print(article)
#imports
from news_scraper import *


articles = scrape_yahoo()
for article in articles:
    print(article)
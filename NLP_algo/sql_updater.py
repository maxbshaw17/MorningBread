#imports
from news_scraper import scrape_finviz


articles = scrape_finviz()
for article in articles:
    print(article)
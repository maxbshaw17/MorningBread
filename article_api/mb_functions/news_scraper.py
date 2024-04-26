# import libraries
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from .article import Article
import time as python_time
import feedparser
import pandas as pd
# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

# methods for cleaning data


def text_to_datetime(date_string):
    return_date = datetime.date(1970, 1, 1)

    # xx:xxXM format
    if "M" in date_string and date_string[0].isnumeric():
        today_string = str(date.today())
        return_date = datetime.datetime.strptime(
            f"{today_string} {date_string}", "%Y-%m-%d %I:%M%p")
    # Mon-xx format
    elif "-" in date_string:
        return_date = datetime.datetime.strptime(
            f"{str(date.today().year)}-{date_string} {str(time(12, 0, 0))}", "%Y-%b-%d %H:%M:%S")
    # x minute(s) ago format
    elif "minute" in date_string:
        nums = int(''.join([char for char in date_string if char.isdigit()]))

        return_date = datetime.datetime.now() - timedelta(minutes=nums)
    # x hour(s) ago format
    elif "hour" in date_string:
        nums = int(''.join([char for char in date_string if char.isdigit()]))

        return_date = datetime.datetime.now() - timedelta(hours=nums)
    # day, 00 Mon Year 00:00:00 GMT
    elif "GMT" in date_string:
        return_date = datetime.datetime.strptime(
            date_string, "%a, %d %b %Y %H:%M:%S GMT") - timedelta(hours=5)
    return return_date

# individual methods for each site


def scrape_finviz():
    start_time = python_time.time()
    # Initialize an empty list to store scraped articles
    article_list = []

    # the url to be connected to
    url = "https://finviz.com/news.ashx"

    # create page object and print connection response
    session = HTMLSession()
    response = session.get(url)

    # create list of html elemnts housing article data, filters out advertisements
    soup = BeautifulSoup(response.text, 'lxml')
    article_table = soup.find(
        'table', {'class': "styled-table-new is-rounded table-fixed"})
    articles = article_table.find_all(
        'tr', {'class': 'styled-row is-hoverable is-bordered is-rounded is-border-top is-hover-borders has-color-text news_table-row', 'onclick': True})

    # loop through article objects and add to master list
    for article in articles:
        # retrieve headline and link from soup object
        text = article.find("td", class_="news_link-cell").get_text()
        link = article.find("a", class_="tab-link").get('href')

        # retrieve date/time - accounts for possibility time and date
        datetime_date = text_to_datetime(article.find(
            "td", class_="text-right news_date-cell color-text is-muted").get_text())

        # creates article object and adds to master list
        article_list.append(Article(text, link, datetime_date, "finviz"))

    print(f"scraped {len(article_list)} articles from finviz in {round(python_time.time() - start_time, 3)} seconds")
    
    return article_list


def scrape_yahoo():
    start_time = python_time.time()
    article_list = []
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('log-level=3')
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=op)
    driver.get('https://finance.yahoo.com/topic/latest-news')

    python_time.sleep(2)

    SCROLL_PAUSE_TIME = 4
    old_height = int(driver.execute_script(
        "return document.documentElement.scrollHeight"))

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")
        current_height = int(driver.execute_script(
            "return document.documentElement.scrollHeight"))
        # Wait to load page
        python_time.sleep(SCROLL_PAUSE_TIME)

        if old_height == current_height:
            break
        else:
            old_height = current_height

    python_time.sleep(2)

    elements_div = BeautifulSoup((driver.find_element(
        By.XPATH, '//div[@id="Fin-Stream"]').get_attribute('innerHTML')), "html.parser")
    elements = list(filter(None, elements_div.find_all('li')))

    for e in elements:
        headline = e.find('a').get_text()
        link = f"https://finance.yahoo.com/{e.find('a').get('href')}"
        publish_time = text_to_datetime(e.find_all('span')[1].get_text())
        source = e.find_all('span')[0].get_text()

        article_list.append(Article(headline, link, publish_time, source))
        
    print(f"scraped {len(article_list)} articles from yahoo in {round(python_time.time() - start_time, 3)} seconds")

    return article_list


def scrape_marketwatch_rss():
    start_time = python_time.time()
    # links to rss feeds
    links = [
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",
        "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
        "https://feeds.content.dowjones.io/public/rss/mw_bulletins",
        "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"
    ]

    article_list = []

    # iterate through links, have the same format
    for link in links:

        feed = feedparser.parse(link)

        for entry in feed.entries:
            article_headline = entry.title
            article_link = entry.link

            article_date = text_to_datetime(entry.published)

            article_list.append(
                Article(article_headline, article_link, article_date, "marketwatch rss"))

    print(f"scraped {len(article_list)} articles from marketwatch in {round(python_time.time() - start_time, 3)} seconds")

    return (article_list)

# method to run all individual methods


def scrape_all():
    article_list = []
    for article in scrape_finviz():
        article_list.append(article)
    for article in scrape_yahoo():
        article_list.append(article)
    for article in scrape_marketwatch_rss():
        article_list.append(article)

    # converts list of article objects to dataframe
    return pd.DataFrame(
        list(map(lambda article: article.to_list(), article_list)),
        columns = ['headline', 'link', 'date', 'source'])
        


if __name__ == "__main__":
    x = scrape_all()
    print(x)
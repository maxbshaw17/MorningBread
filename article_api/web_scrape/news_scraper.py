# import libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from article import Article

import time

# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}


# individual methods for each site
def scrape_finviz():
    # Initialize an empty list to store scraped articles
    article_list = []
    
    #the url to be connected to
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
        date_text = article.find(
            "td", class_="text-right news_date-cell color-text is-muted").get_text()

        # empty datetime object to return later
        datetime_date = datetime.date(1970, 1, 1)

        # checks if string is date or time and updates datetime object accordingly
        if (date_text[0].isnumeric()):
            # string conating todays date to parse
            today_string = str(date.today())

            # updates datetime object using strings from earlier
            datetime_date = datetime.datetime.strptime(
                f"{today_string} {date_text}", "%Y-%m-%d %I:%M%p")
            
        else: # case where date_text is a month and day
            datetime_date = datetime.datetime.strptime(
                f"{str(date.today().year)}-{date_text} {str(time(12, 0, 0))}", "%Y-%b-%d %H:%M:%S")

        # creates article object and adds to master list
        article_list.append(Article(text, link, datetime_date, "finviz"))
    return article_list

def scrape_yahoo():
    article_list = []
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('log-level=3')
    driver = webdriver.Chrome(options=op)
    driver.get('https://finance.yahoo.com/topic/latest-news')
    
    time.sleep(10)
    
    SCROLL_PAUSE_TIME = 3

    new_pages = 10

    while new_pages > 0:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        
        new_pages-=1

    elements_div = BeautifulSoup((driver.find_element(By.XPATH, '//div[@id="Fin-Stream"]').get_attribute('innerHTML')), "html.parser")
    elements = list(filter(None, elements_div.find_all('li')))
    
    
    for e in elements:
        print(e.find('a').get_text())
    
    return article_list

def scrape_marketwatch_rss():
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

        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'lxml')

        articles = soup.find_all('item')

        for article in articles:
            article_headline = article.find('title').get_text()
            article_link = article.find('link').get_text()

            try:
                date_text = article.find('pubDate').get_text()
            except:
                date_text = article.find('pubdate').get_text()
            article_date = datetime.datetime.strptime(
                date_text, "%a, %d %b %Y %H:%M:%S GMT") + timedelta(hours=7)

            article_list.append(
                Article(article_headline, article_link, article_date, "marketwatch rss"))

    return (article_list)

# method to run all individual methods
def scrape_all(yahoo_scrolldown=1000):
    article_list = []
    for article in scrape_finviz():
        article_list.append(article)
    for article in scrape_yahoo(yahoo_scrolldown):
        article_list.append(article)
    for article in scrape_marketwatch_rss():
        article_list.append(article)

    return article_list

scrape_yahoo()
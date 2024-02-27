#import libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from article import Article

headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
           }


#individual methods for each site
def scrape_finviz():
    article_list = []
    url = "https://finviz.com/news.ashx"

    #create page object and print connection response
    session = HTMLSession()
    response = session.get(url)

    #create list of html elemnts housing article data, filters out advertisements
    soup = BeautifulSoup(response.text, 'lxml')
    article_table = soup.find('table', {'class' : "styled-table-new is-rounded table-fixed"})
    articles = article_table.find_all('tr', {'class' : 'styled-row is-hoverable is-bordered is-rounded is-border-top is-hover-borders has-color-text news_table-row', 'onclick' : True})
    #articles = response.html.xpath("//tr[@class='styled-row is-hoverable is-bordered is-rounded is-border-top is-hover-borders has-color-text news_table-row'][@onclick]")

    #loop through article objects and add to master list
    for article in articles:
        #soup = BeautifulSoup(article.html, "html.parser")
        
        #retrieve headline and link from soup object
        text = article.find("td", class_= "news_link-cell").get_text()
        link = article.find("a", class_= "tab-link").get('href')
        
        #retrieve date/time - accounts for time and date display
        date_text = article.find("td", class_= "text-right news_date-cell color-text is-muted").get_text()
        
        #empty datetime object to return later
        datetime_date = datetime.date(1970, 1, 1)
        
        #checks if string is date or time and updates datetime object accordingly
        if(date_text[0].isnumeric()):
            #checks if time is AM or PM and converts to 24 hour scale
            if(date_text[-2:] == 'PM'):
                date_text = f"{(int(date_text[:2])) + 12}:{date_text[3:5]}"
            else:
                date_text = f"{date_text[:5]}"
            
            #string conating todays date to parse
            today_string = str(date.today())
            
            #updates datetime object using strings from earlier
            datetime_date = datetime.datetime.strptime(f"{today_string} {date_text}", "%Y-%m-%d %H:%M")
        #case where date_text is a month and day
        else:
            datetime_date = datetime.datetime.strptime(f"{str(date.today().year)}-{date_text} {str(time(12, 0, 0))}", "%Y-%b-%d %H:%M:%S")

        #creates article object and adds to master list
        article_list.append(Article(text, link, datetime_date, "finviz"))
    return article_list

def scrape_yahoo(scrolldown = 2000):
    article_list = []
    url = "https://finance.yahoo.com/topic/latest-news"

    #create page object and print connection response
    session = HTMLSession()
    response = session.get(url, headers = headers)

    #render javascript and scroll to load more articles
    response.html.render(scrolldown)

    #create soup object and list of html elements with data we want
    soup = BeautifulSoup(response.html.html, 'html5lib')
    articles = soup.find_all('div', {'class' : 'Cf', 'data-test-locator' : False})

    #loop through articles to get data and append article object
    for article in articles:
        try:
            #headline and link
            text = article.find('a').get_text()
            #link may be definite or relative
            link = article.find('a').get('href')
            if link[0] == '/':
                link = "https://finance.yahoo.com" + "link"
            
            #date/time - given in "x minutes/hours ago" format
            datetime_date = datetime.date(1970, 1, 1)
            
            time_text = article.find_all('span')[1].get_text()
            time_text = time_text[:(len(time_text)-4)]
            
            minutes_or_hours = ''.join(filter(str.isdigit, time_text))
            
            if "hour" in time_text:
                datetime_date = datetime.datetime.now() - datetime.timedelta(hours = int(minutes_or_hours))
            elif "minute" in time_text:
                datetime_date = datetime.datetime.now() - datetime.timedelta(minutes = int(minutes_or_hours))
            
            article_list.append(Article(text, link, datetime_date, "yahoo finance"))
        except:
            pass

    return article_list

def scrape_marketwatch_rss():
    #links to rss feeds
    links = [
        "https://feeds.content.dowjones.io/public/rss/mw_topstories",
        "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
        "https://feeds.content.dowjones.io/public/rss/mw_bulletins",
        "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"
    ]
    
    article_list = []
    
    #iterate through links, have the same format
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
            article_date = datetime.datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S GMT") + timedelta(hours = 7)
            
            article_list.append(Article(article_headline, article_link, article_date, "marketwatch rss"))
            
    return(article_list)

#method to run all individual methods
def scrape_all(yahoo_scrolldown = 2000):
    article_list = []
    for article in scrape_finviz():
        article_list.append(article)
    for article in scrape_yahoo(yahoo_scrolldown):
        article_list.append(article)
    for article in scrape_marketwatch_rss():
        article_list.append(article)
    
    return article_list
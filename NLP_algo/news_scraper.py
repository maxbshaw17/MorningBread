#import libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import time
from article import Article


article_list = []

#--------------------------------------------------------------------
#finviz

url = "https://finviz.com/news.ashx"

#create page object and print connection response
session = HTMLSession()
response = session.get(url)

#create list of html elemnts housing article data, filters out advertisements
articles = response.html.xpath("//tr[@class='styled-row is-hoverable is-bordered is-rounded is-border-top is-hover-borders has-color-text news_table-row'][@onclick]")

#loop through article objects and add to master list
for article in articles:
    soup = BeautifulSoup(article.html, "html.parser")
    
    #retrieve headline and link from soup object
    text = soup.find("td", class_= "news_link-cell").get_text()
    link = soup.find("a", class_= "tab-link").get('href')
    
    #retrieve date/time - accounts for time and date display
    date_text = soup.find("td", class_= "text-right news_date-cell color-text is-muted").get_text()
    
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
    article_list.append(Article(text, link, datetime_date))
    
for article in article_list:
    print(article)
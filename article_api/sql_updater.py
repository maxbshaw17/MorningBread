#imports
from web_scrape.news_scraper import *
import mysql.connector

#create database connection object
articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

mycursor = articles_db.cursor()

insert_sql = "INSERT INTO articles (headline, link, date, source) VALUES (%s, %s, %s, %s)"

articles = scrape_all()
values = []

for article in articles:
    values.append((article.headline, article.link, article.date, article.source))

try:
    mycursor.executemany(insert_sql, values)
    articles_db.commit()
except:
    articles_db.rollback()
finally:
    print(mycursor.rowcount, " rows inserted")
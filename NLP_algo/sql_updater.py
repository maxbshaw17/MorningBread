#imports
from news_scraper import *
import mysql.connector

articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

mycursor = articles_db.cursor()

insert_sql = "INSERT INTO articles (headline, link, date, source) VALUES)"
# imports
from db_update.db_connection import *
from nlp_algo.nlp_functions import *
from web_scrape.news_scraper import *

#create database connection object
connection = DB_Connection(
    host="mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user="avnadmin",
    password="AVNS_-1y1cgAxePfkqdPTpji",
    port=25747,
    database="morningbread"    
)

#upload new articles and remove old ones
articles = scrape_all()

connection.insert_articles_db(articles)

connection.delete_old_db(days=1.5)

#remove duplicate articles
connection.remove_dupes_db("articles", "headline")

#pull headlines and vectorize
headlines = connection.get_all_headlines()
array, sents = text_vectorizer(headlines)

#group using DBSCAN
fit_df = fit_dbscan_text(array, sents, ep=2.5, min_s=2)

#clear the grouped articles table
connection.delete_all("articles_grouped")

#insert generated groupings
connection.insert_groupings_db(fit_df)


print(fit_df.sort_values(by='group', ascending=False).head(80).to_string())

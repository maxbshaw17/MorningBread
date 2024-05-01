# imports
from mb_functions.db_connection import *
from mb_functions.news_scraper import *
from mb_functions.nlp_functions import *
import os
from dotenv import load_dotenv
import time as python_time

start_time = python_time.time()

# load the .env file
load_dotenv()

# access secret keys
AIVEN_API_KEY = os.getenv('AIVEN_API_KEY')
CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')
EPSILON = os.getenv('EPSILON')
MIN_S = os.getenv('MIN_S')

# create database connection object
connection = DB_Connection(
    host="mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user="avnadmin",
    password=AIVEN_API_KEY,
    port=25747,
    database="morningbread"
)

# upload new articles and remove old ones and duplicates
articles_df = scrape_all()

connection.insert_into_table(table = "articles", dataframe = articles_df)

connection.delete_from_table(table = "articles", days=1.5)
connection.delete_dupes_from_table(table = "articles", columns = ['headline', 'source'])

# pull headlines and vectorize
headlines = connection.read_table(table = "articles", column_relationships = {'headline' : 'headline'})
cleaned_headlines = clean_sent_list(headlines)
bag_of_words = text_vectorizer(cleaned_headlines)

#---uncomment to display knn plot---
#knn_plot(bag_of_words)

# group using DBSCAN
fit_df = fit_dbscan_text(bag_of_words, headlines, ep=float(EPSILON), min_s=int(MIN_S))

# clear the grouped articles table and joined table
connection.delete_from_table(table = "articles_grouped", clear = True)
connection.delete_from_table(table = "headline_groups", clear = True)

# insert generated groupings
connection.insert_into_table(table = "headline_groups", dataframe = fit_df, column_relationships = {"group": "group_id", "sent":"headline"})

# join groupings table with articles in new grouped articles table
connection.join_groups()

# summarize with chatgpt
headline_groups = connection.read_table(table = "headline_groups")

summarized_sents = summarize_group_df(headline_groups, CHATGPT_API_KEY)

# clear and insert new summaries into table
connection.delete_from_table(table = "summarized_articles", clear = True)
connection.insert_into_table(table = "summarized_articles", dataframe = summarized_sents)

print(f"finished running in {round(python_time.time() - start_time, 3)} seconds")
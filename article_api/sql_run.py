# imports
from mb_functions.db_connection import *
from mb_functions.news_scraper import *
from mb_functions.nlp_functions import *

# create database connection object
connection = DB_Connection(
    host="mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user="avnadmin",
    password="AVNS_-1y1cgAxePfkqdPTpji",
    port=25747,
    database="morningbread"
)

# upload new articles and remove old ones
articles_df = scrape_all()

connection.insert_into_table(table = "articles", dataframe = articles_df)

connection.delete_old_db(days=1.5)

# remove duplicate articles
connection.remove_dupes_db("articles", "headline")

# pull headlines and vectorize
headlines = connection.get_all_headlines()
array, sents = text_vectorizer(headlines)

# group using DBSCAN
fit_df = fit_dbscan_text(array, sents, ep=2.75, min_s=2)

# clear the grouped articles table and joined table
connection.delete_all("articles_grouped")
connection.delete_all("headline_groups")

# insert generated groupings
connection.insert_into_table(table = "headline_groups", dataframe = fit_df, column_relationships = {"group": "group_id", "sent":"headline"})

# join groupings table with information table
connection.join_groups()

# summarize with chatgpt
df = connection.get_groups()

grouped_df = df.groupby(by='group_id')
column_names = list(grouped_df.groups)
sent_list = []

for group in column_names:
    if group >= 0:
        sents = []

        for headline in grouped_df.get_group(group)['headline']:
            sents.append(headline)
        sent_list.append((group, sents))

summarized_sents = []

for group_sents in sent_list:
    sents = group_sents[1]

    summary = prompt_chat_gpt(f"{sents}").content

    summarized_sents.append((group_sents[0], summary))

# insert summaries into table
connection.delete_all("summarized_articles")
connection.insert_summaries_db(summarized_sents)

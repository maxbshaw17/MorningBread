# imports
from mb_functions.db_connection import *
from mb_functions.news_scraper import *
from mb_functions.nlp_functions import *
import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()

# access secret keys
AIVEN_API_KEY = os.getenv('AIVEN_API_KEY')
CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')

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

# group using DBSCAN
fit_df = fit_dbscan_text(bag_of_words, headlines, ep=2.75, min_s=2)

# clear the grouped articles table and joined table
connection.delete_from_table(table = "articles_grouped", clear = True)
connection.delete_from_table(table = "headline_groups", clear = True)

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
connection.delete_from_table(table = "summarized_articles", clear = True)
connection.insert_summaries_db(summarized_sents)

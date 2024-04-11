import mysql.connector
from sql_updater import *
from nlp_algo.nlp_functions import *
from db_update.db_connector import *


articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

mycursor = articles_db.cursor()



headlines = get_all_headlines()
array, sents = text_vectorizer(headlines)

fit_df = fit_dbscan_text(array, sents, ep = 2.5, min_s=2)

print(fit_df.sort_values(by='group', ascending=False).head(80).to_string())
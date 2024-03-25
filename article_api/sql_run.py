from sql_updater import *
from db_update.db_connector import *
from nlp_algo.nlp_functions import *

#insert_articles_db()

#delete_old_db(days=1)

#remove_dupes_db("articles", "headline")

headlines = get_all_headlines()
array, sents = text_vectorizer(headlines)

fit_df = fit_dbscan_text(array, sents, ep = 2.5, min_s=2)

delete_all("articles_grouped")

print(insert_groupings_db(fit_df))


#print(fit_df.sort_values(by='group', ascending=False).head(80).to_string())
from db_update.db_connector import *
from nlp_algo.nlp_functions import *

headlines = get_all_headlines()

array, sents = text_vectorizer(headlines)


#print(knn_plot(array))


fit_df = fit_dbscan_text(array, sents, ep = 2.5, min_s=2)

print(fit_df.sort_values(by='group', ascending=False).head(50))
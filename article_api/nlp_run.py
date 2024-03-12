from db_update.db_connector import *
from nlp_algo.nlp_functions import *

headlines = get_all_headlines()

for x in clean_text_list(headlines):
    print(x)
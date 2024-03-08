from db_update.db_connector import *
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

headlines_tuple = get_all_headlines()

headlines = []

for headline in headlines_tuple:
    headlines.append(headline[0])
    
"""
for x in headlines:
    print(x)
    
print(len(headlines))
"""

vectorizer = CountVectorizer()
bag_of_words = vectorizer.fit_transform(headlines)

print(bag_of_words)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
import re
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

default_stemmer = PorterStemmer()
default_stopwords = stopwords.words('english') # or any other list of your choice

# check for repeats - need to fix on sql side
def remove_repeats(headlines):
    text_no_repeats = []
    for sent in headlines:
        if sent not in text_no_repeats:
            text_no_repeats.append(sent)
    return (text_no_repeats)

def clean_text(text, ):
    
    punc = []
    for i in string.punctuation:
        punc.append(i)
    punc.extend(['’', '‘'])

    def tokenize_text(text):
        return [w for s in sent_tokenize(text) for w in word_tokenize(s)]

    def remove_special_characters(text, characters=punc):
        letters = list(map(lambda x: x, text))
        return_letters = []
        for letter in letters:
            if letter not in characters:
                return_letters.append(letter)
        return ''.join(return_letters)

    def stem_text(text, stemmer=default_stemmer):
        tokens = tokenize_text(text)
        return ' '.join([stemmer.stem(t) for t in tokens])

    def remove_stopwords(text, stop_words=default_stopwords):
        tokens = [w for w in tokenize_text(text) if w not in stop_words]
        return ' '.join(tokens)

    text = text.strip(' ') # strip whitespaces
    text = text.lower() # lowercase
    text = stem_text(text) # stemming
    text = remove_special_characters(text) # remove punctuation and symbols
    text = remove_stopwords(text) # remove stopwords
    text.strip(' ') # strip whitespaces again?

    return text

def clean_text_list(text_list):
    text_list = remove_repeats(text_list)
    return list(map(lambda text: clean_text(text), text_list))


cv = CountVectorizer()
x = cv.fit_transform(text_cleaned)
bag_of_words = x.toarray()

def knn_plot(text_array):
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(text_array)
    distances, indices = nbrs.kneighbors(text_array)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]

    plt.figure(figsize=(7,4))
    plt.plot(distances)
    plt.title('K-Distance - Check where it bends',fontsize=16)
    plt.xlabel('Data Points - sorted by Distance',fontsize=12)
    plt.ylabel('Epsilon',fontsize=12)
    plt.show()


dbscan_opt=DBSCAN(eps=2.5,min_samples=2)
dbscan_opt.fit(x)
df_data = {"group": dbscan_opt.labels_, "sentance" : headlines}
df = pd.DataFrame(data=df_data)

print(df['DBSCAN_opt_labels'].value_counts())

print(df.sort_values(by='DBSCAN_opt_labels', ascending=False).head(50))

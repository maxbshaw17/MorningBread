from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from openai import OpenAI

default_stemmer = PorterStemmer()
# or any other list of your choice
default_stopwords = stopwords.words('english')

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

    text = text.strip(' ')  # strip whitespaces
    text = text.lower()  # lowercase
    text = stem_text(text)  # stemming
    text = remove_special_characters(text)  # remove punctuation and symbols
    text = remove_stopwords(text)  # remove stopwords
    text.strip(' ')  # strip whitespaces again?

    return text


def clean_text_list(text_list):
    return list(map(lambda text: clean_text(text), text_list))


def text_vectorizer(text_list: list) -> pd.DataFrame:
    text_cleaned = clean_text_list(text_list)

    cv = CountVectorizer()
    array = cv.fit_transform(text_cleaned)
    return pd.DataFrame(array.toarray())

def knn_plot(text_array):
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(text_array)
    distances, indices = nbrs.kneighbors(text_array)
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]

    plt.figure(figsize=(7, 4))
    plt.plot(distances)
    plt.title('K-Distance - Check where it bends', fontsize=16)
    plt.xlabel('Data Points - sorted by Distance', fontsize=12)
    plt.ylabel('Epsilon', fontsize=12)
    plt.show()


def fit_dbscan_text(text_array, text, ep=1, min_s=2):
    dbscan_opt = DBSCAN(eps=ep, min_samples=min_s)
    dbscan_opt.fit(text_array)
    df_data = {"group": dbscan_opt.labels_, "sent": text}
    df = pd.DataFrame(data=df_data)

    return df


def prompt_chat_gpt(prompt_message):
    client = OpenAI(api_key="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")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a text summarizer. You are given multiple sentences relating to the same topic, and will return a sentence of similiar length that is a concise summary of the sentences you were given. You return this sentence as your only output, with no additional text"},
            {"role": "user", "content": prompt_message}
        ]
    )

    return completion.choices[0].message

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import string
import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from openai import OpenAI


def clean_sentence(sent: str):
    def preprocess_text(text):
        # convert text to lowecase
        text = text.lower()

        # remove special chars and digits using regex
        text = re.sub(r'\d+', '', text)  # remove digits
        text = re.sub(r'[^\w\s]', '', text)  # remove all special characters

        # tokenize text
        tokens = nltk.word_tokenize(text)

        return tokens

    def remove_stopwords(tokens):
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        return filtered_tokens

    def get_wordnet_pos(treebank_tag):
        # converts treebank tagging convention to wordnet tagging convention
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    def perfrom_lemmatization(tokens):
        lemmatizer = nltk.stem.WordNetLemmatizer()

        treebank_pos_tags = pos_tag(tokens)
        wordnet_pos_tags = [(tag_set[0], get_wordnet_pos(tag_set[1]))
                            for tag_set in treebank_pos_tags]
        lemmatized_tokens = [lemmatizer.lemmatize(tag_set[0], tag_set[1]) if tag_set[1] != '' else lemmatizer.lemmatize(tag_set[0]) for tag_set in wordnet_pos_tags]

        return lemmatized_tokens

    tokens = preprocess_text(sent)
    filtered_tokens = remove_stopwords(tokens)
    lemmmatized_tokens = perfrom_lemmatization(filtered_tokens)
    clean_sent = ' '.join(lemmmatized_tokens)

    return clean_sent


def clean_sent_list(text_list: pd.DataFrame) -> pd.DataFrame:
    sent_list = text_list['headline'].tolist()
    cleaned_sents = [clean_sentence(sent) for sent in sent_list]

    return pd.DataFrame({'cleaned_headline': cleaned_sents})


def text_vectorizer(text_list: pd.DataFrame) -> pd.DataFrame:
    cv = CountVectorizer()
    array = cv.fit_transform(text_list['cleaned_headline'].tolist())

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
    client = OpenAI(api_key="")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a text summarizer. You are given multiple sentences relating to the same topic, and will return a sentence of similiar length that is a concise summary of the sentences you were given. You return this sentence as your only output, with no additional text"},
            {"role": "user", "content": prompt_message}
        ]
    )

    return completion.choices[0].message

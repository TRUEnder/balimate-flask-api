from handler.query import query, queryWithColumnNames
from handler.idhandler import decode
import json
import pandas as pd
from handler.loadDataset import loadDestinations
from recommend import recommend_places
from search import recommend_by_content_based_filtering
from urllib import request
from predict import predict
from handler.preprocessing import preprocessingWithStem
from sklearn.feature_extraction.text import TfidfVectorizer

tourism = pd.read_csv('destination.csv', encoding='latin-1')

#  Data preprocessing

data_tourism = tourism.copy()
data_tourism.description = data_tourism.description.apply(
    preprocessingWithStem)

# TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data_tourism['description'])

tfidf_dataframe = pd.DataFrame(tfidf_matrix[0])

from handler.query import query, queryWithColumnNames
from handler.idhandler import decode
import json
import math
import numpy as np
import pandas as pd
from handler.loadDataset import loadDestinations, loadRating
from recommend import recommend_places
from search import recommend_by_content_based_filtering
from urllib import request
from handler.preprocessing import preprocessingWithStem
from sklearn.feature_extraction.text import TfidfVectorizer

tourism = pd.read_csv('./data/destination.csv')

tfidf_df = pd.read_csv('./data/tfidf_preference.csv')
tfidf_matrix = np.full(
    (tourism.shape[0], tfidf_df.shape[1]), tfidf_df.to_numpy())

print(tfidf_matrix.shape)

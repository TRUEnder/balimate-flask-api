from handler.query import query, queryWithColumnNames
from handler.idhandler import decode
import json
import math
import numpy as np
import pandas as pd
from handler.loadDataset import loadDestinations
from recommend import recommend_places
from search import recommend_by_content_based_filtering
from urllib import request
from predict import predict
from handler.preprocessing import preprocessingWithStem
from sklearn.feature_extraction.text import TfidfVectorizer

tourism = pd.read_csv('destination.csv', encoding='latin-1')
tourism = tourism['more_information'].fillna('')
print(tourism)

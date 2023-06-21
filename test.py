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
from recommend_destinations import recommend_destinations

result = recommend_destinations(10)

print(result)

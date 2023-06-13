from handler.query import query, queryWithColumnNames
from handler.idhandler import decode
import json
import pandas as pd
from handler.loadDataset import loadDestinations
from recommend import recommend_places
from search import recommend_by_content_based_filtering
from urllib.parse import unquote

query = unquote("pantai%20di%20badung")

result = recommend_by_content_based_filtering(query)
response = {
    "code": "success",
    "data": result
}

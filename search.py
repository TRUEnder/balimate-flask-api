import pandas as pd
from rapidfuzz import fuzz

# Local module
from handler.loadDataset import loadDestinations


# Content Based Filtering

def recommend_by_content_based_filtering(nama_tempat):

    # Load data

    # resp = loadDestinations()
    # if (resp['code'] == 'success'):
    #     tourism = resp['data']
    # else:
    #     return resp

    # Load data from local (uncomment below code and comment above code block)
    tourism = pd.read_csv('./data/destination.csv', encoding='latin-1')
    tourism = tourism.fillna('')

    data_content_based_filtering = pd.read_csv(
        './data/data_content_based_filtering.csv')

    matched_tempats = []

    for index, tempat in data_content_based_filtering.iterrows():
        nama_tempat_similarity = fuzz.token_set_ratio(
            nama_tempat.lower(), tempat['place_name'])
        city_similarity = fuzz.token_set_ratio(
            nama_tempat.lower(), tempat['city'].lower())
        category_similarity = fuzz.token_set_ratio(
            nama_tempat.lower(), tempat['category'].lower())
        tags_similarity = fuzz.token_set_ratio(
            nama_tempat.lower(), tempat['tags'].lower())
        rating_similarity = tempat['rating'] / 5

        combined_similarity = (nama_tempat_similarity + tags_similarity +
                               rating_similarity + city_similarity + category_similarity) / 5
        matched_tempats.append((index, combined_similarity, tempat['rating']))

    matched_tempats = sorted(
        matched_tempats, key=lambda x: (x[1], x[2]), reverse=True)
    matched_tempats = matched_tempats[:10]  # Ambil 10 tempat terbaik

    tempat_index = []
    for match in matched_tempats:
        tempat_index.append(match[0])

    recommended_nama_tempats = tourism.iloc[tempat_index]

    return recommended_nama_tempats.to_dict('records')

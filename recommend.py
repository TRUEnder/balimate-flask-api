import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Local module
from handler.preprocessing import preprocessingWithoutStem
from handler.loadDataset import loadDestinations, loadRating


# Fungsi rekomendasi

def recommend_places(query, top_n=10):

    # Load data

    # resp = loadDestinations()
    # if (resp['code'] == 'success'):
    #     tourism = resp['data']
    # else:
    #     return resp

    # Load data from local (uncomment below code and comment above code block)
    tourism = pd.read_csv('./data/destination.csv', encoding='latin-1')
    tourism = tourism.fillna('')
    # rating = loadRating()
    # tourism['rating'] = rating

    # Load Data Preprocessing Result

    data_tourism = tourism.copy()
    for index, row in data_tourism.iterrows():
        if row['weekend_holiday_price'] == 0 and row['weekday_price'] == 0:
            data_tourism.at[index, 'price_tags'] = 'Free'
        elif row['weekend_holiday_price'] <= 120000 and row['weekday_price'] <= 120000:
            data_tourism.at[index, 'price_tags'] = 'Middle'
        elif row['weekend_holiday_price'] > 120000 and row['weekday_price'] > 120000:
            data_tourism.at[index, 'price_tags'] = 'Expensive'

    for index, row in data_tourism.iterrows():
        if row['category'] == 'Agrowisata':
            data_tourism.at[index, 'category_tags'] = 'Agrotourism'
        elif row['category'] == 'Belanja':
            data_tourism.at[index, 'category_tags'] = 'Shopping'
        elif row['category'] == 'Pantai':
            data_tourism.at[index, 'category_tags'] = 'Beach'
        elif row['category'] == 'Religius':
            data_tourism.at[index, 'category_tags'] = 'Religious'
        elif row['category'] == 'Budaya':
            data_tourism.at[index, 'category_tags'] = 'Culture'
        elif row['category'] == 'Rekreasi':
            data_tourism.at[index, 'category_tags'] = 'Recreation'
        elif row['category'] == 'Cagar Alam':
            data_tourism.at[index, 'category_tags'] = 'Biodiversity'
        elif row['category'] == 'Alam':
            data_tourism.at[index, 'category_tags'] = 'Nature'

    data_tourism['tags'] = data_tourism['category_tags'] + ' ' + \
        data_tourism['city'] + ' ' + data_tourism['price_tags']
    data_tourism.drop(['lat', 'lng', 'thumbnail_url',
                       'maps_url', 'more_information'], axis=1, inplace=True)
    data_tourism.tags = data_tourism.tags.apply(preprocessingWithoutStem)

    # inisialisasi untuk mengubah teks menjadi representasi TF-IDF.
    tfidf_vectorizer = TfidfVectorizer()

    # Ubah Combined_Text menjadi vektor TF-IDF / mengubah kumpulan teks menjadi representasi vektor
    tfidf_matrix = tfidf_vectorizer.fit_transform(data_tourism['tags'])

    # Melakukan normalisasi pada kolom 'Rating' menggunakan rumus Min-Max Scaling
    normalized_rating = (data_tourism['rating'].min(
    )) / (data_tourism['rating'].max() - data_tourism['rating'].min())

    # Memperbarui kolom 'Rating' dalam dataframe data_content_based_filtering dengan nilai-nilai yang sudah dinormalisasi.
    data_tourism['rating'] = normalized_rating

    # Main processing

    # memproses query dengan mengubahnya menjadi huruf kecil
    processed_query = query.lower()

    # Transformasi query menjadi vektor TF-IDF menggunakan transform() dari objek tfidf_vectorizer.
    query_vector = tfidf_vectorizer.transform([processed_query])

    # Menghitung cosine_similarities antara vektor query dan matriks TF-IDF menggunakan cosine_similarity().
    # Hasilnya kemudian diflatten menjadi satu dimensi
    cosine_similarities = cosine_similarity(
        query_vector, tfidf_matrix).flatten()

    # Mengalikan cosine_similarities dengan nilai rating yang sudah dinormalisasi untuk mendapatkan skor akhir.
    # Skor ini mencerminkan seberapa relevan tempat wisata dengan query pengguna.
    scores = cosine_similarities * normalized_rating

    # Mengurutkan indeks skor dari yang tertinggi ke terendah
    # dan membatasi hanya sejumlah top_n tempat dengan slicing [:top_n].
    top_indices = scores.argsort()[::-1][:top_n]

    # Mengambil Place_Name dari data_content_based_filtering berdasarkan indeks yang telah diurutkan
    # dan mengembalikan hasilnya dalam bentuk recommended_places.
    recommended_places = tourism.iloc[top_indices]

    return recommended_places.to_dict('records')

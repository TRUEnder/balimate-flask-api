import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


# Load data

tourism = pd.read_csv('./data/destination.csv', encoding='latin-1')
tourism = tourism.fillna('')


# Recommend Based on Destination

def recommend_destinations(place_id):

    # Dapatkan index destinasi berdasarkan place_id
    idx = tourism[tourism['place_id'] == place_id].index[0]

    # Dapatkan kategori destinasi
    destination_category = tourism.iloc[idx]['category']

    # Dapatkan kota destinasi
    destination_city = tourism.iloc[idx]['city']

    # Dapatkan indeks destinasi dengan kategori yang sama
    same_category_destinations = tourism[tourism['category']
                                         == destination_category].index.tolist()

    # Hapus destinasi yang dipilih dari daftar yang direkomendasikan
    same_category_destinations.remove(idx)

    # Dapatkan destinasi dengan kategori yang sama tetapi di kota yang berbeda
    same_category_diff_city_destinations = [
        dest for dest in same_category_destinations if tourism.loc[dest]['city'] != destination_city]

    # Jika ada destinasi yang sesuai di kota yang berbeda, lakukan clustering K-means
    if same_category_diff_city_destinations:
        destinations_for_clustering = tourism.loc[same_category_diff_city_destinations, [
            'lat', 'lng']]
    else:
        destinations_for_clustering = tourism.loc[same_category_destinations, [
            'lat', 'lng']]

    top_k = 3

    if len(destinations_for_clustering) >= 5:
        # Melakukan clustering dengan K-means
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(destinations_for_clustering)

        # Dapatkan kluster destinasi berdasarkan hasil clustering K-means
        destination_cluster = kmeans.predict(
            tourism.loc[[idx], ['lat', 'lng']])

        # Dapatkan indeks destinasi dalam kluster yang sama
        same_cluster_destinations = [dest for dest, cluster in zip(
            same_category_destinations, kmeans.labels_) if cluster == destination_cluster]

        # Ambil top-k destinasi dari kluster yang sama secara acak
        top_destinations = same_cluster_destinations[:top_k]
    else:
        # Jika tidak ada cukup destinasi untuk clustering K-means, pilih destinasi secara acak
        top_destinations = np.random.choice(same_category_destinations, size=min(
            top_k, len(same_category_destinations)), replace=False)

    # Dapatkan informasi destinasi yang direkomendasikan
    recommendations = tourism[tourism.index.isin(top_destinations)]

    return recommendations.to_dict('records')

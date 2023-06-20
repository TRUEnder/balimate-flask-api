from handler.query import query, queryWithColumnNames
import pandas as pd


def loadDestinations():
    resp = queryWithColumnNames('SELECT * FROM destination')

    if (resp['code'] == 'success'):
        tourism = pd.DataFrame(resp['data']['records'],
                               columns=resp['data']['column_names'])

        # Dynamic rating
        rating = []
        for destination in resp['data']['records']:
            ratingResp = query(
                'SELECT AVG(rating) FROM review WHERE place_id=' + str(destination[0]))
            avgRating = round(float(ratingResp['data'][0][0]) * 2, 0) / 2

            rating.append(avgRating)
        tourism.insert(7, "rating", rating, True)

        response = {
            "code": "success",
            "data": tourism
        }
        return response

    else:
        return resp


def loadRating():
    resp = queryWithColumnNames('SELECT * FROM destination')

    if (resp['code'] == 'success'):
        # Dynamic rating
        rating = []
        for destination in resp['data']['records']:
            ratingResp = query(
                'SELECT AVG(rating) FROM review WHERE place_id=' + str(destination[0]))
            avgRating = round(float(ratingResp['data'][0][0]) * 2, 0) / 2

            rating.append(avgRating)

        ratingdf = pd.DataFrame(rating, columns=['rating'])
        return ratingdf

    else:
        return resp

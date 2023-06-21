from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import json
import pandas as pd

# Local module
import handler.idhandler as idhandler
from handler.query import query, queryWithColumnNames
from recommend import recommend_places
from recommend_destinations import recommend_destinations
from search import recommend_by_content_based_filtering


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'API is active!'


@app.route('/recommend', methods=['GET'])
def recommendationHandler():
    useridResp = idhandler.decode(request.args.get('userid'))

    if (useridResp['code'] == 'success'):
        userid = useridResp['data']
        queryStat = 'SELECT pref_categories, pref_city, pref_price FROM user WHERE user_id=' + \
            str(userid)
        queryResp = query(queryStat)

        if queryResp['code'] == 'success':

            if (len(queryResp['data']) != 0):
                (category, city, price) = queryResp['data'][0]
                obj = json.loads(category)

                categories = ''
                for item in obj:
                    categories += (item + ' ')

                input = f"{categories} {city} {price} "

                result = recommend_places(input)
                response = {
                    "code": "success",
                    "data": result
                }
                return jsonify(response)

            else:
                response = {
                    "code": "fail",
                    "message": "Data not found"
                }
                return jsonify(response)

        else:
            return jsonify(queryResp)

    else:
        return jsonify(useridResp)


@app.route('/recommendDest')
def recommendDestinationHandler():
    result = recommend_destinations(int(request.args.get('placeid')))
    response = {
        "code": "success",
        "data": result
    }

    return jsonify(response)


@app.route('/search')
def searchHandler():
    query = urllib.parse.unquote(request.args.get('q'))

    result = recommend_by_content_based_filtering(query)
    response = {
        "code": "success",
        "data": result
    }

    return jsonify(response)


# DEPRECATED
# @app.route('/predict')
# def predictionHandler():
#     useridResp = idhandler.decode(request.args.get('userid'))

#     if (useridResp['code'] == 'success'):
#         userid = useridResp['data']
#         queryStat = 'SELECT place_id FROM destination WHERE place_id NOT IN (SELECT place_id FROM review WHERE user_id=' + str(
#             userid) + ')'
#         queryResp = queryWithColumnNames(queryStat)

#         if queryResp['code'] == 'success':
#             if (len(queryResp['data']) != 0):
#                 input_data = pd.DataFrame(queryResp['data']['records'],
#                                           columns=queryResp['data']['column_names'])

#                 result = predict(userid, input_data)
#                 response = {
#                     "code": "success",
#                     "data": result
#                 }
#                 return jsonify(response)

#             else:
#                 response = {
#                     "code": "fail",
#                     "message": "Data not found"
#                 }
#                 return jsonify(response)

#         else:
#             return jsonify(queryResp)

#     else:
#         return jsonify(useridResp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

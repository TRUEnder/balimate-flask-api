from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import json

# Local module
import handler.idhandler as idhandler
from handler.query import query
from recommend import recommend_places
from search import recommend_by_content_based_filtering


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'API is active!'


@app.route('/recommend', methods=['GET'])
def preferenceHandler():
    userid = idhandler.decode(request.args.get('userid'))

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


@app.route('/search')
def searchHandler():
    query = urllib.parse.unquote(request.args.get('q'))

    result = recommend_by_content_based_filtering(query)
    response = {
        "code": "success",
        "data": result
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

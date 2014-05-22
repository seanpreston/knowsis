# -*- coding: utf-8 -*-
from .exceptions import BadRequest, Unauthorized
from .decorators import authenticate
from flask import Flask, jsonify, request
from util import get_tweet_count

app = Flask(__name__)


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Unauthorized)
def handle_unauthorized(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@app.route('/api/v0/tweets/count/', methods=['GET'])
@authenticate
def tweets_view():
    start = request.args.get('startdate', None)
    if start is None:
        raise BadRequest('Please provide a "startdate" parameter in the format yyyy-mm-dd', status_code=400)
    end = request.args.get('enddate', None)       

    count = get_tweet_count(start, end)

    return jsonify({
        'startdate': start,
        'enddate': end if end else start,
        'count': count,
    })


if __name__ == '__main__':
    app.run(debug=True)

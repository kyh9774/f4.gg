from flask import Flask, render_template
import requests
import logging
import pprint
from flask_restful import Api
from keys import FIFA_KEY

import json
from flask import Response
from functools import wraps


application = Flask(__name__)


# def as_json(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         res = f(*args, **kwargs)
#         res = json.dumps(res, ensure_ascii=False).encode('utf8')
#         return Response(res, content_type='application/json; charset=utf-8')
#     return decorated_function


api = Api(application)

logging.basicConfig(
    filename='test.log',
    level=logging.DEBUG
)


@application.route('/')
# @as_json
def home():
    return render_template(
        'index.html',
    )


@application.route('/<nickname>')
def search_nickname(nickname):
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + nickname
    headers = {'Authorization': FIFA_KEY}
    res = requests.get(url, headers=headers)
    user_result = res.json()

    if len(user_result) == 3:
        access_id = user_result['accessId']
        user_match = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/' + access_id + '/matches?matchtype=50&offset={offset}&limit={limit}'
        user_res = requests.get(user_match, headers=headers)
        user_match_result = user_res.json()
    else:
        return user_result

    match_id = user_match_result[0]

    match_url = "https://api.nexon.co.kr/fifaonline4/v1.0/matches/" + match_id
    match_res = requests.get(match_url, headers=headers)
    match_result = match_res.json()
    return match_result

    # player_url = "https://static.api.nexon.co.kr/fifaonline4/latest/spid.json"
    # player_res = requests.get(player_url, headers=headers)
    # player_result = player_res.json()
    # a = match_result['matchInfo'][1]['player'][1]['spId']
    # for player in player_result:
    #     if player['id'] == a:
    #         name = player['name']
    #         playerid = str(a)
    #
    # playerP_url = "https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/players/p" + playerid + ".png"
    # playerP_res = requests.get(playerP_url, headers=headers)
    # playerP_result = playerP_res.json()
    # return player_P_result


if __name__ == '__main__':
    logging.info("Flask Web Server open!!!")
    application.debug = True
    # app.config['DEBUG'] = True
    application.run(host="localhost", port="8080")


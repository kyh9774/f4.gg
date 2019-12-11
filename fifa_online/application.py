from flask import Flask, render_template, request, redirect
import requests
import logging
import pprint
from flask_restful import Api
from flask_wtf import form
import json

from keys import FIFA_KEY
import os


from name import NameForm

application = Flask(__name__)
application.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
application.config['SECRET_KEY'] = os.urandom(24)


api = Api(application)

logging.basicConfig(
    filename='test.log',
    level=logging.DEBUG
)


@application.route('/', methods=['GET', 'POST'])
def home():
    name_form = NameForm()
    name = str(name_form.name.data)
    if request.method == 'POST':
        return redirect('/' + name)

    return render_template(
        'index.html',
        name_form=name_form
    )


@application.route('/<nickname>')
def search_nickname(nickname):
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + nickname
    headers = {'Authorization': FIFA_KEY}
    res = requests.get(url, headers=headers)
    user_result = res.json()

    if len(user_result) == 3:
        access_id = user_result['accessId']
        user_match = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/' + access_id + '/matches?matchtype=52&offset={offset}&limit={limit}'
        user_res = requests.get(user_match, headers=headers)
        user_match_result = user_res.json()
    else:
        return user_result

    match_id = user_match_result[0]

    tier_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users/" + access_id + "/maxdivision"
    tier_res = requests.get(tier_url, headers=headers)
    tier_result = tier_res.json()
    with open('division.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for x in json_data:
        if x['divisionId'] == tier_result[0]['division']:
            tier_name = x['divisionName']


    match_url = "https://api.nexon.co.kr/fifaonline4/v1.0/matches/" + match_id
    match_res = requests.get(match_url, headers=headers)
    match_result = match_res.json()

    name_form = NameForm()
    name = str(name_form.name.data)
    if request.method == 'POST':
        return redirect('/' + name)

    return render_template(
        'temp.html',
        name_form=name_form,
        match_result=match_result,
        user_result=user_result,
        tier_name=tier_name
    )

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


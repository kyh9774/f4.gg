from flask import Flask, render_template, request, redirect
import requests
import logging
import pprint
from flask_restful import Api
from flask_wtf import form
import json

from api import matchDetail, matchRate, latelySquad
from keys import FIFA_KEY
import os


from name import NameForm

application = Flask(__name__)
application.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
application.config['SECRET_KEY'] = os.urandom(24)


api = Api(application)

api.add_resource(matchRate, "/api/matchRate/<nickname>")
api.add_resource(matchDetail, "/api/matchDetail/<matchcode>")
api.add_resource(latelySquad, "/api/latelySquad/<nickname>")


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


@application.route('/<nickname>', methods=['GET', 'POST'])
def search_nickname(nickname):
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + nickname
    headers = {'Authorization': FIFA_KEY}
    res = requests.get(url, headers=headers)
    user_result = res.json()

    if len(user_result) == 3:
        access_id = user_result['accessId']
        user_match = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/' + access_id + '/matches?matchtype=50&offset={offset}&limit=20'
        user_res = requests.get(user_match, headers=headers)
        user_match_result = user_res.json()
    else:
        return user_result

    tier_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users/" + access_id + "/maxdivision"
    tier_res = requests.get(tier_url, headers=headers)
    tier_result = tier_res.json()

    with open('division.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for x in json_data:
        if x['divisionId'] == tier_result[0]['division']:
            tier_name = x['divisionName']

    match_info = []

    for match_id in user_match_result:
        match_url = "https://api.nexon.co.kr/fifaonline4/v1.0/matches/" + match_id
        match_res = requests.get(match_url, headers=headers)
        match_result = match_res.json()
        match_info.append(match_result)

    name_form = NameForm()
    name = str(name_form.name.data)
    if request.method == 'POST':
        return redirect('/' + name)

    rate_url = "http://localhost:8080/api/matchRate/" + nickname
    rate_res = requests.get(rate_url, headers=headers)
    rate_result = rate_res.json()

    return render_template(
        'match.html',
        name_form=name_form,
        match_result=match_result,
        user_result=user_result,
        tier_name=tier_name,
        user_match_result=user_match_result,
        match_info=match_info,
        nickname=nickname,
        rate_result=rate_result
    )


@application.route('/<nickname>/<matchid>', methods=['GET', 'POST'])
def search_match(nickname, matchid):
    url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + nickname
    headers = {'Authorization': FIFA_KEY}
    res = requests.get(url, headers=headers)
    user_result = res.json()

    name_form = NameForm()
    name = str(name_form.name.data)
    if request.method == 'POST':
        return redirect('/' + name)

    if len(user_result) == 3:
        access_id = user_result['accessId']
        user_match = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/' + access_id + '/matches?matchtype=50&offset={offset}&limit=20'
        user_res = requests.get(user_match, headers=headers)
        user_match_result = user_res.json()
    else:
        return user_result

    headers = {'Authorization': FIFA_KEY}
    match_url = "https://api.nexon.co.kr/fifaonline4/v1.0/matches/" + matchid
    match_res = requests.get(match_url, headers=headers)
    match_result = match_res.json()

    tier_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users/" + access_id + "/maxdivision"
    tier_res = requests.get(tier_url, headers=headers)
    tier_result = tier_res.json()

    with open('division.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for x in json_data:
        if x['divisionId'] == tier_result[0]['division']:
            tier_name = x['divisionName']

    my_url = "http://localhost:8080/api/matchDetail/" + matchid
    my_res = requests.get(my_url)
    my_result = my_res.json()

    team1_player = []
    team2_player = []

    for i in range(1, 19):
        img_url = "https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/players/p" + str(my_result['Team1']['PlayerInfo']['Player' + str(i)]['PlayerInfo']['Player_Pid']) + ".png"
        img_res = requests.get(img_url, headers=headers)
        if img_res == 200:
            img_result = img_res.json()
        else:
            img_result = '../static/images/no.PNG'
        team1_player.append(img_result)

    for i in range(1, 19):
        img_url = "https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/players/p" + str(my_result['Team2']['PlayerInfo']['Player' + str(i)]['PlayerInfo']['Player_Pid']) + ".png"
        img_res = requests.get(img_url, headers=headers)
        if img_res == 200:
            img_result = img_res.json()
        else:
            img_result = '../static/images/no.PNG'
        team2_player.append(img_result)

    if my_result['Team1']['TeamInfo']['Team']['Team_Info']['Team_nickname'] == user_result['nickname']:
        regionInfo = my_result['Team1']
    else:
        regionInfo = my_result['Team2']

    rate_url = "http://localhost:8080/api/matchRate/" + nickname
    rate_res = requests.get(rate_url, headers=headers)
    rate_result = rate_res.json()

    return render_template(
        'detail.html',
        match_result=match_result,
        name_form=name_form,
        user_result=user_result,
        tier_name=tier_name,
        my_result=my_result,
        team1_player=team1_player,
        team2_player=team2_player,
        regionInfo=regionInfo,
        rate_result=rate_result
    )


if __name__ == '__main__':
    logging.info("Flask Web Server open!!!")
    application.debug = True
    # app.config['DEBUG'] = True
    application.run(host="localhost", port="8080")


import pprint
import json
import requests
from flask import Blueprint
from flask_restful import Resource, abort, reqparse

from keys import FIFA_KEY

api_blueprint = Blueprint('api', __name__)

def winrate_func(list,key):
    win=0
    for i in list:
        if i==key:
            win=win+1
    return win/len(list)

def average_func(list):
    return round(sum(list)/len(list),2)

def average_func2(list, list2):
    return round(sum(list)/sum(list2),2)





class matchRate(Resource):

    def get(self, nickname):
        url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + nickname
        headers = {'Authorization': FIFA_KEY}
        res = requests.get(url, headers=headers)
        user_result = res.json()

        if len(user_result) == 3:
            access_id = user_result['accessId']
            user_match = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/' + access_id + '/matches?matchtype=50&offset=0&limit=20'
            user_res = requests.get(user_match, headers=headers)
            user_match_result = user_res.json()
        else:
            return user_result

        # winRate:승률, badEndRate:몰수패 비율
        winRate = []
        badEndRate = []

        # goalRate:골 수, goalAgainst:평균 실점, goalRate_Heading:헤딩골 수, goalRate_Shooting:슈팅골 수, goal_In:페널티 인 골, goal_Out:페널티 아웃 골
        goalRate=[]
        goalAgainst=[]
        goalRate_Heading=[]
        goalRate_Shooting=[]
        goal_In=[]
        goal_Out=[]


        # shootRate:평균 슛, effectiveshootRate:평균 유효슛, shootRate_Heading:헤딩 수, shootRate_Shooting:슈팅 슈, shootRate_In: 페널티 인 슛, shootRate_Out: 페널티 아웃 슛
        shootRate=[]
        effectiveshootRate=[]
        shootRate_Heading=[]
        shootRate_Shooting=[]
        shootRate_In=[]
        shootRate_Out=[]

        # success_Shoot_Rate:슛 성공 확률, success_Effectiveshoot_Rate: 유효슛 성공 확률, success_Shoot_Shooting: 슈팅 성공 확률, success_Shoot_Heading: 헤딩 성공 확률

        # pass:패스 시도,확률, shortPass:짧은패스 시도,확률, longPass:긴패스 시도, 확률, throughPass:쓰루패스 시도, 확률, lobbedThroughPass:로빙패스 시도, 확률
        passTry=[]
        passSuccess=[]
        shortPassTry=[]
        shortPassSuccess=[]
        longPassTry=[]
        longPassSuccess=[]
        throughPassTry=[]
        throughPassSuccess=[]
        lobbedThroughPassTry=[]
        lobbedThroughPassSuccess=[]




        if len(user_match_result) == 0:
            return user_match_result

        else:
            for i in user_match_result:
                match_info= 'https://api.nexon.co.kr/fifaonline4/v1.0/matches/' + i
                match_res = requests.get(match_info, headers=headers)
                match_result = match_res.json()

             # pprint.pprint(match_result)

                if match_result['matchInfo'][0]['accessId'] == access_id:

                    #승률, 몰수패 비율
                    winRate.append(match_result['matchInfo'][0]['matchDetail']['matchResult'])
                    badEndRate.append(match_result['matchInfo'][0]['matchDetail']['matchEndType'])

                    #골 수, 평균 실점, 헤딩골 수, 슈팅골 수, 페널티 인 골, 페널티 아웃 골
                    goalRate.append(match_result['matchInfo'][0]['shoot']['goalTotal'])
                    goalAgainst.append(match_result['matchInfo'][1]['shoot']['goalTotal'])
                    goalRate_Heading.append(match_result['matchInfo'][0]['shoot']['goalHeading'])
                    goalRate_Shooting.append(match_result['matchInfo'][0]['shoot']['goalTotal']-match_result['matchInfo'][0]['shoot']['goalHeading'])
                    goal_In.append(match_result['matchInfo'][0]['shoot']['goalInPenalty'])
                    goal_Out.append(match_result['matchInfo'][0]['shoot']['goalOutPenalty'])

                    #평균 슛, 평균 유효슛, 헤딩 수, 슈팅 슈, 페널티 인 슛, 페널티 아웃 슛
                    shootRate.append(match_result['matchInfo'][0]['shoot']['shootTotal'])
                    effectiveshootRate.append(match_result['matchInfo'][0]['shoot']['effectiveShootTotal'])
                    shootRate_Heading.append(match_result['matchInfo'][0]['shoot']['shootHeading'])
                    shootRate_Shooting.append(match_result['matchInfo'][0]['shoot']['shootTotal'] - match_result['matchInfo'][0]['shoot']['shootHeading'])
                    shootRate_In.append(match_result['matchInfo'][0]['shoot']['shootInPenalty'])
                    shootRate_Out.append(match_result['matchInfo'][0]['shoot']['shootOutPenalty'])

                    #패스 시도,확률, 짧은패스 시도,확률, 긴패스 시도, 확률, 쓰루패스 시도, 확률, 로빙패스 시도, 확률
                    passTry.append(match_result['matchInfo'][0]['pass']['passTry'])
                    passSuccess.append(match_result['matchInfo'][0]['pass']['passSuccess'])
                    shortPassTry.append(match_result['matchInfo'][0]['pass']['shortPassTry'])
                    shortPassSuccess.append(match_result['matchInfo'][0]['pass']['shortPassSuccess'])
                    longPassTry.append(match_result['matchInfo'][0]['pass']['longPassTry'])
                    longPassSuccess.append(match_result['matchInfo'][0]['pass']['longPassSuccess'])
                    throughPassTry.append(match_result['matchInfo'][0]['pass']['throughPassTry'])
                    throughPassSuccess.append(match_result['matchInfo'][0]['pass']['throughPassSuccess'])
                    lobbedThroughPassTry.append(match_result['matchInfo'][0]['pass']['lobbedThroughPassTry'])
                    lobbedThroughPassSuccess.append(match_result['matchInfo'][0]['pass']['lobbedThroughPassSuccess'])



                else:
                    # 승률 및 몰수패 비율
                    winRate.append(match_result['matchInfo'][1]['matchDetail']['matchResult'])
                    badEndRate.append(match_result['matchInfo'][1]['matchDetail']['matchEndType'])

                    # 골 수, 평균 실점, 헤딩골 수, 슈팅골 수, 페널티 인 골, 페널티 아웃 골
                    goalRate.append(match_result['matchInfo'][1]['shoot']['goalTotal'])
                    goalAgainst.append(match_result['matchInfo'][0]['shoot']['goalTotal'])
                    goalRate_Heading.append(match_result['matchInfo'][1]['shoot']['goalHeading'])
                    goalRate_Shooting.append(match_result['matchInfo'][1]['shoot']['goalTotal'] - match_result['matchInfo'][1]['shoot']['goalHeading'])
                    goal_In.append(match_result['matchInfo'][1]['shoot']['goalInPenalty'])
                    goal_Out.append(match_result['matchInfo'][1]['shoot']['goalOutPenalty'])

                    #평균 슛, 평균 유효슛, 헤딩 수, 슈팅 슈, 페널티 인 슛, 페널티 아웃 슛
                    shootRate.append(match_result['matchInfo'][1]['shoot']['shootTotal'])
                    effectiveshootRate.append(match_result['matchInfo'][1]['shoot']['effectiveShootTotal'])
                    shootRate_Heading.append(match_result['matchInfo'][1]['shoot']['shootHeading'])
                    shootRate_Shooting.append(match_result['matchInfo'][1]['shoot']['shootTotal'] - match_result['matchInfo'][1]['shoot']['shootHeading'])
                    shootRate_In.append(match_result['matchInfo'][1]['shoot']['shootInPenalty'])
                    shootRate_Out.append(match_result['matchInfo'][1]['shoot']['shootOutPenalty'])

                    #패스 시도,확률, 짧은패스 시도,확률, 긴패스 시도, 확률, 쓰루패스 시도, 확률, 로빙패스 시도, 확률
                    passTry.append(match_result['matchInfo'][1]['pass']['passTry'])
                    passSuccess.append(match_result['matchInfo'][1]['pass']['passSuccess'])
                    shortPassTry.append(match_result['matchInfo'][1]['pass']['shortPassTry'])
                    shortPassSuccess.append(match_result['matchInfo'][1]['pass']['shortPassSuccess'])
                    longPassTry.append(match_result['matchInfo'][1]['pass']['longPassTry'])
                    longPassSuccess.append(match_result['matchInfo'][1]['pass']['longPassSuccess'])
                    throughPassTry.append(match_result['matchInfo'][1]['pass']['throughPassTry'])
                    throughPassSuccess.append(match_result['matchInfo'][1]['pass']['throughPassSuccess'])
                    lobbedThroughPassTry.append(match_result['matchInfo'][1]['pass']['lobbedThroughPassTry'])
                    lobbedThroughPassSuccess.append(match_result['matchInfo'][1]['pass']['lobbedThroughPassSuccess'])



        matchRate_dict = {
            # winRate:승률, badEndRate:몰수패 비율
            'winLoseInfo': {
                'winRate': winrate_func(winRate,"승"),
                'badEndRate': winrate_func(badEndRate,2)
            },

            # goalRate:골 수, goalAgainst:평균 실점, goalRate_Shooting:슈팅골 수, goalRate_Heading:헤딩골 수, goal_In:페널티 인 골, goal_Out:페널티 아웃 골
            'goalInfo': {
                'goalRate': average_func(goalRate),
                'goalAgainst': average_func(goalAgainst),
                'goalRate_Shooting': average_func2(goalRate_Shooting,goalRate),
                'goalRate_Heading': average_func2(goalRate_Heading,goalRate),
                'goal_In': average_func2(goal_In,goalRate),
                'goal_Out': average_func2(goal_Out,goalRate)
            },

            # shootRate:평균 슛, effectiveshootRate:평균 유효슛, shootRate_Shooting:슈팅 비율, shootRate_Heading:헤딩 비율, shootRate_In: 페널티 인 슛 비율, shootRate_Out: 페널티 아웃 슛 비율
            'shootInfo': {
                'shootRate': average_func(shootRate),
                'effectiveShootRate': average_func2(effectiveshootRate,shootRate),
                'shootRate_Shooting': average_func2(shootRate_Shooting,shootRate),
                'shootRate_Heading': average_func2(shootRate_Heading,shootRate),
                'shootRate_In': average_func2(shootRate_In,shootRate),
                'shootRate_Out': average_func2(shootRate_Out,shootRate)
            },

            # success_Shoot_Rate:슛 성공 확률, success_Effectiveshoot_Rate: 유효슛 성공 확률, success_Shoot_Shooting: 슈팅 성공 확률, success_Shoot_Heading: 헤딩 성공 확률, success_Shoot_In:페널티 인 슛 성공 확률, success_Shoot_Out:페널티 아웃 슛 성공 확률
            'success_ShootInfo': {
                'success_Shoot_Rate': average_func2(goalRate,shootRate),
                'success_Effectiveshoot_Rate': average_func2(goalRate,effectiveshootRate),
                'success_Shoot_Shooting': average_func2(goalRate_Shooting,shootRate_Shooting),
                'success_Shoot_Heading': average_func2(goalRate_Heading,shootRate_Heading),
                'success_Shoot_In': average_func2(goal_In,shootRate_In),
                'success_Shoot_Out': average_func2(goal_Out,shootRate_Out)
            },

            # shortPassRate:짧은 패스 비율, longPassRate:긴 패스 비율, throughPassRate:쓰루 패스 비율, lobbedThroughPassRate:로빙 패스 비율
            'passInfo': {
                'shortPassRate': average_func2(shortPassTry,passTry),
                'longPassRate': average_func2(longPassTry, passTry),
                'throughPassRate': average_func2(throughPassTry, passTry),
                'lobbedThroughPassRate': average_func2(lobbedThroughPassTry, passTry)
            },

            # passSuccess:패스 성공률, shortPassSuccess:짧은패스 성공률, longPassSuccess:긴패스 성공률, throughPassSuccess:쓰루패스 성공률, lobbedThroughPassSuccess:로빙패스 성공률
            'success_PassInfo': {
                'passSuccess': average_func2(passSuccess,passTry),
                'shortPassSuccess': average_func2(shortPassSuccess, shortPassTry),
                'longPassSuccess': average_func2(longPassSuccess, longPassTry),
                'throughPassSuccess': average_func2(throughPassSuccess, throughPassTry),
                'lobbedThroughPassSuccess': average_func2(lobbedThroughPassSuccess,lobbedThroughPassTry)
            }

        }


        return matchRate_dict

        # return json.dumps(matchRate_dict)

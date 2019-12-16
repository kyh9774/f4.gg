

import pprint
import json
import requests
from flask import Blueprint
from flask_restful import Resource, abort, reqparse

from keys import FIFA_KEY

headers = {'Authorization': FIFA_KEY}
api_blueprint = Blueprint('api', __name__)

def winrate_func(list,key):
    win=0
    for i in list:
        if i==key:
            win=win+1
    return round(win/len(list),2)

def average_func(list):
    if len(list)==0:
        return 0
    return round(sum(list)/len(list),2)

def average_func2(list, list2):
    if sum(list2)==0:
        return 0
    return round(sum(list)/sum(list2),2)

def average_func3(int, int2):
    if int2==0:
        return 0
    return round(int/int2,2)

# 팀기록 딕셔너리 함수
def TeamSet(dic,TemaNum):
    Team = {
        'Team': {
            'Team_Info': {
                #팀 닉네임
                'Team_nickname': dic['matchInfo'][TemaNum]['nickname'],
            },
            'Team_Record': {
                # 팀경기결과, 팀 몰수패 여부, 팀 점유율, 팀 레드카드, 팀 옐로우카드
                'Team_winLoseInfo': {
                    'Team_MatchResult': dic['matchInfo'][TemaNum]['matchDetail']['matchResult'],
                    'Team_MatchResultType': dic['matchInfo'][TemaNum]['matchDetail']['matchEndType'],
                    'Team_RedCard': dic['matchInfo'][TemaNum]['matchDetail']['redCards'],
                    'Team_YellowCard': dic['matchInfo'][TemaNum]['matchDetail']['yellowCards'],
                },
                #팀 점수, 팀 실점, 팀 헤딩골, 팀 슈팅골, 페널티인 골 비율, 페널티아웃 골 비율
                'Team_GoalInfo': {
                    'Team_Score': dic['matchInfo'][TemaNum]['shoot']['goalTotal'],
                    'Team_goalAgainst': dic['matchInfo'][abs(TemaNum-1)]['shoot']['goalTotal'],
                    'Team_HeadingGoal': dic['matchInfo'][TemaNum]['shoot']['goalHeading'],
                    'Team_ShootingGoal': dic['matchInfo'][TemaNum]['shoot']['goalTotal'] - dic['matchInfo'][TemaNum]['shoot']['goalHeading'],
                    'Team_Goal_In': average_func3(dic['matchInfo'][TemaNum]['shoot']['goalInPenalty'],
                                                  dic['matchInfo'][TemaNum]['shoot']['goalTotal']),
                    'Team_Goal_Out': average_func3(dic['matchInfo'][TemaNum]['shoot']['goalOutPenalty'],
                                                   dic['matchInfo'][TemaNum]['shoot']['goalTotal'])

                },
                # 팀 슈팅, 팀 유효슈팅, 팀 슈팅성공률, 팀 유효슈팅성공률, 페널티인슈팅확률, 페널티아웃 슈팅확률, 헤딩슈팅비율, 슈팅비율
                'Team_ShootInfo': {
                    'Team_Shoot': dic['matchInfo'][TemaNum]['shoot']['shootTotal'],
                    'Team_EffectiveShoot': dic['matchInfo'][TemaNum]['shoot']['effectiveShootTotal'],
                    'Team_SuccessShootRate': average_func3(dic['matchInfo'][TemaNum]['shoot']['goalTotal'],
                                                    dic['matchInfo'][TemaNum]['shoot']['shootTotal']),
                    'Team_SuccessEffectiveShootRate': average_func3(dic['matchInfo'][TemaNum]['shoot']['goalTotal'],
                                                             dic['matchInfo'][TemaNum]['shoot']['effectiveShootTotal']),
                    'Team_ShootRate_In': average_func3(dic['matchInfo'][TemaNum]['shoot']['shootInPenalty'],
                                                       dic['matchInfo'][TemaNum]['shoot']['shootTotal']),
                    'Team_ShootRate_Out': average_func3(dic['matchInfo'][TemaNum]['shoot']['shootOutPenalty'],
                                                       dic['matchInfo'][TemaNum]['shoot']['shootTotal']),
                    'Team_ShootRate_Heading': average_func3(dic['matchInfo'][TemaNum]['shoot']['shootHeading'],
                                                            dic['matchInfo'][TemaNum]['shoot']['shootTotal']),
                    'Team_ShootRate_Shooting': average_func3(dic['matchInfo'][TemaNum]['shoot']['shootTotal']-dic['matchInfo'][TemaNum]['shoot']['shootHeading'],
                                                             dic['matchInfo'][TemaNum]['shoot']['shootTotal'])
                },
                'Team_PassInfo': {
                    # 팀 패스성공률, 짧은패스 성공률, 긴패스 성공률, 쓰루패스 성공률, 로빙패스 성공률, 팀점유율,
                    'Team_PassSuccess': average_func3(dic['matchInfo'][TemaNum]['pass']['passSuccess'],
                                                   dic['matchInfo'][TemaNum]['pass']['passTry']),
                    'Team_ShortPassSuccess': average_func3(dic['matchInfo'][TemaNum]['pass']['shortPassSuccess'],
                                                   dic['matchInfo'][TemaNum]['pass']['shortPassTry']),
                    'Team_LongPassSuccess': average_func3(dic['matchInfo'][TemaNum]['pass']['longPassSuccess'],
                                                           dic['matchInfo'][TemaNum]['pass']['longPassTry']),
                    'Team_ThroughPassSuccess': average_func3(dic['matchInfo'][TemaNum]['pass']['throughPassSuccess'],
                                                           dic['matchInfo'][TemaNum]['pass']['throughPassTry']),
                    'Team_LobbedThroughPassSuccess': average_func3(dic['matchInfo'][TemaNum]['pass']['lobbedThroughPassSuccess'],
                                                           dic['matchInfo'][TemaNum]['pass']['lobbedThroughPassTry']),
                    'Team_Passession': dic['matchInfo'][TemaNum]['matchDetail']['possession'],
                }
            }
        }
    }
    return Team

#선수기록 딕셔너리 함수
def PlayerSet(dic,TemaNum,PlayerNUm):
    Player = {
        'PlayerInfo': {
            #선수 이름, 포지션 ,선수 강화등급
            'Player_Name': PlayerNameSet(dic['matchInfo'][TemaNum]['player'][PlayerNUm]['spId']),
            'Player_Position': PlayerPositionPosSet(dic['matchInfo'][TemaNum]['player'][PlayerNUm]['spPosition']),
            'Player_Grade':dic['matchInfo'][TemaNum]['player'][PlayerNUm]['spGrade']
        },

        'Player_Record': {
            #선수 슈팅, 선수 패스성공률, 선수 어시스트, 선수 골, 선수 평점
            'Player_Shoot': dic['matchInfo'][TemaNum]['player'][PlayerNUm]['status']['shoot'],
            'Player_PassRate': average_func3(dic['matchInfo'][TemaNum]['player'][PlayerNUm]['status']['passSuccess'],
                                         dic['matchInfo'][TemaNum]['player'][PlayerNUm]['status']['passTry']),
            'Player_Assist': dic['matchInfo'][TemaNum]['player'][PlayerNUm]['status']['assist'],
            'Player_Goal': dic['matchInfo'][TemaNum]['player'][PlayerNUm]['status']['goal'],
            'Player_Score': dic['matchInfo'][TemaNum]['player'][PlayerNUm]['status']['spRating']
        }
    }
    return Player

#선수 이름 파악
def PlayerNameSet(name):
    with open('spid.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for i in json_data:
        if i['id'] == name:
            name = i['name']
    return name

# 선수 포지션 파악
def PlayerPositionPosSet(position):
    with open('spposition.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for i in json_data:
        if i['spposition'] == position:
            position = i['desc']
    return position

# 최근경기 정보
class matchRate(Resource):

    def get(self, nickname):
        url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname=" + nickname
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

        pprint.pprint(matchRate_dict)
        # match_Rate_json = json.dumps(matchRate_dict, indent=4, sort_keys=True)
        # match_Rate_json = json.dumps(matchRate_dict,indent=4)
        # match_Rate_json = json.dumps(matchRate_dict,indent=4, ensure_ascii = False)
        match_Rate_json = json.dumps(matchRate_dict, ensure_ascii=False, indent="\t")

        return matchRate_dict
        pprint.pprint(match_Rate_json)
        # return match_Rate_json
        # return json.dumps(matchRate_dict, ensure_ascii = False, indent='\t')
        # return json.dumps(matchRate_dict, ensure_ascii=False, indent="\t")


# 특정경기의 상세정보
class matchDetail(Resource):

    def get(self, matchcode):
        match_info = 'https://api.nexon.co.kr/fifaonline4/v1.0/matches/' + matchcode
        match_res = requests.get(match_info, headers=headers)
        match_result = match_res.json()

        #팀1, 팀2 딕셔너리  팀 기록
        Team_0 = TeamSet(match_result,0)
        Team_1 = TeamSet(match_result, 1)

        #팀1, 팀2 선수 기록
        PlayerInfo_0={
            'Player1':PlayerSet(match_result,0, 0),
            'Player2': PlayerSet(match_result, 0, 1),
            'Player3': PlayerSet(match_result, 0, 2),
            'Player4': PlayerSet(match_result, 0, 3),
            'Player5': PlayerSet(match_result, 0, 4),
            'Player6': PlayerSet(match_result, 0, 5),
            'Player7': PlayerSet(match_result, 0, 6),
            'Player8': PlayerSet(match_result, 0, 7),
            'Player9': PlayerSet(match_result, 0, 8),
            'Player10': PlayerSet(match_result, 0, 9),
            'Player11': PlayerSet(match_result, 0, 10),
            'Player12': PlayerSet(match_result, 0, 11),
            'Player13': PlayerSet(match_result, 0, 12),
            'Player14': PlayerSet(match_result, 0, 13),
            'Player15': PlayerSet(match_result, 0, 14),
            'Player16': PlayerSet(match_result, 0, 15),
            'Player17': PlayerSet(match_result, 0, 16),
            'Player18': PlayerSet(match_result, 0, 17)
        }
        PlayerInfo_1={
            'Player1':PlayerSet(match_result,1, 0),
            'Player2': PlayerSet(match_result, 1, 1),
            'Player3': PlayerSet(match_result, 1, 2),
            'Player4': PlayerSet(match_result, 1, 3),
            'Player5': PlayerSet(match_result, 1, 4),
            'Player6': PlayerSet(match_result, 1, 5),
            'Player7': PlayerSet(match_result, 1, 6),
            'Player8': PlayerSet(match_result, 1, 7),
            'Player9': PlayerSet(match_result, 1, 8),
            'Player10': PlayerSet(match_result, 1, 9),
            'Player11': PlayerSet(match_result, 1, 10),
            'Player12': PlayerSet(match_result, 1, 11),
            'Player13': PlayerSet(match_result, 1, 12),
            'Player14': PlayerSet(match_result, 1, 13),
            'Player15': PlayerSet(match_result, 1, 14),
            'Player16': PlayerSet(match_result, 1, 15),
            'Player17': PlayerSet(match_result, 1, 16),
            'Player18': PlayerSet(match_result, 1, 17)
        }

        matchDetailInfo = {
            'Team1': {
                'TeamInfo': Team_0,
                'PlayerInfo':PlayerInfo_0
            },
            'Team2': {
                'TeamInfo': Team_1,
                'PlayerInfo': PlayerInfo_1
            }
         }


        # pprint.pprint(matchDetailInfo)

        matchDetail_Json=json.dumps(matchDetailInfo, ensure_ascii=False, indent="\t")
        pprint.pprint(matchDetail_Json)
        # return matchDetail_Json
        return matchDetailInfo






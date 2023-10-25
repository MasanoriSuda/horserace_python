import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re
import urllib.request, urllib.error
from tqdm import tqdm
import datetime
import os
import math
from enum import Enum

#非ライブラリ
from racetrack import racetrack_mappings
from horserace_util import getRaceResultLocal,getRaceResultJRA, getHorseInfo, getDateForDataAnalysis
from jockeytable import jockey_mappings
from racetable import *

class HorseIdNumInfo(Enum):
    HORSE_ID_NUMINFO_HORSE_ID       =  'horse_id' #馬id
    HORSE_ID_NUMINFO_SEX            =  'sex' #性
    HORSE_ID_NUMINFO_AGE            =  'age' #齢
    HORSE_ID_NUMINFO_DATE           =  'date' #日付
    HORSE_ID_NUMINFO_TRACK          =  'track' #開催
    HORSE_ID_NUMINFO_WEATHER        =  'weather' #天気
    HORSE_ID_NUMINFO_RACE_NUM       =  'race_num' #レース番
    HORSE_ID_NUMINFO_HORSE_NUM_ANIM =  'horse_num_anim' #頭数
    HORSE_ID_NUMINFO_HORSE_NUM      =  'horse_num' #馬番
    HORSE_ID_NUMINFO_ODDS           =  'odds' #オッズ
    HORSE_ID_NUMINFO_POPURALITY     =  'popularity' #人気
    HORSE_ID_NUMINFO_ORDER          =  'order' #着順
    HORSE_ID_NUMINFO_JOCKEY         =  'jockey' #騎手
    HORSE_ID_NUMINFO_WEIGHT         =  'weight' #斤量
    HORSE_ID_NUMINFO_DIRT_GRASS     =  'dirt_grass' #ダートor芝
    HORSE_ID_NUMINFO_DISTANCE       =  'distance' #距離
    HORSE_ID_NUMINFO_CONDITION      =  'condition' #馬場コンディション
    HORSE_ID_NUMINFO_TIME           =  'time' #タイム
    HORSE_ID_NUMINFO_3FURLONG       =  '3furlong' #上がり
    HORSE_ID_NUMINFO_HORSE_WEIGHT   =  'horse_weight' #馬体重
    HORSE_ID_NUMINFO_WEIGHT_INCDEC  =  'weight_incdec' #増減

#日付     開催   天気     R          レース名  映像  頭数   枠番  馬番   オッズ  人気  着順    騎手  斤量     距離 馬場 馬場指数     タイム   着差 ﾀｲﾑ指数           通過        ペース    上り       馬体重  厩舎ｺﾒﾝﾄ  備考     勝ち馬(2着馬)       賞金
class RACE(Enum):
    RACE_DATE  = '日付'
    RACE_TRACK    ='開催'
    RACE_WEATHER   = '天気'
    RACE_NUM= 'R'
    RACE__RACE_NAME='レース名'
    RACE_VIDEO='映像'
    RACE_NUM_ANIM='頭数'
    RACE_FRAME='枠番'
    RACE_HORSE_NUM='馬番'
    RACE_ODDS='オッズ'
    RACE_POP='人気'
    RACE_ORDER ='着順'
    RACE_JOCKEY='騎手'
    RACE_WEIGHT='斤量'
    RACE_DIRT_GRASS_DISTANCE='距離'
    RACE_CONDITION='馬場'
    RACE_CONDITION_POINT='馬場指数'
    RACE_TIME='タイム'
    RACE_DIFF_DELI='着差'
    RACE_TIME_POINT='タイム指数'
    RACE_PASSING='通過'
    RACE_PACE='ペース'
    RACE_3FURLONG='上り'
    RACE_HORSE_WEIGHT='馬体重'
    RACE_COMMENT='厩舎コメント'
    RACE_ETC='備考'
    RACE_WINNER='勝ち馬(2着馬)'
    RACE_PRICE='賞金'

#着順  枠番  馬番        馬名  性齢  斤量    騎手     タイム   着差   単勝  人気     馬体重       調教師
class HORSE(Enum):
    HORSE_ORDER     = '着順'
    HORSE_FRAME     ='枠番'
    HORSE_HORSE_NUM ='馬番'
    HORSE_NAME='馬名'
    HORSE_SEX_AGE ='性齢'
    HORSE_WEIGHT ='斤量'
    HORSE_JOCKEY ='騎手'
    HORSE_TIME ='タイム'
    HORSE_DIFF_DELI='着差'
    HORSE_DIFF_ODDS ='単勝'
    HORSE_POPORALITY ='人気'
    HORSE_HORSE_WEIGHT ='馬体重'
    HORSE_TRAINER ='調教師'


#対象レースの5戦を無理やり取得するためのパラメータ
FORCE_BREAK = False
horse_race_lists___ =[
    ["2023/11/03","JBCCLASSIC_2023",horse_id_list_2023_jbc_plan]
]

horse_race_lists =[
        ["2017/11/03","JBCCLASSIC_2017",horse_id_list_JBC2017],
]

horse_race_lists_ =[
    ["2021/07/14","JAPANDIRTDURBY_2021",horse_id_list_2021_jdd],
    ["2022/07/13","JAPANDIRTDURBY_2022",horse_id_list_2022_jdd],
    ["2023/07/12","JAPANDIRTDURBY_2023",horse_id_list_2023_jdd],    
    ["2014/06/25","TEIOU_2014",horse_id_list_teiou_2014], 
    ["2015/06/24","TEIOU_2015",horse_id_list_teiou_2015], 
    ["2016/06/29","TEIOU_2016",horse_id_list_teiou_2016], 
    ["2017/06/28","TEIOU_2017",horse_id_list_teiou_2017], 
    ["2018/06/27","TEIOU_2018",horse_id_list_teiou_2018], 
    ["2019/06/26","TEIOU_2019",horse_id_list_teiou_2019], 
    ["2020/06/24","TEIOU_2020",horse_id_list_teiou_2020], 
    ["2021/06/30","TEIOU_2021",horse_id_list_teiou_2021], 
    ["2022/06/29","TEIOU_2022",horse_id_list_teiou_2022], 
    ["2023/06/28","TEIOU_2023",horse_id_list_teiou_2023],
    ["2018/12/02","CHAMPIONSCUP_2018",horse_id_list_2018_championscup],
    ["2019/12/01","CHAMPIONSCUP_2019",horse_id_list_2019_championscup],
    ["2020/12/06","CHAMPIONSCUP_2020",horse_id_list_2020_championscup],
    ["2021/12/05","CHAMPIONSCUP_2021",horse_id_list_2021_championscup],
    ["2022/12/04","CHAMPIONSCUP_2022",horse_id_list_2022_championscup],      
    ["2013/11/04","JBCCLASSIC_2013",horse_id_list_JBC2013],
    ["2014/11/03","JBCCLASSIC_2014",horse_id_list_JBC2014],          
    ["2015/11/03","JBCCLASSIC_2015",horse_id_list_JBC2015],
    ["2016/11/03","JBCCLASSIC_2016",horse_id_list_JBC2016],
    ["2017/11/03","JBCCLASSIC_2017",horse_id_list_JBC2017],
    ["2018/11/04","JBCCLASSIC_2018",horse_id_list_JBC2018],
    ["2019/11/04","JBCCLASSIC_2019",horse_id_list_JBC2019],          
    ["2020/11/03","JBCCLASSIC_2020",horse_id_list_JBC2020],
    ["2021/11/03","JBCCLASSIC_2021",horse_id_list_JBC2021],
    ["2022/11/03","JBCCLASSIC_2022",horse_id_list_JBC2022],
    ["2013/12/29","DAISHOUTEN_2013",horse_id_list_2013_daishouten],
    ["2014/12/29","DAISHOUTEN_2014",horse_id_list_2014_daishouten],
    ["2015/12/29","DAISHOUTEN_2015",horse_id_list_2015_daishouten],
    ["2016/12/29","DAISHOUTEN_2016",horse_id_list_2016_daishouten],
    ["2017/12/29","DAISHOUTEN_2017",horse_id_list_2017_daishouten],
    ["2018/12/29","DAISHOUTEN_2018",horse_id_list_2018_daishouten],
    ["2019/12/29","DAISHOUTEN_2019",horse_id_list_2019_daishouten],
    ["2020/12/29","DAISHOUTEN_2020",horse_id_list_2020_daishouten],
    ["2021/12/29","DAISHOUTEN_2021",horse_id_list_2021_daishouten],
    ["2022/12/29","DAISHOUTEN_2022",horse_id_list_2022_daishouten],
    ["2021/01/27","KAWASAKI_2021",horse_id_list_2021_kawasaki],
    ["2022/02/02","KAWASAKI_2022",horse_id_list_2022_kawasaki],
    ["2023/02/01","KAWASAKI_2023",horse_id_list_2023_kawasaki],
#    ["2023/11/03","JBCCLASSIC_2023",horse_id_list_2023_jbc_plan]
]

def main():
    print("start")

    for list in horse_race_lists:
        makeRaceInfo(list[0],list[1],list[2])    

def makeRaceInfo(day,racename,horse_id_list):
    print("start")

    df = pd.DataFrame()
    OBJECT_DAY = day
    RACE_NAME  = racename
    horse_id_list = horse_id_list

    teiou_train_2023_df = pd.DataFrame()
    teiou_test_2023_df = pd.DataFrame()

    jbc_counter = 202001
    for horse_id in horse_id_list:
        horse_info_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id/' + str(horse_id) +'.csv'

        is_file = os.path.isfile(horse_info_path)
        if is_file:
            print("file exists")
        else:
            horse_info_data_frame = getHorseInfo(horse_id)
            print(horse_info_data_frame)
            horse_info_data_frame.to_csv(horse_info_path)     

        horse_info_data_frame = pd.read_csv(horse_info_path,index_col=0 )

        horse_info_data_frame = horse_info_data_frame[horse_info_data_frame['着順'] != '除']
        horse_info_data_frame = horse_info_data_frame[horse_info_data_frame['着順'] != '取']
        horse_info_data_frame = horse_info_data_frame[horse_info_data_frame['馬体重'] != '計不']
        horse_info_data_frame = horse_info_data_frame[horse_info_data_frame['着順'] != '中']
        horse_info_data_frame = horse_info_data_frame[horse_info_data_frame['着順'].isna() == False]
        horse_info_data_frame = horse_info_data_frame[horse_info_data_frame['天気'].isna() == False]

        horse_id_set =[]
        sex          =[]
        age          =[]
        date         =[]
        dateforda    =[]
        place        =[]
        track        =[]
        weather      =[]
        race_num     =[]
        horse_race_anim=[]
        horse_num=[]
        odds=[]
        popularity=[]
        order =[]
        jockey=[]
        weight=[]
        dirt_grass=[]
        distance=[]
        condition=[]
        time=[]
        furlong3=[]
        horse_weight=[]
        weight_incdec = []
        same_track = []
        g1_age3 = []
        g2_age3 = []
        g3_age3 = []
        g1_age4 = []
        g2_age4 = []
        g3_age4 = []
        money   = []

        #レースから照合するためのパラメータを取得
        for tmp_place in horse_info_data_frame['開催']:
            horse_id_set.append(horse_id)

        for tmp_place in horse_info_data_frame['開催']:
            tmp2_place = tmp_place
            place.append(tmp2_place)

        for tmp_place in horse_info_data_frame['開催']:
            if(tmp_place == '大井'):
                same_track.append(1)
            else:
                same_track.append(0)

        for tmp_date in horse_info_data_frame['日付']:
            date.append(tmp_date)

        for tmp_race_num in horse_info_data_frame['R']:
            if(math.isnan(tmp_race_num)):
                race_num.append(11.0)
            else:
                race_num.append(tmp_race_num)

        for tmp_horse_num in horse_info_data_frame['馬番']:
            horse_num.append(tmp_horse_num)

        for tmp_horse_race_anim in horse_info_data_frame['頭数']:
            horse_race_anim.append(tmp_horse_race_anim)

        for tmp_horse_num in horse_info_data_frame['天気']:

            weather_mapping={'晴':6,'曇':5,'小雨':4,'雨':3,'小雪':2,'雪':1}
            tmp_weather = weather_mapping[tmp_horse_num]
            weather.append(tmp_weather)

        for tmp2_dirt_or_grass in horse_info_data_frame['距離']:
            tmp_dirt_or_grass = tmp2_dirt_or_grass[0]
            if(tmp_dirt_or_grass=='芝'):
                dirt_grass.append('1')
            else:
                dirt_grass.append('2')

        #各グレードレースへの出場経験を確認する
        for racename in horse_info_data_frame['レース名']:
            if ('(G3)' in racename):
                if('ユニコーン' in racename or
                   'レパード' in racename):
                    g3_age3.append(1)
                    g3_age4.append(0)
                else:
                    g3_age3.append(0)
                    g3_age4.append(1)
            else:
                g3_age3.append(0)
                g3_age4.append(0)                

            if ('(G2)' in racename):
                if('関東オークス' in racename or
                   '兵庫チャンピョン' in racename):
                    g2_age3.append(1)
                    g2_age4.append(0)
                else:
                    g2_age3.append(0)
                    g2_age4.append(1)
            else:
                g2_age3.append(0)
                g2_age4.append(0)                      

            if ('(G1)' in racename):
                if('ジャパンダートダ' in racename):
                    g1_age3.append(1)
                    g1_age4.append(0)
                else:
                    g1_age3.append(0)
                    g1_age4.append(1)   
            else:
                g1_age3.append(0)
                g1_age4.append(0) 

        for tmp2_dirt_or_grass in horse_info_data_frame['距離']:
            length = tmp2_dirt_or_grass[1:]
            distance.append(length)


        for tmp2_dirt_or_grass in horse_info_data_frame['馬場']:
            condition_mapping={'良':4,'稍':3,'重':2,'不':1}
            tmp_condition = condition_mapping[tmp2_dirt_or_grass]
            condition.append(tmp_condition)


        for tmp_furlong in horse_info_data_frame['上り']:
            furlong3.append(tmp_furlong)

        for tmp_money in horse_info_data_frame['賞金']:
            tmp2_money = tmp_money
            if math.isnan(tmp_money):
                tmp2_money = 0.0
            #money_split_list = tmp_money.split(',.')
            #if(len(money_split_list)==2):
            #    money_num = int(money_split_list[0])
            #else:
            #    money_num = int(money_split_list[0])*1000 + int(money_split_list[1])
            money.append(tmp2_money)
        #調教師を追加したい→転厩の可能性があるので、ここでアペンド
        #オーナーを追加したい→別ファイル


        #各レース情報を別で引っ張ってくる
        for num in range(len(date)):
            hasraceinfo = True
            tmp = date[num].split('/')
            #print(type(tmp[0]))

            dateforda.append(getDateForDataAnalysis(int(tmp[0]),int(tmp[1]),int(tmp[2])))
            dateforda

            if len(place[num]) == 3  :
                if(place[num] =='韓国'):
                        tmp_racetrack = racetrack_mappings['韓国']

            if len(place[num]) == 3  :
                if(place[num] =='ソウル'):
                        tmp_racetrack = racetrack_mappings['ソウル']
                elif(place[num] =='名古屋'):
                        tmp_racetrack = racetrack_mappings['名古屋']

                else:
                    tmp_racetrack = racetrack_mappings[place[num][1:3]]
            elif len(place[num]) == 4 or len(place[num]) == 5  :
                if(place[num] =='メイダン'):
                        tmp_racetrack = racetrack_mappings['メイダン']
                elif(place[num] =='キングア'):
                        tmp_racetrack = racetrack_mappings['キングア']
                elif(place[num] =='チャーチ'):
                        tmp_racetrack = racetrack_mappings['チャーチ']
                elif(place[num] =='アラブ首'):
                        tmp_racetrack = racetrack_mappings['アラブ首']

                else:
                    tmp_racetrack = racetrack_mappings[place[num][1:3]]
            else :
                tmp_racetrack = racetrack_mappings[place[num]]

            tmp_place =str(tmp_racetrack)
            #print(tmp_place)
            #print(type(race_num[num]))

            print(tmp_racetrack)
            if tmp_racetrack > 10 and tmp_racetrack <= 100   :
                tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                race_id = tmp[0]+str(tmp_day)+tmp[1]+tmp[2] + str(race_num[num])#年+開催+月日
            elif tmp_racetrack > 100:
                if(tmp_racetrack == 101):
                    #メイダン
                    tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                    race_id = tmp[0]+"J0"+tmp[1]+tmp[2] + str(race_num[num])#年+開催+月日                    
                if(tmp_racetrack == 102):
                    #キングア
                    tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                    race_id = tmp[0]+"P0a00108"#年+開催+月日
                if(tmp_racetrack == 103 or tmp_racetrack == 106):
                    #ソウル
                    tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                    race_id = tmp[0]+"K0"+tmp[1]+tmp[2] + str(race_num[num])#年+開催+月日
                if(tmp_racetrack == 104):
                    #チャーチ
                    tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                    race_id = tmp[0]+"F0"+tmp[1]+tmp[2] + str(race_num[num])#年+開催+月日
                if(tmp_racetrack == 105):
                    #チャーチ
                    tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                    race_id = tmp[0]+"C700704"#年+開催+月日                    
            else:
                tmp_day       = str(tmp_racetrack) if   tmp_racetrack >= 10 else "0" +   str(tmp_racetrack)
                tmp_kaisai    = int(place[num][0])
                if len(place[num]) == 4:
                    tmp_week      = int(place[num][3])
                elif len(place[num]) == 5:
                    tmp_week      = int(place[num][3:5])

                tmp_kaisai    = str(tmp_kaisai) if  tmp_kaisai >= 10 else "0" +  str(tmp_kaisai)
                tmp_week      = str(tmp_week) if  tmp_week >= 10 else "0" +  str(tmp_week)
                tmp_race      = str(race_num[num]) if  int(race_num[num]) >= 10 else "0" +  str(race_num[num])

                race_id = tmp[0]+str(tmp_day)+str(tmp_kaisai)+(tmp_week) + str(tmp_race)#年+開催+週　回

            race_info_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/race_id/' + str(race_id) +'.csv'
            is_file = os.path.isfile(race_info_path)
            if is_file:
                print(race_id+":file exists")
            else:
                print(race_id+":file not exists")


                if tmp_racetrack <= 10:
                    race_info_data_frame = getRaceResultJRA(int(tmp[0]),int(tmp[1]),int(tmp[2]),race_num[num],racetrack_mappings[place[num][1:3]],int(tmp_kaisai),int(tmp_week))
                else:
                    race_info_data_frame = getRaceResultLocal(int(tmp[0]),int(tmp[1]),int(tmp[2]),race_num[num],racetrack_mappings[place[num]])


                #if isinstance(race_info_data_frame,list) and not race_info_data_frame :continue
                try:
                    race_info_data_frame.to_csv(race_info_path) 
                except:
                    hasraceinfo = False

            is_file = os.path.isfile(race_info_path)
            if is_file == True:
                race_info_data_frame = pd.read_csv(race_info_path)
                hoge = horse_num[num]
                tmp_each_race_df = race_info_data_frame.query('馬番 == @hoge')
                print(tmp_each_race_df)
            else:
                hasraceinfo = False
            #print(race_info_data_frame)

            if hasraceinfo == False:
                sex.append('0')
                age.append('0')
                #date.append('0')
                track.append('0')
                #weather.append('0')
                #horse_race_anim.append('0')
                #horse_num.append('0')
                odds.append('0')

                popularity.append('0')
                order.append('0')
                jockey.append('0')
                weight.append('0')
                #dirt_grass.append('0')
                #distance.append('0')
                #condition.append('0')
                time.append('0')
                #furlong3.append('0')
                horse_weight.append('0')
                weight_incdec.append('0')

            else:
                print(tmp_each_race_df['性齢'].values[0])
                tmp_sex = tmp_each_race_df['性齢'].values[0][0]
                if(tmp_sex == '牡'):
                    sex.append('3')
                elif(tmp_sex == '牝'):
                    sex.append('1')
                elif(tmp_sex == 'セ'):
                    sex.append('2')
                elif(tmp_sex == '牡'):
                    sex.append('0')

                tmp_age = tmp_each_race_df['性齢'].values[0][1:]
                age.append(tmp_age)


                tmp_track = tmp_racetrack
                track.append(tmp_track)

                #weather_mapping={'晴':4,'曇':3,'小雨':2,'雨':1}
                #tmp_weather = weather_mapping[tmp_each_race_df['天気']]
                #weather.append(tmp_weather)

                #tmp_race_num = tmp_each_race_df['R']
                #race_num.append(tmp_race_num)

                #tmp_horse_race_anim = tmp_each_race_df['頭数']
                #horse_race_anim.append(tmp_horse_race_anim)

                tmp_odds = tmp_each_race_df['単勝'].values[0]
                print(tmp_odds)
                odds.append(tmp_odds)

                tmp_horse_race_anim = tmp_each_race_df['人気'].values[0]
                popularity.append(tmp_horse_race_anim)

                tmp_order = str(tmp_each_race_df['着順'].values[0]).split('(')
                tmp2_order = int(tmp_order[0])
                tmp3_order      = '1' if  tmp2_order <= 1 else "0"
                order.append(tmp3_order)

                tmp2_jockey = tmp_each_race_df['騎手'].values[0]
                print(type(tmp2_jockey))
                try:
                    tmp_jockey = jockey_mappings[tmp2_jockey]
                except:
                    tmp_jockey = 0

                jockey.append(tmp_jockey)

                tmp_weight = tmp_each_race_df['斤量'].values[0]
                weight.append(tmp_weight)

                #tmp_dirt_or_grass = tmp_each_race_df.at[0,'距離'][0]
                #if(tmp_dirt_or_grass=='芝'):
                #    dirt_grass.append('1')
                #else:
                #    dirt_grass.append('2')
                
                #tmp_distance = tmp_dirt_or_grass = tmp_each_race_df.at[0,'距離'][1:]
                #distance.append(tmp_distance)
                
                #condition_mapping={'良':4,'稍':3,'重':2,'不良':1}
                #tmp_condition = condition_mapping[tmp_each_race_df.loc[0,'馬場']]
                #condition.append(tmp_condition)
                
                tmp_time = tmp_each_race_df['タイム'].values[0]
                print("time:"+tmp_time[2:4])
                tmp2_condition = str(int(tmp_time[0])*60+int(tmp_time[2:4]))+"."+tmp_time[5]
                time.append(tmp2_condition)
                
                #tmp_furlong = tmp_each_race_df['上り'].values[0]
                #furlong3.append(tmp_furlong)
                
                tmp_horse_weight = tmp_each_race_df['馬体重'].values[0][0:3]
                print(type(tmp_horse_weight))
                horse_weight.append(tmp_horse_weight)
                
                tmp_weight_incdec = tmp_each_race_df['馬体重'].values[0][3:]
                if(len(tmp_weight_incdec)==3):
                    weight_incdec.append('0')
                elif(len(tmp_weight_incdec)==4):
                    weight_incdec.append(str(int(tmp_weight_incdec[1:3])))
                elif(len(tmp_weight_incdec)==5):
                    weight_incdec.append(str(int(tmp_weight_incdec[1:4])))

        #print(distance)
        horse_info_data_frame2 = pd.DataFrame()
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'horse_id',horse_id_set)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'sex', sex)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'age', age)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'date', date)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'dateforda', dateforda)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'track', track)        
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'weather', weather)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'race_num', race_num)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'horse_num_anim', horse_race_anim)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'horse_num', horse_num)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'odds', odds)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'popularity', popularity)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'order', order)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'jockey', jockey)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'weight', weight)
        #print(dirt_grass)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'dirt_grass', dirt_grass)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'distance', distance)
        loc = loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'condition', condition)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'time', time)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, '3furlong', furlong3)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'horse_weight', horse_weight)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'weight_incdec', weight_incdec)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'same_track', same_track)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'g1_age3', g1_age3)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'g2_age3', g2_age3)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'g3_age3', g3_age3)        
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'g1_age4', g1_age4)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'g2_age4', g2_age4)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'g3_age4', g2_age4)
        loc = len(horse_info_data_frame2.columns)
        horse_info_data_frame2.insert(loc, 'money',  money)

        print("---")
        print(horse_info_data_frame)
        print("---")

        print(horse_info_data_frame2)
        horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/' + str(horse_id) +'.csv'
        horse_info_data_frame2.to_csv(horse_info_new_path)

        count = 0
        #print(horse_info_data_frame2.iloc[0:5,:])

        counter = 0

        for index in range (0,len(horse_info_data_frame2)):
            findIndex = False
            hoge2 = horse_info_data_frame2.iloc[index,3]
            print(hoge2)
            #
            if hoge2  == OBJECT_DAY or FORCE_BREAK == True:
                findIndex = True
                break
            else:
                counter = counter +1

        if findIndex == False:
            counter=0
            counter_last_5 = counter
            counter_last5_plus_5 = counter_last_5 + 5
        else:
            counter_last_5 = counter + 1
            counter_last5_plus_5 = counter_last_5 + 5

        print('---------------train_data---------------')
        print(horse_info_data_frame2.iloc[counter_last_5:counter_last5_plus_5,:])
        print('---------------end_train_data-----------')

        print('---------------test_data---------------')
        print(horse_info_data_frame2.iloc[counter:counter+1,:])
        print('---------------end_test_data-----------')

        #訓練データ
        teiou_train_2023_df = teiou_train_2023_df.append(horse_info_data_frame2.iloc[counter_last_5:counter_last5_plus_5,:])
        horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+ 'train_' + str(race_id) +'.csv'
        horse_info_data_frame2.iloc[counter_last_5:counter_last5_plus_5,:].to_csv(horse_info_new_path)


        #テストデータ
        if findIndex == True:
            horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+ 'test_' + str(race_id) +'.csv'
            horse_info_data_frame2.iloc[counter:counter+1,:].to_csv(horse_info_new_path)
            teiou_test_2023_df = teiou_test_2023_df.append(horse_info_data_frame2.iloc[counter:counter+1,:])
        else:
            print("test data not made")

        jbc_counter = jbc_counter + 1

    horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+'train_'+RACE_NAME+'.csv'
    teiou_train_2023_df.to_csv(horse_info_new_path)

    if(teiou_test_2023_df.empty != True):
        horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+'test_'+RACE_NAME+'.csv'
        teiou_test_2023_df.to_csv(horse_info_new_path)


if __name__ == "__main__":
    main()
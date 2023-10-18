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
from horserace_util import getRaceResultLocal,getRaceResultJRA, getHorseInfo
from jockeytable import jockey_mappings

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



def main():
    print("start")

    df = pd.DataFrame()

    horse_id_list_18 = [
        2013104055,
        2015104273,
        2014103385,
        2012104314,
        2010102446,
        2011104994,
        2015100122,
        2013101861,
        2011104995,
        2012104367,
        #2012104019,
        #2013103863,
        #2012110098,
        #2012101830,
        #2010104098,
        #2011104326,
    ]


    horse_id_list_JBC19 = [
        2015104879,
        2015104273,
        2012104019,
        2013104246,
        2013109025,
        2015105608,
        2015102374,
        2014106448,
        2011104326,
        #2016105664,
        #2011105236,
    ]

    #金沢
    horse_id_list_JBC2021 = [
                     2016100981,
                     2015104273,
                     2015104879,
                     2017101010,
                     2013104055,
                     2016104163,
                     2017105292,
                     2015100122,
                     2015103370,
                     2017106443,
                     2016101955,
                     2017105956,
                     ]

    #盛岡
    horse_id_list_JBC2022 = [
                     2017101010,
                     2019104678,
                     2019104245,
                     2018101012,
                     2017106404,
                     2016101455,
                     2019105656,
                     2018104033,
                     2018106265,
                     2017102025,
                     2014104735,
                     2013101965,
                     2016105316,
                     2016103323,
                     2017102571,
                     ]

    #大井
    horse_id_list_JBC2020 = [
        2016104458,
        2015104273,
        2015104879,
        2016100981,
        2017105292,
        2016103957,
        2015102390,
        2015105868,
        2010102446,
        2012104314,
        2012104019,
        2013104755,
        2015102946,
        2012100627,
        2012104678,
    ]

    #2019_帝王賞
    horse_id_list_teiou_2019 = [
        2015104273,
        2015104879,
        2012104314,
        2012101502,
        2015105676,
        2014104052,
        2010102446,
        2011101738,
        2012104367,
        2013104755,
        2014104469,
        2013104508,
        2012110098,
        2011104326,
    ]

    #2020_帝王賞
    horse_id_list_teiou_2020 = [
        2016104458,
        2015104273,
        2015104879,
        2016106260,
        2012104314,
        2013104055,
        2012101502,
        2013109025,
        2013104755,
        2015104189,
        2016100661,
        2014104582,
        2015105676,
        2015102249,
    ]

    #2021_帝王賞
    horse_id_list_teiou_2021 = [
        2017101010,
        2012104314,
        2014100656,
        2016100981,
        2015104273,
        2015104879,
        2016101455,
        2016104426,
        2017105292,
        2016104163,
        2016100661,
        2017103550,
        2015102249,
    ]

    #2022_帝王賞
    horse_id_list_teiou_2022 = [
        2017106404,
        2015104879,
        2015104273,
        2014100656,
        2017101010,
        2012104314,
        2015104526,
        2016101055,
        2016101455,
    ]

    #2023_帝王賞→どうなるか学習したい
    horse_id_list_teiou_2023 = [
        2017106404,
        2019104678,
        2017101010,
        2017103290,
        2017101184,
        2017105395,
        2017105396,
        2019101623,
        2019103502,
        2018103811,
        2017109038,
        2016101455,

    ]

    #2013東京大賞典
    horse_id_list_2013_daishouten =[
        2009100921,
        2006106794,
        2007100191,
        2010110052,
        2006106201,
        2008102944,
        2009102405,
        2006100953,
        2006103167,
    ]

    #2014東京大賞典
    horse_id_list_2014_daishouten =[
        2009100921,
        2010106548,
        2008101041,
        2011102947,
        2008102944,
        2007103394,
        2006106794,
        2010104098,
        2009102405,
        2005103453,
        2006106156,
        2008105433,
        2010103370,
        2006100953,
        2010100898,
        #000a0127d6,
    ]

    #2015東京大賞典
    horse_id_list_2015_daishouten =[
        2010102446,
        2009100921,
        2006106794,
        2010106548,
        2009102179,
        2011102947,
        2007103864,
        2008101041,
        2010104996,
        2009105650,
        2009102405,
        2009103308,
        2009103120,
        2010100266,
    ]

    #2016東京大賞典
    horse_id_list_2016_daishouten =[
        2012110098,
        2010110078,
        2010102446,
        2012104314,
        2010106548,
        2012101974,
        2011102128,
        2011102947,
        2013105190,
        2009104054,
        2012106362,
        2008102828,
        2011102186,
        2010104087,
    ]


    #2017東京大賞典
    horse_id_list_2017_daishouten =[
        2010106548,
        2010102446,
        2013104055,
        2012110098,
        2013101999,
        2012101502,
        2010104916,
        2014104453,
        2013105053,
        2013104755,
        2013100291,
        2014106418,
        2013105190,
        2013101922,
        2009110017,
        2008102895,
    ]

    #2018東京大賞典
    horse_id_list_2018_daishouten =[
        2015104273,
        2013106119,
        2013104055,
        2010102446,
        2015102979,
        2014104469,
        2015105608,
        2011102464,
        2015105676,
        2012110098,
        2010104098,
        2015102249,
        2011102489,
        2010105981,
        #2014101639,
        2014100688,
    ]

    #2019東京大賞典
    horse_id_list_2019_daishouten =[
        2015104273,
        2012104314,
        2015105676,
        2013106119,
        2015102374,
        2014103477,
        2013100291,
        2013104055,
        2015110103,
        2013105190,
        2013109093,
        2008200010,
        2013101999,
    ]

    #2020東京大賞典
    horse_id_list_2020_daishouten =[
        2015104273,
        2016104163,
        2012104882,
        2014102787,
        2016100981,
        2017101010,
        2013103324,
        2016103957,
        2015105676,
        2015105608,
        2012104314,
        2017105292,
        2014100629,
        2015100106,
        2013105471,
        2014103284,
    ]

    #2021東京大賞典
    horse_id_list_2021_daishouten =[
        2015104273,
        2014100656,
        2012104882,
        2016100981,
        2016102276,
        2014104259,
        2013105053,
        2014106474,
        2016103957,
        2012104314,
        2018105679,
        2014100629,
        2018103898,
        2014103284,
        2015103370,

    ]

    #2022東京大賞典
    horse_id_list_2022_daishouten =[
        2017103843,
        2019101623,
        2017106404,
        2017100988,
        2017105395,
        2017100024,
        2018104021,
        2017103602,
        2019103502,
        2016104163,
        2017109038,
        2015104417,
        2016106602,
        2016105093,
    ]

    #2021川崎記念
    horse_id_list_2021_kawasaki =[
        2016104163,
        2015104273,
        2017105292,
        2013105053,
        2016100981,
        2016102276,
        2016103957,
        2013103324,
        2010106550,
    ]

    #2022川崎記念
    horse_id_list_2022_kawasaki =[
        2015104879,
        2014105850,
        2017105356,
        2018104059,
        2016104163,
        2017104867,
        2016103957,
        2015102374,
        2014109171,
        2014104332,
        2013104055,
        2015102249,
    ]

    #2023川崎記念
    horse_id_list_2023_kawasaki =[
        2017103843,
        2017101010,
        2016105885,
        2017103942,
        2017105395,
        2015104526,
        2019104245,
        2019101623,
        2014105850,
        2018103756,
    ]

    #2022チャンピョンズカップ
    horse_id_list_2020_championscup =[
        2015104879,
        2013106119,
        2014104052,
        2016104458,
        2014110031,
        2017110151,
        2013105399,
        2015104107,
        2015100318,
        2015110086,
        2014100656,
        2014106474,
        2014104259,
        2013106094,
        2015103248,
        2013103671,
    ]
    #2022チャンピョンズカップ
    horse_id_list_2021_championscup =[
        2017101010,
        2015104879,
        2014104259,
        2014104052,
        2014106474,
        2016101455,
        2017106404,
        2015104526,
        2013105399,
        2016104163,
        2017110151,
        2018105233,
        2013104055,
        2014100656,
        2017100988,
        2017105292,
    ]

    #2022チャンピョンズカップ
    horse_id_list_2022_championscup =[
        2017105396,
        2019104678,
        2019100630,
        2017101010,
        2018103528,
        2017100988,
        2016100617,
        2019101623,
        2016101455,
        2017101719,
        2015104417,
        2018105251,
        2015105868,
        2014106474,
        2018105365,
    ]


    OBJECT_DAY = "2020/12/06"
    RACE_NAME  = "CHAMPIONSCUP_2020"
    horse_id_list = horse_id_list_2020_championscup

    teiou_2023_df = pd.DataFrame()

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
        place        =[]#後でtrackに変える
        track        =[]#後でtrackに変える
        weather      =[]#
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

        #レースから照合するためのパラメータを取得
        for tmp_place in horse_info_data_frame['開催']:
            horse_id_set.append(horse_id)

        for tmp_place in horse_info_data_frame['開催']:
            place.append(tmp_place)

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

        for tmp2_dirt_or_grass in horse_info_data_frame['距離']:
            tmp_dirt_or_grass = tmp2_dirt_or_grass[1:]
            distance.append(tmp_dirt_or_grass)


        for tmp2_dirt_or_grass in horse_info_data_frame['馬場']:
            condition_mapping={'良':4,'稍':3,'重':2,'不':1}
            tmp_condition = condition_mapping[tmp2_dirt_or_grass]
            condition.append(tmp_condition)


        for tmp_furlong in horse_info_data_frame['上り']:
            furlong3.append(tmp_furlong)


        #調教師を追加したい→転厩の可能性があるので、ここでアペンド
        #オーナーを追加したい→別ファイル

        for num in range(len(date)):
            hasraceinfo = True
            tmp = date[num].split('/')
            print(type(tmp[0]))

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
                tmp_race      = str(race_num[num]) if  race_num[num] >= 10 else "0" +  str(race_num[num])

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
                    sex.append('1')
                elif(tmp_sex == '牝'):
                    sex.append('2')
                elif(tmp_sex == 'セ'):
                    sex.append('3')
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

                tmp_order = tmp_each_race_df['着順'].values[0]
                order.append(tmp_order)

                tmp2_jockey = tmp_each_race_df['騎手'].values[0]
                print(type(tmp2_jockey))
                tmp_jockey = jockey_mappings[tmp2_jockey]
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
            hoge2 = horse_info_data_frame2.iloc[index,3]
            print(hoge2)
            if hoge2  == OBJECT_DAY:
                break
            else:
                counter = counter +1

        counter_plus_5 = counter + 5

        print(horse_info_data_frame2.iloc[counter:counter_plus_5,:])


        if(teiou_2023_df.empty == False):
            teiou_2023_df = teiou_2023_df.append(horse_info_data_frame2.iloc[counter:counter_plus_5,:])
        else:
            teiou_2023_df = horse_info_data_frame2.iloc[counter:counter_plus_5,:]

        horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/' + str(race_id) +'.csv'
        horse_info_data_frame2.iloc[counter:counter_plus_5,:].to_csv(horse_info_new_path)

        jbc_counter = jbc_counter + 1

    horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+RACE_NAME+'.csv'
    teiou_2023_df.to_csv(horse_info_new_path)


if __name__ == "__main__":
    main()
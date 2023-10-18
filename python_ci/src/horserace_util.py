import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re
import urllib.request, urllib.error
from tqdm import tqdm
import datetime

#非ライブラリ
from racetable import object_this_year_race
from object_horse import Horse
from horsetable import horse_mappings
from racetrack import racetrack_mappings

def convertFromHorseNameToHorseID(horsename):
    for key, value in horse_mappings.items():
        if key == horsename:
            return value

    return 0

def convertFromHorsePlaceIdToHorsePlace(place):
    for key, value in racetrack_mappings.items():
        if value == place:
            return key

    return 0

def checkURL(url):
    isUrlOk = False
    try:
        f = urllib.request.urlopen(url)
        isUrlOk = True
        f.close()
    except:
        isUrlOk = False
    
    return isUrlOk 

def getHorseURL(horse_num):
    url = "https://db.netkeiba.com/horse/" + horse_num

    return url

def getRaceURL(race_num):
    url = "https://db.netkeiba.com/race/" + race_num

    return url

def getHorseInfo(horse_id):
    this_horse_id   = ''
    tmp_horse_id  = str(horse_id)
    this_horse_id =  tmp_horse_id

    #print(this_horse_id)

    url = getHorseURL(this_horse_id)

    race_request = requests.get(url)
    race_request.encoding = "EUC-JP"

    try:
        race_results_data_frame = pd.read_html(url)[3]
        #受賞歴があると[3]に受賞歴が入るので[4]にする
        if race_results_data_frame.columns[0]=='受賞歴':
            race_results_data_frame = pd.read_html(url)[4]
    except:
        #print("race has not exist")
        race_results_data_frame = []    
        hoge = False
    
    #print(self.race_results_data_frame)

    time.sleep(0.1)

    return race_results_data_frame

def getRaceResultJRA(year,month,day,race_num,place_num,kai,week):
    race_id   = ''
    tmp_year      = str(year)
    tmp_month     = str(month) if month >= 10 else "0" + str(month)
    tmp_day       = str(day) if   day >= 10 else "0" +   str(day)
    tmp_kai     = str(kai) if kai >= 10 else "0" + str(kai)
    tmp_week       = str(week) if   week >= 10 else "0" +   str(week)
    tmp_race      = str(race_num) if  race_num >= 10 else "0" +  str(race_num)
    tmp_place_num = str(place_num) if  place_num >= 10 else "0" +  str(place_num)
    race_id= tmp_year + tmp_place_num + tmp_kai + tmp_week + tmp_race
    tmp_date = tmp_year + "/" + tmp_month + "/" + tmp_day
    print(race_id)
    url= getRaceURL(race_id)

    #print(url)

    race_results_data_frame = []
    isDataExists = True
    try:
        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

    except requests.exceptions.RequestException as e:
        #1回だけリトライ
        print(f"Error:{e}")
        print("Retrying in 10 seconds...")
        time.sleep(1)
        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

    #サーバー負荷対策でスリープを入れる
    time.sleep(0.1)
    
    if(race_request):
        try:
            race_results_data_frame = pd.read_html(url)[0]
            hoge=True
        except:
            print("race has not exist")
            race_results_data_frame = []    
            hoge = False

    print('------------------------------------------')
    print(race_results_data_frame)
    print('------------------------------------------')

    return race_results_data_frame


def getRaceResultLocal(year,month,day,race_num,place_num):
    race_id   = ''
    tmp_year      = str(year)
    tmp_month     = str(month) if month >= 10 else "0" + str(month)
    tmp_day       = str(day) if   day >= 10 else "0" +   str(day)
    tmp_race      = str(int(race_num)) if  race_num >= 10 else "0" +  str(race_num)
    tmp_place_num = str(place_num) if  place_num >= 10 else "0" +  str(place_num)
    if tmp_place_num == '101':
        tmp_place_num = 'J0'

    race_id= tmp_year + tmp_place_num + tmp_month + tmp_day + tmp_race
    tmp_date = tmp_year + "/" + tmp_month + "/" + tmp_day
    print(race_id)
    url= getRaceURL(race_id)

    #print(url)

    race_results_data_frame = []

    print('------------------------------------------')
    print(race_results_data_frame)
    print('------------------------------------------')

    try:
        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

    except requests.exceptions.RequestException as e:
        #1回だけリトライ
        print(f"Error:{e}")
        print("Retrying in 10 seconds...")
        time.sleep(1)
        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

    #サーバー負荷対策でスリープを入れる
    time.sleep(0.1)
    
    if(race_request):
        try:
            race_results_data_frame = pd.read_html(url)[0]
        except:
            print("race has not exist")
            race_results_data_frame = []   

    return race_results_data_frame

def getThisYearRace():    
    for horse_num in object_this_year_race:
        df_ = pd.DataFrame()
        horse = Horse(horse_num[0],horse_num[1])
        horse.initializeHorse()
        list = horse.makeDataFrame(False, 1)
        df_ = df_.append(list, ignore_index=True)
        print(horse_num[0])
        print(df_)



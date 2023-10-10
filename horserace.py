import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re
import urllib.request, urllib.error
from tqdm import tqdm

#非ライブラリ
from racetable import object_race, object_this_year_race
from jockeytable import jockey_mappings

year_start = 2023
year_end   = 2024

def checkURL(url):
    isUrlOk = False
    try:
        f = urllib.request.urlopen(url)
        isUrlOk = True
        f.close()
    except:
        isUrlOk = False
    
    return isUrlOk 



class Horse():
    def __init__(self,horse_num,sex,age,race_date):
        self.horse_num = horse_num
        self.age       = age
        self.sex       = sex
        self.race_date = race_date
        #self.race_results_data_frame = []
        #self.trainerandhouseowner = []

    def setYearMonthDay(self,race_date):
        tmp = self.race_date.split('/')
        self.year  = int(tmp[0])
        self.month = int(tmp[1])
        self.day   = int(tmp[2])

    def setTrainerAndHorseOwner(self):
        url = getURL(self.horse_num)

        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

        self.trainerandhouseowner = pd.read_html(url)[1]

    def setHorseResult(self):
        url = getURL(self.horse_num)

        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

        self.race_results_data_frame = pd.read_html(url)[3]
        #受賞歴があると[3]に受賞歴が入るので[4]にする
        if self.race_results_data_frame.columns[0]=='受賞歴':
            self.race_results_data_frame = pd.read_html(url)[4]
        #print(self.race_results_data_frame)

    def getIndex(self):
        self.index = self.race_results_data_frame.index
        for index in self.index:
            tmp = self.race_results_data_frame.iat[index,0].split('/')
            #print(self.race_results_data_frame)
            year  = int(tmp[0])
            month = int(tmp[1])
            day   = int(tmp[2])
            if(year<=self.year and month <= self.month and day <= self.day):
                print(index)
                return index

    def initializeHorse(self):
        self.setTrainerAndHorseOwner()
        self.setHorseResult()
        self.setYearMonthDay(self.race_date)

    def getSex(self):
        sex_and_birth = self.sex
        if("牡" in sex_and_birth):
            return "1"
        elif("牝" in sex_and_birth):
            return "2"
        elif("セ" in sex_and_birth):
            return "3"
        else:
            return "0"

    def getAge(self):
        return self.age

    def getDate(self,index):
        return self.race_results_data_frame.iat[index,0]
    
    def getPlace(self,index):
        mappings = {'札幌':1,'門別':30,'盛岡':35, '浦和': 42, '船橋': 43, '大井': 44, '川崎':45}

        for key, value in mappings.items():
            if key in self.race_results_data_frame.iat[index,1]:
                return str(value)
        return "0"

    def getWeather(self,index):
        mappings = {'晴':4, '曇': 3, '小雨': 2, '雨': 1}

        for key, value in mappings.items():
            if key in self.race_results_data_frame.iat[index,2]:
                return str(value)
        return "0"

    def getRaceNum(self,index):
        return str(self.race_results_data_frame.iat[index,3])

    def getHorseNum(self,index):
        return str(self.race_results_data_frame.iat[index,8])

    def getOdds(self,index):
        return str(self.race_results_data_frame.iat[index,9])
    
    def getPopularity(self,index):
        return str(self.race_results_data_frame.iat[index,10])    

    def getResult(self,index):
        return str(self.race_results_data_frame.iat[index,11])

    def getJockey(self,index):
        for key, value in jockey_mappings.items():
            if key in self.race_results_data_frame.iat[index,12]:
                return str(value)
        return "0"

    def getWeight(self,index):
        return str(self.race_results_data_frame.iat[index,13])

    def getDirtOrGrass(self,index):
        tmp = self.race_results_data_frame.iat[index,14]
        sex_and_birth = tmp[0]
        if("芝" in sex_and_birth):
            return "1"
        elif("ダ" in sex_and_birth):
            return "2"
        else:
            return "0"

    def getDistance(self,index):
        tmp = self.race_results_data_frame.iat[index,14]
        return str(tmp[1:])

    def getRaceTrack(self,index):
        mappings = {'良':4, '稍': 3, '重': 2, '不良': 1,'不': 1}

        for key, value in mappings.items():
            if key in self.race_results_data_frame.iat[index,15]:
                return str(value)
        return "0"

    def getTime(self,index):
        tmp = self.race_results_data_frame.iat[index,17]
  
        time = int(tmp[0]) * 60 + int(tmp[2:4]) + int(tmp[5]) * 0.1

        return str(time)

    def get3Farlong(self,index):
        return str(self.race_results_data_frame.iat[index,22])

    def getBodyWeight(self,index):
        weight = self.race_results_data_frame.iat[index,23]
        return str(weight[0:3])

    def getBodyWeightIncDec(self,index):
        tmp_weight = self.race_results_data_frame.iat[index,23]
        tmp_weight = tmp_weight[3:]
        tmp_len    = len(tmp_weight)
        
        #print(tmp_len)

        if(tmp_len==3):
            return str(tmp_weight[1:2])
        elif(tmp_len==4):
            return str(tmp_weight[1:3])
        elif(tmp_len==5):
            return str(tmp_weight[1:4])

    def getTrainer(self):
        return self.trainerandhouseowner.iat[1,1]#調教師

    def getHorseOwner(self):
        return self.trainerandhouseowner.iat[2,1]#馬主:
        
    def isValid(self,index):
        if(self.race_results_data_frame.iat[index,23] != '計不' and
           self.race_results_data_frame.iat[index,11] != '除'):
            return True    
        else:
            return False

    def debugPrintLatestRace(self):
        #print(self.race_results_data_frame.index)
        for index in self.race_results_data_frame.index:
            if(self.isValid(index) == True):
                print(self.getSex(),end=' , ')
                print(self.getAge(),end=' , ')
                print(self.getDate(index) + " ",end=' , ')
                print(self.getPlace(index) + " ",end=' , ')
                print(self.getWeather(index) + " ",end=' , ')
                print(self.getHorseNum(index) + " ",end=' , ')
                print(self.getResult(index) + " ",end=' , ')
                print(self.getJockey(index) + " ",end=' , ')
                print(self.getWeight(index) + " ",end=' , ')
                print(self.getDirtOrGrass(index) + " ",end=' , ')
                print(self.getDistance(index) + " ",end=' , ')
                print(self.getRaceTrack(index) + " ",end=' , ')
                print(self.getTime(index) + " ",end=' , ')
                print(self.get3Farlong(index) + " ",end=' , ')
                print(self.getBodyWeight(index) + " ",end=' , ')
                print(self.getBodyWeightIncDec(index) + " ",end=' , ')
                print(self.getTrainer() + " ",end=' , ')
                print(self.getHorseOwner())

    def debugPrintPickedRace(self):
        #print(self.race_results_data_frame.index)
        for index in self.race_results_data_frame.index:
            if(self.getDate(index) == self.race_date):
                print(self.getSex(),end=' , ')
                print(self.getAge(),end=' , ')
                print(self.getDate(index) + " ",end=' , ')
                print(self.getPlace(index) + " ",end=' , ')
                print(self.getWeather(index) + " ",end=' , ')
                print(self.getHorseNum(index) + " ",end=' , ')
                print(self.getResult(index) + " ",end=' , ')
                print(self.getJockey(index) + " ",end=' , ')
                print(self.getWeight(index) + " ",end=' , ')
                print(self.getDirtOrGrass(index) + " ",end=' , ')
                print(self.getDistance(index) + " ",end=' , ')
                print(self.getRaceTrack(index) + " ",end=' , ')
                print(self.getTime(index) + " ",end=' , ')
                print(self.get3Farlong(index) + " ",end=' , ')
                print(self.getBodyWeight(index) + " ",end=' , ')
                print(self.getBodyWeightIncDec(index))
                #print(self.getTrainer())
                #print(self.getHorseOwner())

    def makeDataFrame(self, fixday,last_race_num):
        #print(self.race_results_data_frame.index)

        counter = 0
        list_all = []
        for index  in self.race_results_data_frame.index:
            if(self.getDate(index) == self.race_date or fixday == False):
                if(self.isValid(index) == True):
                    list = []
                    list.append(float(self.getSex()))
                    list.append(float(self.getAge()))
                    #list.append(int(self.getDate(index)))
                    list.append(float(self.getPlace(index)))
                    list.append(float(self.getWeather(index)))
                    list.append(float(self.getRaceNum(index)))
                    list.append(float(self.getHorseNum(index)))
                    list.append(float(self.getOdds(index)))
                    list.append(float(self.getPopularity(index)))
                    list.append(float(self.getResult(index)))
                    list.append(float(self.getJockey(index)))
                    list.append(float(self.getWeight(index)))
                    list.append(float(self.getDirtOrGrass(index)))
                    list.append(float(self.getDistance(index)))
                    list.append(float(self.getRaceTrack(index)))
                    list.append(float(self.getTime(index)))
                    list.append(float(self.get3Farlong(index)))
                    list.append(float(self.getBodyWeight(index)))
                    list.append(float(self.getBodyWeightIncDec(index)))
                    #print(self.getTrainer())
                    #print(self.getHorseOwner())
                    list_all.append(list)
                    counter = counter + 1
                    if(counter >= last_race_num): break

        return list_all

    def makeHorseInfo(self, fixday):
        #print(self.race_results_data_frame.index)

        list_all = []
        for index  in self.race_results_data_frame.index:
            if(self.getDate(index) == self.race_date or fixday == False):
                if(self.isValid(index) == True):
                    list = []
                    list.append(float(self.getSex()))
                    list.append(float(self.getAge()))
                    #初競馬場か
                    #逃げ/先行/差し/追い込み
                    #重賞経験数
                    #
                    list.append(float(self.getRaceNum(index)))
                    list.append(float(self.getHorseNum(index)))
                    list.append(float(self.getOdds(index)))
                    list.append(float(self.getPopularity(index)))
                    list.append(float(self.getResult(index)))
                    list.append(float(self.getJockey(index)))
                    list.append(float(self.getWeight(index)))
                    list.append(float(self.getDirtOrGrass(index)))
                    list.append(float(self.getDistance(index)))
                    list.append(float(self.getRaceTrack(index)))
                    list.append(float(self.getTime(index)))
                    list.append(float(self.get3Farlong(index)))
                    list.append(float(self.getBodyWeight(index)))
                    list.append(float(self.getBodyWeightIncDec(index)))
                    #print(self.getTrainer())
                    #print(self.getHorseOwner())
                    list_all.append(list)

        return list_all




def getRaceResult(year,month,day,race_num,place_num):
    race_id   = ''
    tmp_month = str(month) if month >= 10 else "0" + str(month)
    tmp_day   =   str(day) if   day >= 10 else "0" +   str(day)
    tmp_race  =  str(race_num) if  race_num >= 10 else "0" +  str(race_num)
    race_id= str(year) + place_num + tmp_month + tmp_day +tmp_race
    url= "https://db.netkeiba.com/race/" + race_id
    #url= "https://db.netkeiba.com/race/202344091901"

    print(race_id)

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
    time.sleep(1)
    if(race_request):
        try:
            race_results_data_frame = pd.read_html(url)[0]
        except:
            print("race has not exist")
            race_results_data_frame = []    

    return race_results_data_frame

def getURL(horse_num):
    url = "https://db.netkeiba.com/horse/" + horse_num

    return url

def getThisYearRace():

    
    for horse_num in object_this_year_race:
        df_ = pd.DataFrame()
        horse = Horse(horse_num[0],"牡","2",horse_num[1])
        horse.initializeHorse()
        list = horse.makeDataFrame(False, 1)
        df_ = df_.append(list, ignore_index=True)
        print(horse_num[0])
        print(df_)

def getLast10YearRace():
    horse_nums        = [
                         ["2011105041","2013/10/09"],#ストーンリバー
                         ["2012103422","2014/10/15"],#ストーンリバー
                         ["2013103885","2015/10/21"],#ストーンリバー
                         ["2014101408","2016/10/05"],#ストーンリバー
                         ["2015102718","2017/10/11"],#リコーワルサー
                         ["2016100981","2018/10/17"],#ミューチャリー
                         ["2017106186","2019/10/22"],#リーチ
                         ["2018100548","2020/10/14"],#リーチ 
                         ["2019106611","2021/10/13"],#シルトプレ
                         ["2020104196","2022/10/12"],#ヒーローコール
                         ]
    
    df_ = pd.DataFrame()
    list_all = []
    list_label = ['sex','age','place','weather','recenum','horsenum','odds','popularity','result','jockey','weight','dirt','distance','track','time','farlong','bweight','incdec']
    list_all.append(list_label)
    df_ = df_.append(list_all, ignore_index=True)    
    for horse_num in horse_nums:
        horse = Horse(horse_num[0],"牡","2",horse_num[1])
        horse.initializeHorse()
        list = horse.makeDataFrame(True, 1)
        df_ = df_.append(list, ignore_index=True)

    print(df_)
    df_.to_csv("last10years.csv")

def getLast3YearRaceAllHorse():
    
    df_ = pd.DataFrame()
    list_all = []
    list_label = ['sex','age','place','weather','recenum','horsenum','odds','popularity','result','jockey','weight','dirt','distance','track','time','farlong','bweight','incdec']
    list_all.append(list_label)
    df_ = df_.append(list_all, ignore_index=True)    
    for horse_num in object_race:
        horse = Horse(horse_num[0],"牡","2",horse_num[1])
        horse.initializeHorse()
        list = horse.makeDataFrame(True, 1)
        df_ = df_.append(list, ignore_index=True)

    print(df_)
    df_.to_csv("last10years.csv")



def Wakamusha1st():
    horse_nums        = ["2021100888",
                         "2021100815",
                         "2021100316"
                         ]
    for horse_num in horse_nums:
        horse = Horse(horse_num,"牡","2","2022/10/12""2022/10/12")
        horse.initializeHorse()
        print(horse.debugPrintLatest())


def WakamushaLastTenYears():
    horse_nums        = ["2011105041",
                         "2011100434",
                         "2011100280",
                         ]
    for horse_num in horse_nums:
        horse = Horse(horse_num,"牡","2","2022/10/12")
        horse.initializeHorse()
        print(horse.debugPrintLatest())


#競馬場
#30:門別
#42:浦和
#43:船橋
#44:大井
#45:川崎

#川崎の例(2022年川崎05月18日6レース)
#202245051806
def main():

    #getLatestTenYearsRace()
    #getLast3YearRaceAllHorse()
    getThisYearRace()

def main2():
    print("start")

    year_start = 2023

    #getLatestTenYearsRace()

    for year in range(0,0):
        race_data_all = []
        race_data_all.append(['race_id','馬','騎手','馬番','走破時間','オッズ','通過順','着順','体重','体重変化','性','齢','斤量','上がり','人気','レース名','日付','開催','クラス','芝・ダート','距離','回り','馬場','天気','場id','場名'])

        num_place = ["30","42","43","44","45"]
        for w in range(len(num_place)):
            place = ""
            if num_place[w]=="30":
                place = "門別"
            elif num_place[w]=="42":
                place = "浦和"
            elif num_place[w]=="43":
                place = "船橋"
            elif num_place[w]=="44":
                place = "大井"
            elif num_place[w]=="45":
                place = "川崎"

            #print(place)

            race_id_list = []
            for month in range(9,9):
                #print(month)
                for day in range(1,32):
                    #print(day)
                    for race_num in range(1,13):
                        race_results_data_frame = getRaceResult(year,month,day,race_num,num_place[w])

                        # getSexAndBirth(race_results_data_frame)

                        #print(race_results_data_frame)

                        #race_results_data_frame = Results.scrape(race_id_list)

                        # レースから
                        # 着順   [0]   そのまま
                        # 枠番   [1]   そのまま
                        # 馬番   [2]   そのまま
                        # 馬名   [3]   そのまま
                        # 性齢   [4]   分割
                        # 斤量   [5]   そのまま
                        # 騎手   [6]   そのまま
                        # タイム [7]   そのまま
                        # 着差   [8]   そのまま（使わないかも）
                        # 単勝   [9]   そのまま
                        # 人気   [10]  そのまま
                        # 調教師 [11]  そのまま


                        
                        #print(race_results_data_frame)

if __name__ == "__main__":
    main()






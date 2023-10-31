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
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
print(str(Path(__file__).resolve().parent.parent))


from config.racetable import object_race, object_this_year_race
from config.jockeytable import jockey_mappings
#from config.horsetable import horse_mappings
from python_ci.scrape.src.core.racetrack import racetrack_mappings

def getHorseURL(horse_num):
    url = "https://db.netkeiba.com/horse/" + horse_num

    return url

def convertFromHorseNameToHorseID(horsename):
    for key, value in horse_mappings.items():
        if key == horsename:
            return value
    return 0

class Horse():

    def __init__(self,horse_name,sex,race_date):
        self.horse_num = convertFromHorseNameToHorseID(horse_name)
        self.sex       = sex
        self.race_date = race_date
        #self.race_results_data_frame = []
        #self.trainerandhouseowner = []
        assert self.horse_num == 0


    def setYearMonthDay(self):
        tmp = self.race_date.split('/')
        self.year  = int(tmp[0])
        self.month = int(tmp[1])
        self.day   = int(tmp[2])

    def setTrainerAndHorseOwner(self):
        url = getHorseURL(self.horse_num)

        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

        self.trainerandhouseowner = pd.read_html(url)[1]

    def setHorseResult(self):
        url = getHorseURL(self.horse_num)

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
        self.setYearMonthDay()

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

    def getCurrentAge(self):
        birth_tmp = self.trainerandhouseowner.iat[0,1]#生年月日
        birth_tmp = birth_tmp[0:4]

        year = datetime.date.today().year
        age = year - int(year)

        return age

    def getDate(self,index):
        return self.race_results_data_frame.iat[index,0]
    
    def getPlace(self,index):
        for key, value in racetrack_mappings.items():
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
                print(self.getCurrentAge(),end=' , ')
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
                print(self.getCurrentAge(),end=' , ')
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
                    list.append(float(self.getCurrentAge()))
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
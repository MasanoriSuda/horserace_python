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
from racetrack import racetrack_mappings
from horserace_util import getRaceResultLocal

def main():
    print("start")

    df = pd.DataFrame()

    #getLatestTenYearsRace()
    for year in range(2022,2024):
        #print(place)
        for month in range(1,13):
            #print(month)
            for day in range(1,32):
                #print(day)
                for key, value in racetrack_mappings.items():
                    for race_num in range(1,13):
                        race_results_data_frame = getRaceResultLocal(year,month,day,race_num,value)
                        if len(race_results_data_frame) != 0:
                            print(race_results_data_frame)                            

                            race_id   = ''
                            tmp_year      = str(year)
                            tmp_month     = str(month) if month >= 10 else "0" + str(month)
                            tmp_day       = str(day) if   day >= 10 else "0" +   str(day)
                            tmp_race      = str(race_num) if  race_num >= 10 else "0" +  str(race_num)
                            tmp_place_num = str(value)
                            race_id= tmp_year + tmp_place_num + tmp_month + tmp_day + tmp_race

                            path ="/home/msuda/workspace/vscode/horserace/python_ci/csv/race_id/" + race_id +".csv"
                            race_results_data_frame.to_csv(path)
                        else : break

if __name__ == "__main__":
    main()






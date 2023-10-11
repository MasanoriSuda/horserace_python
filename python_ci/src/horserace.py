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
from horserace_util import getRaceResult

def main():
    print("start")

    df = pd.DataFrame()

    #getLatestTenYearsRace()
    for year in range(2023,2024):
        #print(place)
        for month in range(1,2):
            #print(month)
            for day in range(1,8):
                #print(day)
                for key, value in racetrack_mappings.items():
                    for race_num in range(1,13):
                        race_results_data_frame = getRaceResult(year,month,day,race_num,value)
                        if len(race_results_data_frame) != 0:
                            print(race_results_data_frame)
                            df = pd.concat([df,race_results_data_frame])
                            

    df.to_csv("../csv/nankan_tmp.csv")

if __name__ == "__main__":
    main()






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
from horserace_util import getHorseInfo

def main():
    print("start")

    df = pd.DataFrame()

    #getLatestTenYearsRace()

    for year in range(2017,2011,-1):
        #print(place)
        counter = 0
        for horse_id in range(100000,119999):
            horse_info_data_frame = getHorseInfo(year,horse_id)
            if len(horse_info_data_frame) != 0:
                #print(horse_info_data_frame)                            

                this_horse_id   = ''
                tmp_year      = str(year)
                tmp_horse_id     = str(horse_id)
                this_horse_id = tmp_year + tmp_horse_id

                path ="/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id/" + this_horse_id +".csv"
                horse_info_data_frame.to_csv(path)
                print(this_horse_id)
                counter = 0
            else:
                counter = counter+1
                if counter >= 100:
                    break

if __name__ == "__main__":
    main()
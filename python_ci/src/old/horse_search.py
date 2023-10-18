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
from horserace_util import getRaceResultLocal
from racetrack import racetrack_mappings

def main():
    print("start")

    #getLatestTenYearsRace()
    for year in range(2020,2024):
        race_data_all = []
        #print(place)
        race_id_list = []
        for month in range(1,13):
            #print(month)
            for day in range(1,32):
                #print(day)
                for key, value in racetrack_mappings.items():
                    for race_num in range(1,13):
                        race_results_data_frame = getRaceResultLocal(year,month,day,race_num,value)
                        if len(race_results_data_frame) != 0:
                            print(race_results_data_frame)

if __name__ == "__main__":
    main()
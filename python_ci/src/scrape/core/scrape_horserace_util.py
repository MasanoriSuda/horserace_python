import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import re
import urllib.request, urllib.error
from tqdm import tqdm
import datetime

# 非ライブラリ
# from racetable import object_this_year_race
# from object_horse import Horse
# 自作ライブラリ
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
print(str(Path(__file__).resolve().parent.parent))

from core.scrape_racetrack import racetrack_mappings
from config.scrape_config_table import scrape_race_eval_list

# def convertFromHorseNameToHorseID(horsename):
#    for key, value in horse_mappings.items():
#        if key == horsename:
#            return value
#
#    return 0


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


def getDateForDataAnalysis(year, month, day):
    # Todo:暫定で日付を学習用に変更するパラメータ
    normalyear = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    normalyear = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    totalval = 1

    for tmp_year in range(2001, 2050):
        for tmp_month in range(1, 13):
            for tmp_day in range(1, 32):
                if year == tmp_year and month == tmp_month and day == tmp_day:
                    return totalval
                else:
                    totalval = totalval + 1

    return 0


def getHorseInfo(horse_id):
    this_horse_id = ""
    tmp_horse_id = str(horse_id)
    this_horse_id = tmp_horse_id

    # print(this_horse_id)

    url = getHorseURL(this_horse_id)

    race_request = requests.get(url)
    race_request.encoding = "EUC-JP"

    try:
        race_results_data_frame = pd.read_html(url)[3]
        # 受賞歴があると[3]に受賞歴が入るので[4]にする
        if race_results_data_frame.columns[0] == "受賞歴":
            race_results_data_frame = pd.read_html(url)[4]
    except:
        # print("race has not exist")
        race_results_data_frame = []
        hoge = False

    # print(self.race_results_data_frame)

    time.sleep(0.1)

    return race_results_data_frame


def getraceidforjra(year, month, day, race_num, place_num, kai, week):
    race_id = ""
    tmp_year = str(year)
    tmp_kai = str(kai) if kai >= 10 else "0" + str(kai)
    tmp_week = str(week) if week >= 10 else "0" + str(week)
    tmp_race = str(int(race_num)) if race_num >= 10 else "0" + str(int(race_num))
    tmp_place_num = str(place_num) if place_num >= 10 else "0" + str(place_num)
    race_id = tmp_year + tmp_place_num + tmp_kai + tmp_week + tmp_race

    assert len(race_id) == 12

    return race_id


def getRaceResultByRaceID(race_id):
    url = getRaceURL(race_id)
    race_results_data_frame = []

    try:
        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"

    except requests.exceptions.RequestException as e:
        # 1回だけリトライ
        print(f"Error:{e}")
        print("Retrying in 10 seconds...")
        time.sleep(0.1)
        race_request = requests.get(url)
        race_request.encoding = "EUC-JP"
        assert print("request err")
    # サーバー負荷対策でスリープを入れる
    time.sleep(0.1)

    if race_request:
        try:
            race_results_data_frame = pd.read_html(url)[0]
        except Exception as e:
            # Todo：例外発生時は以下で暫定対処する
            # https://teratail.com/questions/e069selc4rg5tn
            r = requests.get(url)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "lxml")

            # tr と td 要素を持つ table 要素のみをデータフレームに変換
            dfs = [pd.read_html(str(t))[0] for t in soup.select("table:has(tr td)")]

            print(dfs[0], end="\n\n")

            race_results_data_frame = dfs[0]
    return race_results_data_frame


def getRaceResultJRA(year, month, day, race_num, place_num, kai, week):
    race_id = getraceidforjra(year, month, day, race_num, place_num, kai, week)

    race_results_data_frame = getRaceResultByRaceID(race_id)

    return race_results_data_frame


def getraceidforlocal(year, month, day, race_num, place_num):
    race_id = ""
    tmp_year = str(year)
    tmp_month = str(month) if month >= 10 else "0" + str(month)
    tmp_day = str(day) if day >= 10 else "0" + str(day)
    tmp_race = str(int(race_num)) if race_num >= 10 else "0" + str(race_num)
    tmp_place_num = str(place_num) if place_num >= 10 else "0" + str(place_num)
    if tmp_place_num == "101":
        tmp_place_num = "J0"

    race_id = tmp_year + tmp_place_num + tmp_month + tmp_day + tmp_race

    assert len(race_id) == 12

    return race_id


def getRaceResultLocal(year, month, day, race_num, place_num):
    race_id = getraceidforlocal(year, month, day, race_num, place_num)

    race_results_data_frame = getRaceResultByRaceID(race_id)

    return race_results_data_frame


def getobjectraceinfo(race):
    return scrape_race_eval_list[race][1]

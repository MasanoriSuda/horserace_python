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

# 自作ライブラリ
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))
print("hoge")
print(str(Path(__file__).resolve().parent.parent.parent))
print(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

# 非ライブラリ
from python_ci.src.scrape.core.scrape_table_racetrack import racetrack_mappings
from python_ci.src.scrape.core.scrape_horserace_util import (
    getobjectraceinfo,
)
from python_ci.src.scrape.core.scrape_table_jockey import jockey_mappings

from python_ci.src.scrape.core.scrape_class_horse import Horse
from python_ci.src.scrape.core.scrape_class_race import Race

# from config.JBC2023.scrape_config_train_test_objectrace import scrape_config_horse_race_lists, scrape_config_racetrack
from python_ci.src.scrape.config.scrape_config_table import (
    scrape_race_eval_list,
    scrapeconfiggetobjectrace,
)


class HorseInteg:
    horse_id_set = []
    sex = []
    age = []
    date = []
    dateforda = []
    place = []
    track = []
    weather = []
    race_num = []
    horse_race_anim = []
    horse_num = []
    odds = []
    popularity = []
    order = []
    order_complex = []
    jockey = []
    weight = []
    dirt_grass = []
    distance = []
    condition = []
    time = []
    furlong3 = []
    horse_weight = []
    weight_incdec = []
    same_track = []
    g1_age3 = []
    g2_age3 = []
    g3_age3 = []
    g1_age4 = []
    g2_age4 = []
    g3_age4 = []
    money = []
    raceid_list = []
    sexage = []
    racename = []
    track_str = []

    labellists = [
        ["horse_id", horse_id_set],
        ["sex", sex],
        ["age", age],
        ["date", date],
        ["dateforda", dateforda],
        ["track", track],
        ["weather", weather],
        ["race_num", race_num],
        ["horse_num_anim", horse_race_anim],
        ["horse_num", horse_num],
        ["odds", odds],
        ["popularity", popularity],
        ["order", order],
        ["order_complex", order_complex],
        ["jockey", jockey],
        ["weight", weight],
        ["dirt_grass", dirt_grass],
        ["distance", distance],
        ["condition", condition],
        ["time", time],
        ["3furlong", furlong3],
        ["horse_weight", horse_weight],
        ["weight_incdec", weight_incdec],
        ["same_track", same_track],
        ["g1_age3", g1_age3],
        ["g2_age3", g2_age3],
        ["g3_age3", g3_age3],
        ["g1_age4", g1_age4],
        ["g2_age4", g2_age4],
        ["g3_age4", g3_age4],
        ["money", money],
    ]

    horse_id = ""
    horse = ""
    df = []

    def get_kaisai(self, track):
        if len(track) < 4:
            return 0
        else:
            if track == "札幌(地)":
                return 0
            elif track == "中京(地)":
                return 0
            elif track == "新潟(地)":
                return 0
            else:
                # todo:暫定で中央競馬
                return track[0]

    def get_week(self, track):
        if len(track) < 4:
            return 0
        else:
            if track == "札幌(地)":
                return 0
            elif track == "中京(地)":
                return 0
            elif track == "新潟(地)":
                return 0
            else:
                # todo:暫定で中央競馬
                return track[3:]

    def convet_track_id_to_num(self, track):
        if len(track) == 2:
            tmp_racetrack = racetrack_mappings[track]
        elif len(track) == 3:
            tmp_racetrack = racetrack_mappings[track]
        elif len(track) == 4 or len(track) == 5:
            if track == "札幌(地)":
                tmp_racetrack = racetrack_mappings["札幌(地)"]
            elif track == "中京(地)":
                tmp_racetrack = racetrack_mappings["中京(地)"]
            elif track == "新潟(地)":
                tmp_racetrack = racetrack_mappings["新潟(地)"]
            else:
                # todo:暫定で中央競馬
                tmp_racetrack = racetrack_mappings[track[1:3]]
        else:
            assert print("track not exist.")

        return tmp_racetrack

    def get_race_id(self, date, race_num, track, kaisai, week):
        year, month, day = date.split("/")

        if track > 10:
            tmp_race = (
                str(int(race_num)) if int(race_num) >= 10 else "0" + str(int(race_num))
            )
            race_id = year + str(track) + month + day + tmp_race  # 年+開催+月日

            assert len(race_id) == 12, print("assert!")
        else:
            tmp_racetrack = str(track) if track >= 10 else "0" + str(track)

            tmp_kaisai = str(kaisai) if int(kaisai) >= 10 else "0" + str(kaisai)
            tmp_week = str(week) if int(week) >= 10 else "0" + str(week)
            tmp_race = (
                str(int(race_num)) if int(race_num) >= 10 else "0" + str(int(race_num))
            )

            race_id = (
                year + tmp_racetrack + str(tmp_kaisai) + tmp_week + tmp_race
            )  # 年+開催+週　回

            if len(race_id) != 12:
                print(
                    "len is invalid :" + str(len(race_id)) + ",race_id :" + str(race_id)
                )
                assert len(race_id) == 12, print("assert!")

        return race_id

    def getallhorseidinfo(self):
        raceid_list = []
        for index, row in self.df.iterrows():
            self.date = row["日付"]
            self.track = row["開催"]
            self.race_num = row["天気"]
            self.race_num = row["R"]
            race_id = self.get_race_id(self.date, self.race_num, self.track)
            raceid_list.append(race_id)
            print(race_id)
        self.raceid_list = raceid_list
        return raceid_list

    def getallraceid(self):
        raceid_list = []
        for index, row in self.df.iterrows():
            self.date = row["日付"]
            self.race_num = row["R"]
            self.track = row["開催"]
            race_id = self.get_race_id(self.date, self.race_num, self.track)
            raceid_list.append(race_id)
            print(race_id)
            for tmp_race in race_id:
                race = Race(tmp_race)

        return raceid_list

    def get_sex_age_and_race_name(self):
        raceid_list = []
        for index, row in self.df.iterrows():
            self.date = row["日付"]
            self.race_num = row["R"]
            self.track = row["開催"]
            race_id = self.get_race_id(self.date, self.race_num, self.track)
            raceid_list.append(race_id)
            print(race_id)
        return raceid_list

    def adddfdatetolist(self, label, dataframe):
        list = []
        for date in dataframe[label]:
            list.append(date)

        return list

    def adddfdatatolist(self, label, dataframe):
        return dataframe[label]

    def adddistancetolist(self, label, dataframe):
        return dataframe[label][1:]

    def get_money_in_race(self, money):
        if math.isnan(money):
            money = 0.0
        return money

    def get_track_condition_by_num(self, label):
        condition_mapping = {"良": 4, "稍": 3, "重": 2, "不": 1}
        return condition_mapping[label]

    def addsametracktolist(self, label, dataframe, race):
        if dataframe[label][0] == getobjectraceinfo(race):
            return 1
        else:
            return 0

    def convertweathertonum(self, weather):
        weather_mapping = {"晴": 6, "曇": 5, "小雨": 4, "雨": 3, "小雪": 2, "雪": 1}
        return weather_mapping[weather]

    def addgrassordirttolist(self, dirt_grass):
        dirt_mapping = {"芝": 1, "ダ": 2, "障": 3}
        print(dirt_mapping[dirt_grass])
        return dirt_mapping[dirt_grass]

    def get_order(self, order):
        if type(order) == str:
            if len(order) == 4:
                tmp_order = order[0]
            elif len(order) == 5:
                tmp_order = order[0:2]
            else:
                tmp_order = order
        else:
            tmp_order = order
        return 1 if int(tmp_order) == 1 else 0

    def get_order_complex(self, order):
        if type(order) == str:
            if len(order) == 4:
                tmp_order = order[0]
            elif len(order) == 5:
                tmp_order = order[0:2]
            else:
                tmp_order = order
        else:
            tmp_order = order
        return 1 if int(tmp_order) <= 3 else 0

    def get_jockey_id(self, jockey):
        try:
            return jockey_mappings[jockey]
        except:
            return 0

    def get_grass_or_dirt_to_list(self, dirt_grass):
        dirt_mapping = {"芝": 1, "ダ": 2, "障": 3}
        print(dirt_mapping[dirt_grass])
        return dirt_mapping[dirt_grass]

    def get_time_by_second(self, time):
        minits = time[0]
        seconds = time[2:4]
        milliseconds = time[5]
        return 60 * int(minits) + int(seconds) + 0.1 * int(milliseconds)

    def get_horse_weight(self, horse_weight):
        return horse_weight[0:3]

    def get_horse_weight_inc_dec(self, horse_weight):
        tmp_weight_incdec = horse_weight[3:]
        if len(tmp_weight_incdec) == 3:
            return "0"
        elif len(tmp_weight_incdec) == 4:
            return tmp_weight_incdec[1:3]
        elif len(tmp_weight_incdec) == 5:
            return tmp_weight_incdec[1:4]
        else:
            assert False

    def get_is_same_track(self, track, this_track):
        if track == this_track:
            return 1
        else:
            return 0

    def getdateindex(self, date):
        index = 0
        for list in self.date:
            if list == date:
                break
            else:
                index = index + 1

        if index == len(self.date):
            index = -1

        return index

    def get_race_grade(self, racename):
        g1_age3 = []
        g2_age3 = []
        g3_age3 = []
        g1_age4 = []
        g2_age4 = []
        g3_age4 = []

        if "(G3)" in racename:
            if "ユニコーン" in racename or "レパード" in racename:
                g3_age3 = 1
                g3_age4 = 0
            else:
                g3_age3 = 0
                g3_age4 = 1
        else:
            g3_age3 = 0
            g3_age4 = 0

        if "(G2)" in racename:
            if "関東オークス" in racename or "兵庫チャンピョン" in racename:
                g2_age3 = 1
                g2_age4 = 0
            else:
                g2_age3 = 0
                g2_age4 = 1
        else:
            g2_age3 = 0
            g2_age4 = 0

        if "(G1)" in racename:
            if "ジャパンダートダ" in racename:
                g1_age3 = 1
                g1_age4 = 0
            else:
                g1_age3 = 0
                g1_age4 = 1
        else:
            g1_age3 = 0
            g1_age4 = 0
        return g1_age3, g1_age4, g2_age3, g2_age4, g3_age3, g3_age4

    def get_sex(self, sex_and_age):
        sex_mapping = {"牝": 1, "セ": 2, "牡": 3}
        return sex_mapping[sex_and_age[0]]

    def get_age(self, sex_and_age):
        return sex_and_age[1:]

    def getDateForDataAnalysis(self, year, month, day):
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

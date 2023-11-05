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
print(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

# 非ライブラリ
from python_ci.src.scrape.core.scrape_table_racetrack import racetrack_mappings
from python_ci.src.scrape.core.scrape_table_jockey import jockey_mappings

# from config.JBC2023.scrape_config_train_test_objectrace import scrape_config_horse_race_lists, scrape_config_racetrack
from python_ci.src.scrape.config.scrape_config_table import (
    scrape_race_eval_list,
    scrapeconfiggetobjectrace,
)

from python_ci.src.scrape.core.scrape_class_horse import Horse
from python_ci.src.scrape.core.scrape_class_race import Race
from python_ci.src.scrape.core.scrape_class_horseinteg import HorseInteg

from python_ci.src.learning.core.learning_mlp_pytorch import learning_getobjectreace

# デバッグ情報を出力するかどうか
DEBUG_INFO = True


class HorseIdNumInfo(Enum):
    HORSE_ID_NUMINFO_HORSE_ID = "horse_id"  # 馬id
    HORSE_ID_NUMINFO_SEX = "sex"  # 性
    HORSE_ID_NUMINFO_AGE = "age"  # 齢
    HORSE_ID_NUMINFO_DATE = "date"  # 日付
    HORSE_ID_NUMINFO_TRACK = "track"  # 開催
    HORSE_ID_NUMINFO_WEATHER = "weather"  # 天気
    HORSE_ID_NUMINFO_RACE_NUM = "race_num"  # レース番
    HORSE_ID_NUMINFO_HORSE_NUM_ANIM = "horse_num_anim"  # 頭数
    HORSE_ID_NUMINFO_HORSE_NUM = "horse_num"  # 馬番
    HORSE_ID_NUMINFO_ODDS = "odds"  # オッズ
    HORSE_ID_NUMINFO_POPURALITY = "popularity"  # 人気
    HORSE_ID_NUMINFO_ORDER = "order"  # 着順
    HORSE_ID_NUMINFO_JOCKEY = "jockey"  # 騎手
    HORSE_ID_NUMINFO_WEIGHT = "weight"  # 斤量
    HORSE_ID_NUMINFO_DIRT_GRASS = "dirt_grass"  # ダートor芝 or障害
    HORSE_ID_NUMINFO_DISTANCE = "distance"  # 距離
    HORSE_ID_NUMINFO_CONDITION = "condition"  # 馬場コンディション
    HORSE_ID_NUMINFO_TIME = "time"  # タイム
    HORSE_ID_NUMINFO_3FURLONG = "3furlong"  # 上がり
    HORSE_ID_NUMINFO_HORSE_WEIGHT = "horse_weight"  # 馬体重
    HORSE_ID_NUMINFO_WEIGHT_INCDEC = "weight_incdec"  # 増減


# 日付     開催   天気     R          レース名  映像  頭数   枠番  馬番   オッズ  人気  着順    騎手  斤量     距離 馬場 馬場指数     タイム   着差 ﾀｲﾑ指数           通過        ペース    上り       馬体重  厩舎ｺﾒﾝﾄ  備考     勝ち馬(2着馬)       賞金
class RACE(Enum):
    RACE_DATE = "日付"
    RACE_TRACK = "開催"
    RACE_WEATHER = "天気"
    RACE_NUM = "R"
    RACE__RACE_NAME = "レース名"
    RACE_VIDEO = "映像"
    RACE_NUM_ANIM = "頭数"
    RACE_FRAME = "枠番"
    RACE_HORSE_NUM = "馬番"
    RACE_ODDS = "オッズ"
    RACE_POP = "人気"
    RACE_ORDER = "着順"
    RACE_JOCKEY = "騎手"
    RACE_WEIGHT = "斤量"
    RACE_DIRT_GRASS_DISTANCE = "距離"
    RACE_CONDITION = "馬場"
    RACE_CONDITION_POINT = "馬場指数"
    RACE_TIME = "タイム"
    RACE_DIFF_DELI = "着差"
    RACE_TIME_POINT = "タイム指数"
    RACE_PASSING = "通過"
    RACE_PACE = "ペース"
    RACE_3FURLONG = "上り"
    RACE_HORSE_WEIGHT = "馬体重"
    RACE_COMMENT = "厩舎コメント"
    RACE_ETC = "備考"
    RACE_WINNER = "勝ち馬(2着馬)"
    RACE_PRICE = "賞金"


# 着順  枠番  馬番        馬名  性齢  斤量    騎手     タイム   着差   単勝  人気     馬体重       調教師
class HORSE(Enum):
    HORSE_ORDER = "着順"
    HORSE_FRAME = "枠番"
    HORSE_HORSE_NUM = "馬番"
    HORSE_NAME = "馬名"
    HORSE_SEX_AGE = "性齢"
    HORSE_WEIGHT = "斤量"
    HORSE_JOCKEY = "騎手"
    HORSE_TIME = "タイム"
    HORSE_DIFF_DELI = "着差"
    HORSE_DIFF_ODDS = "単勝"
    HORSE_POPORALITY = "人気"
    HORSE_HORSE_WEIGHT = "馬体重"
    HORSE_TRAINER = "調教師"


def scrapegetobjectrace():
    return scrapeconfiggetobjectrace()


def makeRaceInfo(day, racename, horse_id_list, force_get_last_5race, object_track):
    df = pd.DataFrame()
    OBJECT_DAY = day
    RACE_NAME = racename
    horse_id_list = horse_id_list

    teiou_train_2023_df = pd.DataFrame()
    teiou_test_2023_df = pd.DataFrame()

    for horse_id in horse_id_list:
        horse_id_set = []  # horse_id
        sex = []  # race
        age = []  # race
        date = []  # horse_id
        dateforda = []  # horse_id
        place = []  # horse_id
        track = []  # horse_id
        weather = []  # horse_id
        race_num = []  # horse_id
        horse_race_anim = []  # horse_id
        horse_num = []  # horse_id
        odds = []  # horse_id
        popularity = []  # horse_id
        order = []  # this
        order_complex = []  # this
        jockey = []  # horse_id
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
        race_id = []
        kaisai = []
        week = []

        horse = Horse(horse_id)
        horse.gethorseinfowithvalidation()

        # レースから照合するためのパラメータを取得
        # 以下は
        # https://db.netkeiba.com/horse/xxxxxxxxxx/
        # からスクレイピングしている

        # for tmp_place in horse_info_data_frame["開催"]:
        #    horse_id_set.append(horse_id)

        horse_id_set = horse.get_horse_id_list()
        print(horse_id_set)

        # sex
        # age
        horseinteg = HorseInteg()
        date = horse.get_date_list()
        for tmp_date in date:
            tmp_year, tmp_month, tmp_day = tmp_date.split("/")
            tmp_dateforda = horseinteg.getDateForDataAnalysis(
                int(tmp_year), int(tmp_month), int(tmp_day)
            )
            dateforda.append(tmp_dateforda)

        tmp_track_list = horse.get_track_list()
        for tmp_track in tmp_track_list:
            tmp_kaisai = horseinteg.get_kaisai(tmp_track)
            kaisai.append(tmp_kaisai)

        tmp_track_list = horse.get_track_list()
        for tmp_track in tmp_track_list:
            tmp_week = horseinteg.get_week(tmp_track)
            week.append(tmp_week)

        tmp_track_list = horse.get_track_list()
        for tmp_track in tmp_track_list:
            tmp_data = horseinteg.convet_track_id_to_num(tmp_track)
            track.append(tmp_data)

        tmp_weather_list = horse.get_weather_list()
        for tmp_weather in tmp_weather_list:
            weather.append(horseinteg.convertweathertonum(tmp_weather))

        race_num = horse.get_race_number_list()
        horse_race_anim = horse.get_horse_number_list()
        horse_num = horse.get_horse_count_list()
        odds = horse.get_odds_list()
        popularity = horse.get_popularity_list()

        for tmp_order in horse.get_finishing_order_list():
            order.append(horseinteg.get_order(tmp_order))

        for tmp_order in horse.get_finishing_order_list():
            order_complex.append(horseinteg.get_order_complex(tmp_order))

        for tmp_jockey in horse.get_starting_jockey_list():
            jockey.append(horseinteg.get_jockey_id(tmp_jockey))

        weight = horse.get_impost_list()

        for tmp_dirt_grass in horse.get_distance_list():
            dirt_grass.append(horseinteg.get_grass_or_dirt_to_list(tmp_dirt_grass[0]))

        for tmp_distance in horse.get_distance_list():
            distance.append(tmp_distance[1:])

        for tmp_condition in horse.get_track_condition_list():
            condition.append(horseinteg.get_track_condition_by_num(tmp_condition))

        for tmp_time in horse.get_time_list():
            time.append(horseinteg.get_time_by_second(tmp_time))

        furlong3 = horse.get_3farlong_list()

        for tmp_horse_weight in horse.get_horse_weight_list():
            horse_weight.append(horseinteg.get_horse_weight(tmp_horse_weight))

        for tmp_horse_weight in horse.get_horse_weight_list():
            weight_incdec.append(horseinteg.get_horse_weight_inc_dec(tmp_horse_weight))

        for tmp_track in horse.get_track_list():
            same_track.append(horseinteg.get_is_same_track(tmp_track, object_track))

        for tmp_race_name in horse.get_race_name_list():
            (
                tmp_g1_3,
                tmp_g1_4,
                tmp_g2_3,
                tmp_g2_4,
                tmp_g3_3,
                tmp_g3_4,
            ) = horseinteg.get_race_grade(tmp_race_name)
            g1_age3.append(tmp_g1_3)
            g2_age3.append(tmp_g2_3)
            g3_age3.append(tmp_g3_3)
            g1_age4.append(tmp_g1_4)
            g2_age4.append(tmp_g2_4)
            g3_age4.append(tmp_g3_4)

        for tmp_money in horse.get_money_list():
            money.append(horseinteg.get_money_in_race(tmp_money))

        for i in range(len(date)):
            tmp_race_id = horseinteg.get_race_id(
                date[i], race_num[i], track[i], kaisai[i], week[i]
            )
            race_id.append(tmp_race_id)

        for i in range(len(race_id)):
            tmp_race = Race(race_id[i])
            sex_and_age = tmp_race.get_sex_and_age(horse_race_anim[i])
            sex.append(horseinteg.get_sex(sex_and_age))
            age.append(horseinteg.get_age(sex_and_age))

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

        horse_info_data_frame2 = pd.DataFrame()
        i = 0
        for labellist in labellists:
            loc = len(horse_info_data_frame2.columns)
            horse_info_data_frame2.insert(loc, labellist[0], labellist[1])

        counter = 0

        print(len(labellists))

        for index in range(0, len(horse_info_data_frame2)):
            findIndex = False
            hoge2 = horse_info_data_frame2.iloc[index, 3]

            if hoge2 == OBJECT_DAY or force_get_last_5race == True:
                findIndex = True
                break
            else:
                counter = counter + 1

        if findIndex != True:
            print(horse_info_data_frame2.iloc[0:, :])
            print(OBJECT_DAY + "is not valid")

        assert findIndex == True

        counter_last_5 = counter + 1
        counter_last5_plus_5 = counter_last_5 + 5

        if DEBUG_INFO == True:
            print("---------------train_data---------------")
            print(horse_info_data_frame2.iloc[counter_last_5:counter_last5_plus_5, :])
            print("---------------end_train_data-----------")

            print("---------------test_data---------------")
            print(horse_info_data_frame2.iloc[counter : counter + 1, :])
            print("---------------end_test_data-----------")

        # 訓練データ
        teiou_train_2023_df = teiou_train_2023_df.append(
            horse_info_data_frame2.iloc[counter_last_5:counter_last5_plus_5, :]
        )

        # テストデータ
        if findIndex == True:
            teiou_test_2023_df = teiou_test_2023_df.append(
                horse_info_data_frame2.iloc[counter : counter + 1, :]
            )
        else:
            print("warning:test data not made:" + race_id)

    horse_info_new_path = "./python_ci/csv/learning/" + RACE_NAME + "_last5race.csv"
    teiou_train_2023_df.to_csv(horse_info_new_path)

    if teiou_test_2023_df.empty != True:
        horse_info_new_path = "./python_ci/csv/learning/" + RACE_NAME + "_result.csv"
        teiou_test_2023_df.to_csv(horse_info_new_path)


def main():
    race = scrapegetobjectrace()
    learning_race = learning_getobjectreace()
    assert race == learning_race

    scrape_config_horse_race_lists = scrape_race_eval_list[race][0]
    for list in scrape_config_horse_race_lists:
        makeRaceInfo(list[0], list[1], list[2], list[3], race)


if __name__ == "__main__":
    main()

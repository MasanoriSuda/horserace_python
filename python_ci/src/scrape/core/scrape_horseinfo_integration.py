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

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
print(str(Path(__file__).resolve().parent.parent.parent))

# 非ライブラリ
from scrape.core.scrape_racetrack import racetrack_mappings
from scrape.core.scrape_horserace_util import (
    getRaceResultLocal,
    getRaceResultJRA,
    getHorseInfo,
    getDateForDataAnalysis,
    getobjectraceinfo,
)
from scrape.core.scrape_jockeytable import jockey_mappings

# from config.JBC2023.scrape_config_train_test_objectrace import scrape_config_horse_race_lists, scrape_config_racetrack
from scrape.config.scrape_config_table import (
    scrape_race_eval_list,
    scrapeconfiggetobjectrace,
)

from learning.core.learning_mlp_pytorch import learning_getobjectreace

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


def main():
    race = scrapegetobjectrace()
    learning_race = learning_getobjectreace()
    assert race == learning_race

    scrape_config_horse_race_lists = scrape_race_eval_list[race][0]
    for list in scrape_config_horse_race_lists:
        makeRaceInfo(list[0], list[1], list[2], list[3], race)


def getvalidrace(horse_info_data_frame_src):
    """_summary_
    checke whether this race is held in japan or not
    """

    horse_info_data_frame = horse_info_data_frame_src

    # レース除外、中止、海外レース等のケースは取り除いておく
    horse_info_data_frame = horse_info_data_frame[horse_info_data_frame["着順"] != "除"]
    horse_info_data_frame = horse_info_data_frame[horse_info_data_frame["着順"] != "取"]
    horse_info_data_frame = horse_info_data_frame[horse_info_data_frame["馬体重"] != "計不"]
    horse_info_data_frame = horse_info_data_frame[horse_info_data_frame["着順"] != "中"]
    horse_info_data_frame = horse_info_data_frame[
        horse_info_data_frame["着順"].isna() == False
    ]
    horse_info_data_frame = horse_info_data_frame[
        horse_info_data_frame["天気"].isna() == False
    ]
    horse_info_data_frame = horse_info_data_frame[
        horse_info_data_frame["枠番"].isna() == False
    ]

    return horse_info_data_frame


def addhorseidtolist(horse_id, dataframe):
    list = []
    for i in range(0, len(dataframe)):
        list.append(horse_id)

    return list


def adddfdatatolist(label, dataframe):
    list = []
    for tmp_data in dataframe[label]:
        list.append(tmp_data)

    return list


def adddistancetolist(label, dataframe):
    list = []
    for tmp_distance in dataframe[label]:
        distance = tmp_distance[1:]
        list.append(distance)

    return list


def addmoneytolist(label, dataframe):
    list = []
    for tmp_money in dataframe[label]:
        tmp2_money = tmp_money
        if math.isnan(tmp_money):
            tmp2_money = 0.0
        list.append(tmp2_money)
    return list


def addtrackcondition(label, dataframe):
    list = []
    for tmp2_dirt_or_grass in dataframe[label]:
        condition_mapping = {"良": 4, "稍": 3, "重": 2, "不": 1}
        tmp_condition = condition_mapping[tmp2_dirt_or_grass]
        list.append(tmp_condition)
    return list


def addsametracktolist(label, dataframe, race):
    list = []
    for tmp_place in dataframe[label]:
        if tmp_place == getobjectraceinfo(race):
            list.append(1)
        else:
            list.append(0)
    return list


def addweathertolist(label, dataframe):
    list = []
    for tmp_horse_num in dataframe[label]:
        weather_mapping = {"晴": 6, "曇": 5, "小雨": 4, "雨": 3, "小雪": 2, "雪": 1}
        tmp_weather = weather_mapping[tmp_horse_num]
        list.append(tmp_weather)
    return list


def addgrassordirttolist(label, dataframe):
    list = []
    for tmp2_dirt_or_grass in dataframe[label]:
        dirt_mapping = {"芝": 1, "ダ": 2, "障": 3}
        list.append(dirt_mapping[tmp2_dirt_or_grass[0:1]])

    return list


def addgraderaceinfotolist(label, dataframe):
    g1_age3 = []
    g2_age3 = []
    g3_age3 = []
    g1_age4 = []
    g2_age4 = []
    g3_age4 = []
    for racename in dataframe[label]:
        if "(G3)" in racename:
            if "ユニコーン" in racename or "レパード" in racename:
                g3_age3.append(1)
                g3_age4.append(0)
            else:
                g3_age3.append(0)
                g3_age4.append(1)
        else:
            g3_age3.append(0)
            g3_age4.append(0)

        if "(G2)" in racename:
            if "関東オークス" in racename or "兵庫チャンピョン" in racename:
                g2_age3.append(1)
                g2_age4.append(0)
            else:
                g2_age3.append(0)
                g2_age4.append(1)
        else:
            g2_age3.append(0)
            g2_age4.append(0)

        if "(G1)" in racename:
            if "ジャパンダートダ" in racename:
                g1_age3.append(1)
                g1_age4.append(0)
            else:
                g1_age3.append(0)
                g1_age4.append(1)
        else:
            g1_age3.append(0)
            g1_age4.append(0)
    return g1_age3, g1_age4, g2_age3, g2_age4, g3_age3, g3_age4


def makeRaceInfo(day, racename, horse_id_list, force_get_last_5race, race):
    df = pd.DataFrame()
    OBJECT_DAY = day
    RACE_NAME = racename
    horse_id_list = horse_id_list

    teiou_train_2023_df = pd.DataFrame()
    teiou_test_2023_df = pd.DataFrame()

    for horse_id in horse_id_list:
        horse_info_path = "./python_ci/csv/scrape/horse_id/" + str(horse_id) + ".csv"

        is_file = os.path.isfile(horse_info_path)
        if is_file == False:
            horse_info_data_frame = getHorseInfo(horse_id)
            print(horse_info_data_frame)
            horse_info_data_frame.to_csv(horse_info_path)
        else:
            horse_info_data_frame = pd.read_csv(horse_info_path, index_col=0)

        horse_info_data_frame = getvalidrace(horse_info_data_frame)

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

        # レースから照合するためのパラメータを取得
        # 以下は
        # https://db.netkeiba.com/horse/xxxxxxxxxx/
        # からスクレイピングしている

        # for tmp_place in horse_info_data_frame["開催"]:
        #    horse_id_set.append(horse_id)

        horse_info_data_frame_tmp = horse_info_data_frame["開催"]
        horse_id_set = addhorseidtolist(horse_id, horse_info_data_frame_tmp)

        place = adddfdatatolist("開催", horse_info_data_frame)

        same_track = addsametracktolist("開催", horse_info_data_frame, race)

        date = adddfdatatolist("日付", horse_info_data_frame)

        race_num = adddfdatatolist("R", horse_info_data_frame)

        horse_num = adddfdatatolist("馬番", horse_info_data_frame)

        horse_race_anim = adddfdatatolist("頭数", horse_info_data_frame)

        weather = addweathertolist("天気", horse_info_data_frame)

        dirt_grass = addgrassordirttolist("距離", horse_info_data_frame)

        distance = adddistancetolist("距離", horse_info_data_frame)

        condition = addtrackcondition("馬場", horse_info_data_frame)

        furlong3 = adddfdatatolist("上り", horse_info_data_frame)

        money = addmoneytolist("賞金", horse_info_data_frame)

        g1_age3, g1_age4, g2_age3, g2_age4, g3_age3, g3_age4 = addgraderaceinfotolist(
            "レース名", horse_info_data_frame
        )

        # Todo 調教師を追加したい→転厩の可能性があるので、レース毎にアペンド予定
        # Todo オーナーを追加したい

        # 各レース情報を別で引っ張ってくる
        # https://db.netkeiba.com/race/xxxxxxxxxxxx/
        # からとってきている
        for num in range(len(date)):
            hasraceinfo = True
            tmp = date[num].split("/")

            dateforda.append(
                getDateForDataAnalysis(int(tmp[0]), int(tmp[1]), int(tmp[2]))
            )

            if len(place[num]) == 2:
                tmp_racetrack = racetrack_mappings[place[num]]
            elif len(place[num]) == 3:
                tmp_racetrack = racetrack_mappings[place[num]]
            elif len(place[num]) == 4 or len(place[num]) == 5:
                if place[num] == "札幌(地)":
                    tmp_racetrack = racetrack_mappings["札幌(地)"]
                elif place[num] == "中京(地)":
                    tmp_racetrack = racetrack_mappings["中京(地)"]
                elif place[num] == "新潟(地)":
                    tmp_racetrack = racetrack_mappings["新潟(地)"]
                else:
                    # todo:暫定で中央競馬
                    tmp_racetrack = racetrack_mappings[place[num][1:3]]
            else:
                assert print("track not exist.")

            tmp_place = str(tmp_racetrack)

            if tmp_racetrack > 10 and tmp_racetrack <= 100:
                tmp_day = (
                    str(tmp_racetrack)
                    if tmp_racetrack >= 10
                    else "0" + str(tmp_racetrack)
                )
                tmp_race = (
                    str(int(race_num[num]))
                    if int(race_num[num]) >= 10
                    else "0" + str(int(race_num[num]))
                )
                race_id = tmp[0] + str(tmp_day) + tmp[1] + tmp[2] + tmp_race  # 年+開催+月日
            else:
                tmp_day = (
                    str(tmp_racetrack)
                    if tmp_racetrack >= 10
                    else "0" + str(tmp_racetrack)
                )
                tmp_kaisai = int(place[num][0])
                if len(place[num]) == 4:
                    tmp_week = int(place[num][3])
                elif len(place[num]) == 5:
                    tmp_week = int(place[num][3:5])

                tmp_kaisai = (
                    str(tmp_kaisai) if tmp_kaisai >= 10 else "0" + str(tmp_kaisai)
                )
                tmp_week = str(tmp_week) if tmp_week >= 10 else "0" + str(tmp_week)
                tmp_race = (
                    str(int(race_num[num]))
                    if int(race_num[num]) >= 10
                    else "0" + str(int(race_num[num]))
                )

                race_id = (
                    tmp[0] + str(tmp_day) + str(tmp_kaisai) + (tmp_week) + str(tmp_race)
                )  # 年+開催+週　回

                assert len(race_id) == 12, print("assert!")

            race_info_path = "./python_ci/csv/scrape/race_id/" + race_id + ".csv"
            is_file = os.path.isfile(race_info_path)
            if is_file == False:
                print(race_info_path + ":file not exists")
                assert len(race_id) == 12, print("assert!")

                # todo 中央と地方で関数をまとめる
                if tmp_racetrack <= 10:
                    race_info_data_frame = getRaceResultJRA(
                        int(tmp[0]),
                        int(tmp[1]),
                        int(tmp[2]),
                        race_num[num],
                        racetrack_mappings[place[num][1:3]],
                        int(tmp_kaisai),
                        int(tmp_week),
                    )
                else:
                    race_info_data_frame = getRaceResultLocal(
                        int(tmp[0]),
                        int(tmp[1]),
                        int(tmp[2]),
                        int(race_num[num]),
                        racetrack_mappings[place[num]],
                    )

                try:
                    race_info_data_frame.to_csv(race_info_path)
                except:
                    hasraceinfo = False

            is_file = os.path.isfile(race_info_path)
            if is_file == True:
                race_info_data_frame = pd.read_csv(race_info_path)
                hoge = horse_num[num]
                tmp_each_race_df = race_info_data_frame.query("馬番 == @hoge")
            else:
                hasraceinfo = False

            if hasraceinfo == False:
                sex.append("0")
                age.append("0")
                # date.append('0')
                track.append("0")
                # weather.append('0')
                # horse_race_anim.append('0')
                # horse_num.append('0')
                odds.append("0")

                popularity.append("0")
                order.append("0")
                order_complex.append("0")
                jockey.append("0")
                weight.append("0")
                # dirt_grass.append('0')
                # distance.append('0')
                # condition.append('0')
                time.append("0")
                # furlong3.append('0')
                horse_weight.append("0")
                weight_incdec.append("0")

            else:
                tmp_sex = tmp_each_race_df["性齢"].values[0][0]
                if tmp_sex == "牡":
                    sex.append("3")
                elif tmp_sex == "牝":
                    sex.append("1")
                elif tmp_sex == "セ":
                    sex.append("2")
                elif tmp_sex == "牡":
                    sex.append("0")

                tmp_age = tmp_each_race_df["性齢"].values[0][1:]
                age.append(tmp_age)

                tmp_track = tmp_racetrack
                track.append(tmp_track)

                # 馬情報取得時に設定済み
                # weather_mapping={'晴':4,'曇':3,'小雨':2,'雨':1}
                # tmp_weather = weather_mapping[tmp_each_race_df['天気']]
                # weather.append(tmp_weather)

                # tmp_race_num = tmp_each_race_df['R']
                # race_num.append(tmp_race_num)

                # tmp_horse_race_anim = tmp_each_race_df['頭数']
                # horse_race_anim.append(tmp_horse_race_anim)

                tmp_odds = tmp_each_race_df["単勝"].values[0]
                odds.append(tmp_odds)

                tmp_horse_race_anim = tmp_each_race_df["人気"].values[0]
                popularity.append(tmp_horse_race_anim)

                tmp_order = str(tmp_each_race_df["着順"].values[0]).split("(")
                tmp2_order = int(tmp_order[0])
                tmp3_order = "1" if tmp2_order <= 1 else "0"
                order.append(tmp3_order)
                tmp3_order = "1" if tmp2_order <= 3 else "0"
                order_complex.append(tmp3_order)

                tmp2_jockey = tmp_each_race_df["騎手"].values[0]

                try:
                    tmp_jockey = jockey_mappings[tmp2_jockey]
                except:
                    tmp_jockey = 0
                    # print('not found: ' +tmp2_jockey)

                jockey.append(tmp_jockey)

                tmp_weight = tmp_each_race_df["斤量"].values[0]
                weight.append(tmp_weight)

                # tmp_dirt_or_grass = tmp_each_race_df.at[0,'距離'][0]
                # if(tmp_dirt_or_grass=='芝'):
                #    dirt_grass.append('1')
                # else:
                #    dirt_grass.append('2')

                # tmp_distance = tmp_dirt_or_grass = tmp_each_race_df.at[0,'距離'][1:]
                # distance.append(tmp_distance)

                # condition_mapping={'良':4,'稍':3,'重':2,'不良':1}
                # tmp_condition = condition_mapping[tmp_each_race_df.loc[0,'馬場']]
                # condition.append(tmp_condition)

                tmp_time = tmp_each_race_df["タイム"].values[0]
                tmp2_condition = (
                    str(int(tmp_time[0]) * 60 + int(tmp_time[2:4])) + "." + tmp_time[5]
                )
                time.append(tmp2_condition)

                # tmp_furlong = tmp_each_race_df['上り'].values[0]
                # furlong3.append(tmp_furlong)

                tmp_horse_weight = tmp_each_race_df["馬体重"].values[0][0:3]
                horse_weight.append(tmp_horse_weight)

                tmp_weight_incdec = tmp_each_race_df["馬体重"].values[0][3:]
                if len(tmp_weight_incdec) == 3:
                    weight_incdec.append("0")
                elif len(tmp_weight_incdec) == 4:
                    weight_incdec.append(str(int(tmp_weight_incdec[1:3])))
                elif len(tmp_weight_incdec) == 5:
                    weight_incdec.append(str(int(tmp_weight_incdec[1:4])))

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
        for labellist in labellists:
            loc = len(horse_info_data_frame2.columns)
            horse_info_data_frame2.insert(loc, labellist[0], labellist[1])

        counter = 0

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


if __name__ == "__main__":
    main()

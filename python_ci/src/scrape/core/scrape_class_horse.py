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


class Horse:
    horse_id = ""
    horse_info_data_frame = []
    race_id = []

    def gethorseurl(self):
        url = "https://db.netkeiba.com/horse/" + self.horse_id

        return url

    def is_exist_horse_id_info_csv(self):
        horse_info_path = "./python_ci/csv/scrape/horse_id/" + self.horse_id + ".csv"

        is_file = os.path.isfile(horse_info_path)
        print(self.horse_id)
        print("horse ok!!!")
        assert is_file == True

        return is_file

    def get_horse_id_info_from_csv(self):
        horse_info_path = "./python_ci/csv/scrape/horse_id/" + self.horse_id + ".csv"
        horse_info_data_frame = pd.read_csv(horse_info_path, index_col=0)

        return horse_info_data_frame

    def set_horse_id_info_to_csv(self, df):
        horse_info_path = (
            "./python_ci/csv/scrape/horse_id/" + str(self.horse_id) + ".csv"
        )
        df.to_csv(horse_info_path)

    def get_horse_id_info_from_url(self):
        # print(this_horse_id)

        url = self.gethorseurl(self.horse_id)

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

    def isexisthorseid(self):
        ret = True
        horse_info_path = (
            "./python_ci/csv/scrape/horse_id/" + str(self.horse_id) + ".csv"
        )

        is_file = os.path.isfile(horse_info_path)
        if is_file == False:
            print("horse_idが存在しません")
            ret = False

        return ret

    def __init__(self, horse_id):
        assert len(str(horse_id)) == 10
        self.horse_id = str(horse_id)
        if self.is_exist_horse_id_info_csv():
            self.horse_info_data_frame = self.get_horse_id_info_from_csv()
        else:
            df = self.get_horse_id_info_from_url()
            self.set_horse_id_info_to_csv(df)
            df = self.getvalidrace(self.horse_info_data_frame)
            self.horse_info_data_frame = df

    def ishorseraceexists(self, date):
        date_df = self.horse_info_data_frame
        if date in date_df:
            return True
        else:
            print("Error:" + date + "には出走していません")
            return False

    def getvalidrace(self, horse_info_data_frame_src):
        """_summary_
        checke whether this race is held in japan or not
        """

        horse_info_data_frame = horse_info_data_frame_src

        # レース除外、中止、海外レース等のケースは取り除いておく
        horse_info_data_frame = horse_info_data_frame[
            horse_info_data_frame["着順"] != "除"
        ]
        horse_info_data_frame = horse_info_data_frame[
            horse_info_data_frame["着順"] != "取"
        ]
        horse_info_data_frame = horse_info_data_frame[
            horse_info_data_frame["馬体重"] != "計不"
        ]
        horse_info_data_frame = horse_info_data_frame[
            horse_info_data_frame["着順"] != "中"
        ]
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

    def gethorseinfowithvalidation(self):
        df = self.getvalidrace(self.horse_info_data_frame)
        self.horse_info_data_frame = df
        return df

    def getnumofraceenterd(self):
        return len(self.horse_info_data_frame.index)

    def get_horse_id_list(self):
        horse_number_list = []

        for i in range(len(self.get_list_from_label("開催"))):
            try:
                horse_number = self.horse_id

            except:
                continue
            horse_number_list.append(horse_number)
        print(len(horse_number_list))
        return horse_number_list

    def get_list_from_label(self, label, needint=False):
        horse_number_list = []

        for i in range(len(self.horse_info_data_frame)):
            try:
                horse_number = self.horse_info_data_frame.at[i, label]
                if needint == True:
                    horse_number = int(horse_number)

            except:
                continue
            horse_number_list.append(horse_number)

        return horse_number_list

    def get_date_list(self):
        return self.get_list_from_label("日付")

    def get_track_list(self):
        return self.get_list_from_label("開催")

    def get_weather_list(self):
        return self.get_list_from_label("天気")

    def get_race_number_list(self):
        return self.get_list_from_label("R", True)

    def get_race_name_list(self):
        return self.get_list_from_label("レース名")

    def get_horse_number_list(self):
        return self.get_list_from_label("馬番")

    def get_horse_count_list(self):
        return self.get_list_from_label("頭数")

    def get_starting_gate_number_list(self):
        return self.get_list_from_label("馬番")

    def get_odds_list(self):
        return self.get_list_from_label("オッズ")

    def get_popularity_list(self):
        return self.get_list_from_label("人気")

    def get_finishing_order_list(self):
        return self.get_list_from_label("着順")

    def get_starting_jockey_list(self):
        return self.get_list_from_label("騎手")

    def get_impost_list(self):
        return self.get_list_from_label("斤量")

    def get_distance_list(self):
        return self.get_list_from_label("距離")

    def get_track_condition_list(self):
        return self.get_list_from_label("馬場")

    def get_time_list(self):
        return self.get_list_from_label("タイム")

    def get_3farlong_list(self):
        return self.get_list_from_label("上り")

    def get_horse_weight_list(self):
        return self.get_list_from_label("馬体重")

    def get_money_list(self):
        return self.get_list_from_label("賞金")


def main():
    horse = Horse("2017103843")
    print(horse.gethorseinfowithvalidation())
    print(horse.getnumofraceenterd())
    print(horse.get_horse_id_list("開催"))
    print(horse.get_date_list())
    print(horse.get_horse_number_list())
    print(horse.get_race_number_list())


if __name__ == "__main__":
    main()

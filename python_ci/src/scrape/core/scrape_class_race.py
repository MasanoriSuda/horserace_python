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
print(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

# 非ライブラリ
from python_ci.src.scrape.core.scrape_table_racetrack import racetrack_mappings
from python_ci.src.scrape.core.scrape_class_horse import Horse

# from config.JBC2023.scrape_config_train_test_objectrace import scrape_config_horse_race_lists, scrape_config_racetrack
from python_ci.src.scrape.config.scrape_config_table import (
    scrape_race_eval_list,
    scrapeconfiggetobjectrace,
)


class Race:
    race_id = ""
    race_results_data_frame = []

    def get_race_url(self, race_num):
        url = "https://db.netkeiba.com/race/" + race_num

        return url

    def is_exist_race_id_info_csv(self):
        race_info_path = "./python_ci/csv/scrape/race_id/" + str(self.race_id) + ".csv"

        is_file = os.path.isfile(race_info_path)

        assert is_file == True

        return is_file

    def get_race_id_info_from_csv(self):
        race_info_path = "./python_ci/csv/scrape/race_id/" + str(self.race_id) + ".csv"
        race_info_data_frame = pd.read_csv(race_info_path, index_col=0)

        return race_info_data_frame

    def set_race_id_info_to_csv(self, df):
        # print(df)
        race_info_path = "./python_ci/csv/scrape/race_id/" + str(self.race_id) + ".csv"
        df.to_csv(race_info_path)

    def get_race_result_by_race_id(self):
        url = self.get_race_url(self.race_id)
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
            self.race_results_data_frame = race_results_data_frame
        return race_results_data_frame

    def make_race_id_data(self):
        if self.is_exist_race_id_info_csv() == True:
            self.race_results_data_frame = self.get_race_id_info_from_csv()
        else:
            df = self.get_race_result_by_race_id()
            print(df)
            self.set_race_id_info_to_csv(df)
            self.race_results_data_frame = df

    def __init__(self, race_id):
        print(race_id)
        assert len(str(race_id)) == 12
        self.race_id = str(race_id)
        self.make_race_id_data()

    def get_sex_and_age(self, gate_num):
        tmp_each_race_df = self.race_results_data_frame.query("馬番 == @gate_num")
        # "性齢" 列の値を抽出
        sex_and_age = tmp_each_race_df.loc[tmp_each_race_df.index[0], "性齢"]
        return sex_and_age

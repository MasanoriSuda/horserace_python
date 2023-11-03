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
from python_ci.src.scrape.core.scrape_racetrack_table import racetrack_mappings
from python_ci.src.scrape.core.scrape_horserace_util import (
    getRaceResultByRaceID,
    getHorseInfo,
    getDateForDataAnalysis,
    getobjectraceinfo,
    getRaceURL,
    getRaceResultByRaceID,
)
from python_ci.src.scrape.core.scrape_jockeytable import jockey_mappings

# from config.JBC2023.scrape_config_train_test_objectrace import scrape_config_horse_race_lists, scrape_config_racetrack
from python_ci.src.scrape.config.scrape_config_table import (
    scrape_race_eval_list,
    scrapeconfiggetobjectrace,
)


class Race:
    race_id = ""

    def __init__(self, race_id):
        assert len(race_id) == 12
        self.race_id = race_id

    def getRaceResultByRaceID(self):
        url = getRaceURL(self.race_id)
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


def main():
    race = Race("202346092610")
    df = race.getRaceResultByRaceID()
    print(df)


if __name__ == "__main__":
    main()

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
from scrape.core.scrape_horserace_util import (
    getHorseInfo,
)


class Horse:
    horse_info_data_frame = []

    def __init__(self, horse_id):
        assert len(horse_id) == 10
        self.horse_id = horse_id

    def isexisthorseid(self):
        ret = True
        horse_info_path = (
            "./python_ci/csv/scrape/horse_id/" + str(self.horse_id) + ".csv"
        )

        is_file = os.path.isfile(horse_info_path)
        if is_file == False:
            self.horse_info_data_frame = getHorseInfo(self.horse_id)
            if self.horse_info_data_frame != []:
                print("horse_idが存在しません")
                ret = False

        return ret

    def ishorseraceexists(self, date):
        date_df = self.horse_info_data_frame
        if date in date_df:
            return True
        else:
            print("Error:" + date + "には出走していません")
            return False

    def gethorseinfo(self, horse_id):
        horse_info_path = "./python_ci/csv/scrape/horse_id/" + str(horse_id) + ".csv"

        is_file = os.path.isfile(horse_info_path)
        if is_file == False:
            horse_info_data_frame = getHorseInfo(horse_id)
            if horse_info_data_frame.empty == False:
                horse_info_data_frame.to_csv(horse_info_path)
        else:
            horse_info_data_frame = pd.read_csv(horse_info_path, index_col=0)

        return horse_info_data_frame

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
        horse_info_data_frame_src = self.gethorseinfo(self.horse_id)
        df = self.getvalidrace(horse_info_data_frame_src)
        self.horse_info_data_frame = df
        return df

    def getnumofraceenterd(self):
        return len(self.horse_info_data_frame.index)


def main():
    horse = Horse("2017103843")
    print(horse.gethorseinfowithvalidation())
    print(horse.getnumofraceenterd())


if __name__ == "__main__":
    main()

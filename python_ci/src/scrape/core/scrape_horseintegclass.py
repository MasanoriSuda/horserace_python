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

from python_ci.src.scrape.core.scrape_horseclass import Horse

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

    horse = Horse("2019102383")
    df = horse.gethorseinfowithvalidation()

    df_tmp = df["日付"]

    print(df_tmp)

    def __init__():
        return 0

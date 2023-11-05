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
from racetrack import racetrack_mappings
from horserace_util import getRaceResultLocal


def main():
    print("start")

    df = pd.DataFrame()

    dict = {}
    for hogehoge in range(0, 2):
        if hogehoge == 1:
            counter_start = 5000
            counter_end = 6000
        else:
            counter_start = 5000
            counter_end = 000
        for jockey_id in range(counter_start, counter_end):
            for counter in range(0, 2):
                if counter == 0:
                    url = (
                        "https://db.netkeiba.com/jockey/result/recent/"
                        + "0"
                        + str(jockey_id)
                    )
                else:
                    url = (
                        "https://db.netkeiba.com//?pid=jockey_detail&id=0"
                        + str(jockey_id)
                        + "&page=2"
                    )

                if hogehoge != 1:
                    if counter == 0:
                        url = "https://db.netkeiba.com/jockey/result/recent/" + hex(
                            jockey_id
                        ).replace("0x", "")
                    else:
                        url = (
                            "https://db.netkeiba.com//?pid=jockey_detail&id=0"
                            + hex(jockey_id).replace("0x", "")
                            + "&page=2"
                        )

                race_request = requests.get(url)
                race_request.encoding = "EUC-JP"
                # サーバー負荷対策でスリープを入れる
                time.sleep(0.1)

                if race_request:
                    try:
                        race_results_data_frame = pd.read_html(url)[0]
                        hoge = True
                    except:
                        # print(hex(jockey_id).replace('0x','') + "jockey has not exist")
                        print(hex(jockey_id) + ":jockey has not exist")
                        race_results_data_frame = []
                        break

                # デバッグ用
                date = race_results_data_frame.iat[0, 0]
                place = race_results_data_frame.iat[0, 1]
                race_num = race_results_data_frame.iat[0, 3]
                horse_name = race_results_data_frame.iat[0, 12]

                tmp = date.split("/")
                year = int(tmp[0])
                month = int(tmp[1])
                day = int(tmp[2])

                try:
                    value = racetrack_mappings[place]
                except:
                    value = 0

                # if(place == '浦和'):
                #    value = 42
                # elif(place == '船橋'):
                #    value = 43
                # elif(place == '大井'):
                #    value = 44
                # elif(place == '川崎'):
                #    value = 45
                # else:
                #    value = 0

                race_id = ""
                tmp_year = str(year)
                tmp_month = str(month) if month >= 10 else "0" + str(month)
                tmp_day = str(day) if day >= 10 else "0" + str(day)
                tmp_race = str(race_num) if race_num >= 10 else "0" + str(race_num)
                tmp_place_num = str(value)
                race_id = tmp_year + tmp_place_num + tmp_month + tmp_day + tmp_race

                path = (
                    "/home/msuda/workspace/vscode/horserace/python_ci/csv/race_id/"
                    + race_id
                    + ".csv"
                )
                try:
                    df = pd.read_csv(path, index_col=0)
                except:
                    print(str(jockey_id) + "not found")
                    continue
                # print(df)

                hoge = horse_name
                tmp_df = df.query("馬名 == @hoge")
                print(tmp_df.iat[0, 9])
                jocky_name = tmp_df.iat[0, 9]
                dict[jocky_name] = jockey_id
                break

        # print(tmp_df)

    print(dict)


if __name__ == "__main__":
    main()

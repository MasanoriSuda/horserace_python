from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
print(str(Path(__file__).resolve().parent.parent.parent))
from config.scrape_config_racetable import *

scrape_config_jbcsprint2023_racetrack = "大井"

# 対象レース及び参考レースの情報
scrape_config_horse_race_jbcsprint2023_lists = [
    # 開催日付、開催レース、開催レースの馬idリスト、予想対象レースかどうか
    ["2022/11/03", "JBCSPRINT_2022", horse_id_list_2022_jbcsprint, False],
    ["2021/11/03", "JBCSPRINT_2021", horse_id_list_2021_jbcsprint, False],
    ["2020/11/03", "JBCSPRINT_2020", horse_id_list_2020_jbcsprint, False],
    ["2019/11/04", "JBCCPRINT_2019", horse_id_list_2019_jbcsprint, False],
    ["2018/11/04", "JBCSPRINT_2018", horse_id_list_2018_jbcsprint, False],
    ["2017/11/03", "JBCSPRINT_2017", horse_id_list_2017_jbcsprint, False],
    ["2016/11/03", "JBCSPRINT_2016", horse_id_list_2016_jbcsprint, False],
    ["2015/11/03", "JBCSPRINT_2015", horse_id_list_2015_jbcsprint, False],
    ["2014/11/03", "JBCSPRINT_2014", horse_id_list_2014_jbcsprint, False],
    ["2013/11/04", "JBCSPRINT_2013", horse_id_list_2013_jbcsprint, False],
]

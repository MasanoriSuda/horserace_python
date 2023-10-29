# pytorch
import torch
import torch.nn as nn
import torch.optim as optim

from enum import Enum

# 自作ライブラリ
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
print(str(Path(__file__).resolve().parent.parent))
from config.jbcclassic2023.scrape_config_train_test_objectrace import (
    scrape_config_horse_race_jbcclassic2023_lists,
    scrape_config_jbcclassic2023_racetrack,
)
from config.jbcsprint2023.scrape_config_train_test_objectrace import (
    scrape_config_horse_race_jbcsprint2023_lists,
    scrape_config_jbcsprint2023_racetrack,
)


class Scrape_Race(Enum):
    JBCCLASSIC2023 = 0
    JBCSPRINT2023 = 1
    JBCLADIESCLASSIC2023 = 2
    JBC2NDCLASSIC2023 = 3


def scrapeconfiggetobjectrace():
    return Scrape_Race.JBCCLASSIC2023.value


scrape_race_eval_list = [
    [
        scrape_config_horse_race_jbcclassic2023_lists,
        scrape_config_jbcclassic2023_racetrack,
    ],
    [
        scrape_config_horse_race_jbcsprint2023_lists,
        scrape_config_jbcsprint2023_racetrack,
    ],
]

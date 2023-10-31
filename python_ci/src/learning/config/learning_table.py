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

from config.jbcclassic2023.learning_config_evallist import evalsample_jbcclassic2023
from config.jbcclassic2023.learning_racelists import (
    race_for_learing_train_lists_jbcclassic2023,
    race_for_learing_test_lists_jbcclassic2023,
    race_for_learing_eval_lists_jbcclassic2023,
)
from config.jbcsprint2023.learning_config_evallist import evalsample_jbcsprint2023
from config.jbcsprint2023.learning_racelists import (
    race_for_learing_train_lists_jbcsprint2023,
)


class Learning_Race(Enum):
    JBCCLASSIC2023 = 0
    JBCSPRINT2023 = 1
    JBCLADIESCLASSIC2023 = 2
    JBCC2NDLASSIC2023 = 3


learning_race_eval_list = [
    [
        race_for_learing_train_lists_jbcclassic2023,
        race_for_learing_test_lists_jbcclassic2023,
        race_for_learing_eval_lists_jbcclassic2023,
    ],
    [
        race_for_learing_train_lists_jbcsprint2023,
        race_for_learing_train_lists_jbcsprint2023,
        race_for_learing_train_lists_jbcsprint2023,
    ],
]


def leaningconfigobjctrace():
    return Learning_Race.JBCCLASSIC2023.value

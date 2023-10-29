import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# pytorch
import torch
import torch.nn as nn
import torch.optim as optim

# 自作ライブラリ
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
print(str(Path(__file__).resolve().parent.parent))
from config.learning_table import (
    learning_race_eval_list,
    Learning_Race,
    leaningconfigobjctrace,
)

race_all_lists_test = pd.DataFrame()


"""_summary_
"""


def learning_getnnmodel():
    net = nn.Sequential(
        nn.Linear(22, 256),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(256, 128),
        nn.ReLU(),
        nn.Linear(128, 2),
    )

    return net


"""_summary_
"""


def learning_tuningdfparam(df):
    jbc_all_lists_tmp = df

    print(df)

    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="odds")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="date")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="weight_incdec")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="3furlong")
    # jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='distance')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="horse_weight")

    f_horsediv = lambda x: (x - 1980000000) / 1000000
    jbc_all_lists_tmp["horse_id"] = jbc_all_lists_tmp["horse_id"].apply(f_horsediv)

    f_distancediv = lambda x: x / 100
    jbc_all_lists_tmp["distance"] = jbc_all_lists_tmp["distance"].apply(f_distancediv)

    f_money = lambda x: x / 100
    jbc_all_lists_tmp["money"] = jbc_all_lists_tmp["money"].apply(f_money)

    f_dateda = lambda x: x / 100
    jbc_all_lists_tmp["dateforda"] = jbc_all_lists_tmp["dateforda"].apply(f_dateda)

    get_odd_even = lambda x: (10000 + x) / 100 if x % 2 == 0 else x / 100
    #    get_odd_even = lambda x: x / 100
    jbc_all_lists_tmp["jockey"] = jbc_all_lists_tmp["jockey"].apply(get_odd_even)

    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="money")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="order_complex")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="horse_id")
    # jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='time')
    # jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='weight')
    # jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='jockey')

    return jbc_all_lists_tmp


def learning_geevaldata():
    """_summary_"""
    jbc_all_lists_tmp = pd.DataFrame()

    try:
        horse_info_new_path = "./python_ci/csv/learning/test_JBCCLASSIC_2023.csv"
        try:
            jbc_2021_df = pd.read_csv(horse_info_new_path, index_col=0)
        except:
            assert False

        jbc_2021_df = learning_tuningdfparam(jbc_2021_df)

        jbc_all_lists_tmp = jbc_all_lists_tmp.append(jbc_2021_df)
    except:
        print("file not found")

    horse_info_new_path = "./python_ci/csv/learning/JBC_evaldata.csv"

    try:
        jbc_all_lists_tmp = pd.read_csv(horse_info_new_path, index_col=0)
    except:
        assert False

    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="order")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="money")
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns="horse_id")

    print("hoge")
    print(jbc_all_lists_tmp)

    return jbc_all_lists_tmp


def learning_settrainandtestdata(race_idx, train_or_test_or_eval):
    """_summary_"""
    jbc_all_lists_tmp = pd.DataFrame()
    if train_or_test_or_eval == 0:
        TRAIN_OR_TEST = "train_"
    elif train_or_test_or_eval == 1:
        TRAIN_OR_TEST = "test_"
    if train_or_test_or_eval == 0 or train_or_test_or_eval == 1:
        for list in learning_race_eval_list[race_idx][0]:
            try:
                horse_info_new_path = (
                    "./python_ci/csv/learning/" + TRAIN_OR_TEST + list + ".csv"
                )
                jbc_2021_df = pd.read_csv(horse_info_new_path, index_col=0)

                jbc_all_lists_tmp = jbc_all_lists_tmp.append(jbc_2021_df)
            except:
                print("file not found")
    else:
        try:
            horse_info_new_path = (
                "./python_ci/csv/learning/" + TRAIN_OR_TEST + list + ".csv"
            )
            jbc_2021_df = pd.read_csv(horse_info_new_path, index_col=0)

            jbc_all_lists_tmp = jbc_all_lists_tmp.append(jbc_2021_df)
        except:
            print("file not found")

    horse_info_new_path = "./python_ci/csv/learning/" + TRAIN_OR_TEST + "JBC_CATALL.csv"

    jbc_all_lists_tmp.to_csv(horse_info_new_path)

    jbc_all_lists = learning_tuningdfparam(jbc_all_lists_tmp)

    print(len(jbc_all_lists))
    print(jbc_all_lists)

    if train_or_test_or_eval == 0:
        t_train = torch.Tensor(jbc_all_lists["order"].values.astype(np.int64))
        x_train = torch.Tensor(
            jbc_all_lists.drop("order", axis=1).values.astype(np.float32)
        )
    else:
        t_test = torch.Tensor(jbc_all_lists["order"].values.astype(np.int64))
        x_test = torch.Tensor(
            jbc_all_lists.drop("order", axis=1).values.astype(np.float32)
        )

    if train_or_test_or_eval == 0:
        return t_train, x_train, jbc_all_lists
    elif train_or_test_or_eval == 1:
        return t_test, x_test, jbc_all_lists


# 参考
# https://qiita.com/__Rossi__/items/a0ea3a8d6e24d0755737
def learning_exec(race_idx):
    """_summary_"""
    df_eval = learning_geevaldata()

    t_train, x_train, race_all_lists_train = learning_settrainandtestdata(race_idx, 0)
    t_test, x_test, race_all_lists_test = learning_settrainandtestdata(race_idx, 1)

    # numpyからtensorに変換
    x_train = torch.tensor(x_train, dtype=torch.float32)
    t_train = torch.tensor(t_train, dtype=torch.int64)
    x_test = torch.tensor(x_test, dtype=torch.float32)
    t_test = torch.tensor(t_test, dtype=torch.int64)

    # シードを固定
    torch.manual_seed(1000)

    net = learning_getnnmodel()

    net.train()  # 学習モードに切り替え

    # 交差エントロピー誤差関数
    loss_fnc = nn.CrossEntropyLoss()

    # SGD
    optimizer = optim.SGD(net.parameters(), lr=0.01)  # 学習率は0.05

    # 損失のログ
    record_loss_train = []
    record_loss_test = []

    # 1000エポック学習
    for i in range(1000):
        # 勾配を0に
        optimizer.zero_grad()

        # 順伝播
        y_train = net(x_train)
        y_test = net(x_test)

        # 誤差を求める
        loss_train = loss_fnc(y_train, t_train)
        loss_test = loss_fnc(y_test, t_test)
        record_loss_train.append(loss_train.item())
        record_loss_test.append(loss_test.item())

        # 逆伝播（勾配を求める）
        loss_train.backward()

        # パラメータの更新
        optimizer.step()

        if i % 100 == 0:
            print(
                "Epoch:",
                i,
                "Loss_Train:",
                loss_train.item(),
                "Loss_Test:",
                loss_test.item(),
            )

    y_test = net(x_test)
    # print(y_test)
    count = (y_test.argmax(1) == t_test).sum().item()
    print("正解率:", str(count / len(y_test) * 100) + "%")

    # ネットワークを推論モードに切り替え
    net.eval()

    for index, row in df_eval.iterrows():
        # データをPyTorch Tensorに変換
        data_point_tensor = torch.Tensor(row.values.astype(np.float32))

        # 推論を実行
        y_test2 = net(data_point_tensor)

        # ソフトマックス関数を適用
        y_test2 = y_test2.softmax(dim=0)

        # クラス0およびクラス1の確率を取得
        prob_class_0 = y_test2[0].item()
        prob_class_1 = y_test2[1].item()

        # 結果を出力
        print("[0.1]:=[" + str(prob_class_0) + "," + str(prob_class_1) + "]")

    print(list)

    jbc_all_lists_test_tmp2 = race_all_lists_test[["age", "order"]]

    age_order_totals = jbc_all_lists_test_tmp2.groupby("age")["order"].mean()

    age_order_totals.plot(kind="bar")
    plt.xlabel("Age")
    plt.ylabel("Total Orders")
    plt.title("Total Orders by Age")
    plt.show()


def learning_getobjectreace():
    """_summary_

    Returns:
        _type_: _description_
    """
    return leaningconfigobjctrace()


def main():
    race_idx = learning_getobjectreace()
    learning_exec(race_idx)


if __name__ == "__main__":
    main()

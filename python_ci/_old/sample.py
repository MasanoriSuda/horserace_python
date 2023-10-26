import pandas as pd
from pandas import Series,DataFrame
import numpy as np

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt

##CSVデータをPythonを使って読み込み
wine_data_set = pd.read_csv("last10years.csv",sep=",",header=0)
print(DataFrame(wine_data_set).head())

##説明変数の設定
print("-----説明変数--------")
setsumei = DataFrame(wine_data_set.drop("result",axis=1))
print(setsumei.head(10))

##目的変数の設定
print("-----目的変数-------")
mokuteki = DataFrame(wine_data_set["result"])
print(mokuteki.head(10))

##訓練データとテストデータの分割
setsumei_train,setsumei_test,mokuteki_train,mokuteki_test = train_test_split(setsumei,mokuteki,test_size=0.3)
print("-----訓練データとテストデータの分割--------")
print("-----説明変数 訓練データ--------")
print(setsumei_train.shape)
print(setsumei_train.head())
print("-----説明変数 テストデータ--------")
print(setsumei_test.shape)
print(setsumei_test.head())
print("-----目的変数 訓練データ--------")
print(mokuteki_test.shape)
print(setsumei_test.head())
print("-----目的変数 テストデータ--------")
print(mokuteki_train.shape)
print(mokuteki_train.head())
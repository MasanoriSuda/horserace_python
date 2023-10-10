#モジュールの読み込み
from __future__ import print_function

import pandas as pd
from pandas import Series,DataFrame

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import numpy as np
import matplotlib.pyplot as plt

import keras
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.optimizers import Adam

out_data = [1,2,3,4,5,6,7,8,9,10,11,12,13]
out_data = np.array(out_data)
#CSVファイルの読み込み
wine_data_set = pd.read_csv("last10years.csv",sep=",",header=0)

#説明変数(ワインに含まれる成分)
x = DataFrame(wine_data_set.drop("result",axis=1))

#目的変数(各ワインの品質を10段階評価したもの)
y = DataFrame(wine_data_set["result"])

#説明変数・目的変数をそれぞれ訓練データ・テストデータに分割
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.05)


#データの整形
x_train = x_train.astype(np.float32)
x_test = x_test.astype(np.float32)
y_train = y_train.astype(np.float32)
y_test = y_test.astype(np.float32)

#y_train = keras.utils.to_categorical(out_data,np.max(out_data)+1)
#y_test = keras.utils.to_categorical(out_data,np.max(out_data)+1)


#ニューラルネットワークの実装①
model = Sequential()

model.add(Dense(50, activation='relu', input_shape=(17,)))
model.add(Dropout(0.2))

model.add(Dense(50, activation='relu', input_shape=(17,)))
model.add(Dropout(0.2))

model.add(Dense(50, activation='relu', input_shape=(17,)))
model.add(Dropout(0.2))

model.add(Dense(14, activation='softmax'))

model.summary()
print("\n")

#ニューラルネットワークの実装②
model.compile(loss='mean_squared_error',optimizer=RMSprop(),metrics=['accuracy'])
#勾配法には、Adam(lr=1e-3)という方法もある（らしい）。

#ニューラルネットワークの学習
history = model.fit(x_train, y_train,batch_size=558,epochs=40,verbose=1,validation_data=(x_test, y_test))

#ニューラルネットワークの推論
score = model.evaluate(x_test,y_test,verbose=1)
print("\n")
print("Test loss:",score[0])
print("Test accuracy:",score[1])

#評価したい馬の情報を設定
#前走(鎌倉記念)
#sample = [[1.0,  2.0,  45.0,  4.0,  11.0,  1.0,  4.9,  3.0,  5342.0,  55.0,  2.0,  1500.0,  4.0,  97.6,  40.0,  440.0, -8.0]] #パンセ(7)
#sample =  [[1.0,  2.0,  30.0,  3.0,  12.0,  4.0,  1.8,  1.0,  5286.0,  54.0,  2.0,  1700.0,  3.0,  111.3,  41.1,  496.0,  6.0]] #サンノトーレ(4)
#sample  = [[1.0,  2.0,  45.0,  4.0,  11.0,  3.0,  1.8,  1.0,  5365.0,  55.0,  2.0,  1500.0,  4.0,  97.8,  40.5,  490.0, -4.0]] #アジアミッション(2)(4)
#sample  =  [[1.0,  2.0,  45.0,  4.0,  2.0,  9.0,  9.6,  5.0,   5365.0,  54.0,  2.0,  1400.0,  4.0,  92.2,  40.1,  459.0,   10.0]]#カルタシス(3)
#sample  = [[1.0,  2.0,  42.0,  4.0,  11.0,  12.0,  1.5,  1.0,  5365.0,  54.0,  2.0,  1400.0,  4.0,  89.0,  39.6,  535.0,  7.0]]#アムクラージュ(2)(3)
#sample  =  [[1.0,  2.0,  30.0,  3.0,   4.0,   3.0,  2.5,  1.0,  5492.0,  54.0,  2.0,  1000.0,  3.0,  61.4,  37.0,  456.0,  0.0]]#スノーシュー(5)
#sample  =  [[1.0,  2.0,  45.0,  4.0,  11.0,  6.0,  7.4,  4.0,    5524.0,  55.0,  2.0,  1500.0,  4.0,  98.2,  40.9,  450.0,  12.0]]#ホークマン(13)
#sample  =   [[1.0,  2.0,  43.0,  4.0,  4.0,  5.0,  2.5,  2.0,  5549.0,  54.0,  2.0,  1500.0,  4.0,  98.7,  40.8,  512.0,  0.0]]#メイプルケンジ(9)
#sample  =  [[1.0,  2.0,  44.0,  3.0,  5.0,  1.0,  3.4,  2.0,    5399.0,  54.0,  2.0,  1400.0,  4.0,  90.5,  40.7,  468.0, -2.0]]#エドノビートイン(8)
#sample  =  [[1.0,  2.0,  42.0,  4.0,  11.0,  5.0,  3.0,  2.0,  5342.0,  54.0,  2.0,  1400.0,  4.0,  91.2,  42.0,  476.0,  19.0]]#ライゾマティクス(10)
#sample   =  [[1.0,  2.0,  44.0,  3.0,  11.0,   9.0,  28.4,  7.0,  5630.0,  54.0,  2.0,  1200.0,  4.0,  73.2,  38.4,  450.0,  0.0]]#モンゲースパイ(9)
#sample =     [[1.0,  2.0,  45.0,  4.0,  11.0,  7.0,  3.0,  1.0,  5399.0,  55.0,  2.0,  1500.0,  4.0,  97.5,  40.4,  477.0, 2.0]] #パンセ(7)


#sample =[[1.0,  2.0,  30.0,  3.0,  12.0,  4.0,  137.3,  10.0,    9004.0,  54.0,  2.0,  1600.0,  2.0,  107.7,  44.2,  468.0,   0.0]] #(1)
#sample =[[1.0,  2.0,  30.0,  3.0,  12.0,  3.0,   61.3,   9.0,    5578.0,  54.0,  2.0,  1600.0,  2.0,  107.8,  44.1,  480.0,   2.0]] #(4)
#sample =[[1.0,  2.0,  30.0,  4.0,  8.0 ,  3.0,   11.6,   5.0,    9005.0,  55.0,  2.0,  1700.0,  3.0,  114.7,  40.0,  442.0,   8.0]] #(2)
#sample =[[1.0,  2.0,  30.0,  3.0,  6.0 ,  6.0,    3.6,   2.0,    5592.0,  56.0,  2.0,  1600.0,  4.0,  105.4,  40.4,  462.0,   6.0]] #(4)
#sample =[[1.0,  2.0,  30.0,  3.0,  12.0,  2.0,   11.3,   4.0,    5477.0,  54.0,  2.0,  1600.0,  2.0,  108.3,  45.0,  458.0,  10.0]] #(9)
#sample =[[1.0,  2.0,  30.0,  3.0,  5.0 ,  4.0,    7.2,   3.0,    5411.0,  54.0,  2.0,  1000.0,  4.0,   62.3,  37.7,  484.0,  -2.0]] #(6)
#sample =[[1.0,  2.0,  30.0,  3.0,  12.0,  1.0,   18.6,   5.0,    5492.0,  54.0,  2.0,  1600.0,  2.0,  108.2,  44.1,  450.0,   4.0]] #(13)
#sample =[[1.0,  2.0,  30.0,  3.0,  12.0,  7.0,    5.3,   3.0,    9006.0,  54.0,  2.0,  1600.0,  2.0,  106.9,  43.0,  414.0,   4.0]] #(6)
#sample =[[1.0,  2.0,  30.0,  3.0,  9.0 ,  3.0,  103.8,  10.0,    5502.0,  54.0,  2.0,  1700.0,  4.0,  112.9,  40.5,  450.0,   2.0]] #(10)
#sample =[[1.0,  2.0,  30.0,  3.0,  9.0 ,  8.0,   16.6,   6.0,    5492.0,  54.0,  2.0,  1500.0,  2.0,  101.5,  43.6,  438.0,  -4.0]] #(1)
sample =[[1.0,  2.0,  30.0,  3.0,  12.0,  9.0,   36.1,   7.0,    5502.0,  54.0,  2.0,  1600.0,  2.0,  107.3,  43.4,  456.0,  -2.0]] #(13)






print("\n")
print("--馬のデータ--")

print(sample)

#ポイント：ワインの成分をNumpyのArrayにしないとエラーが出る
sample = np.array(sample)
y_prob = model.predict(sample)
y_pred = np.argmax(y_prob, axis=1)

print("\n")
print("--予測着順--")
print(y_pred)
print("\n")


#学習履歴のグラフ化に関する参考資料
#http://aidiary.hatenablog.com/entry/20161109/1478696865

def plot_history(history):
    # print(history.history.keys())
    
    # 精度の履歴をプロット
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend(['acc', 'val_acc'], loc='lower right')
    plt.show()
    
    # 損失の履歴をプロット
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['loss', 'val_loss'], loc='lower right')
    plt.show()

# 学習履歴をプロット
plot_history(history)

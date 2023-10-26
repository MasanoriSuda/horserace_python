import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# pytorch
import torch
import torch.nn as nn
import torch.optim as optim

#自作ライブラリ
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
print(str(Path(__file__).resolve().parent.parent))
from config.learning_racelists import race_for_learing_lists

#参考
#https://qiita.com/__Rossi__/items/a0ea3a8d6e24d0755737

jbc_all_lists_train = pd.DataFrame()
jbc_all_lists_test = pd.DataFrame()

for train_or_test in range (0,2):
    if(train_or_test == 0):
        jbc_all_lists_tmp = jbc_all_lists_train
        TRAIN_OR_TEST = 'train_'
    else:
        jbc_all_lists_tmp = jbc_all_lists_test
        TRAIN_OR_TEST = 'test_'
    for list in race_for_learing_lists:
        try:
            horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+TRAIN_OR_TEST+list+'.csv'
            jbc_2021_df = pd.read_csv(horse_info_new_path,index_col=0)
            #print(jbc_2021_df)

            jbc_all_lists_tmp = jbc_all_lists_tmp.append(jbc_2021_df)
        except:
            print("file not found")

        df = jbc_all_lists_tmp
        #print(df[df.isna().any(axis=1)].loc[:, df.isna().any()])

    horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+TRAIN_OR_TEST+'JBC_CATALL.csv'

    jbc_all_lists_tmp.to_csv(horse_info_new_path)

    if(train_or_test == 1):
        jbc_all_lists_test = jbc_all_lists_tmp

    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='horse_id')
    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='jockey')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='odds')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='date')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='weight_incdec')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='3furlong')
    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='distance')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='horse_weight')

    #print(jbc_all_lists_tmp)

    f_horsediv = lambda x: x / 10000000
    jbc_all_lists_tmp['horse_id'] = jbc_all_lists_tmp['horse_id'].apply(f_horsediv)

    f_distancediv = lambda x: x / 100
    jbc_all_lists_tmp['distance'] = jbc_all_lists_tmp['distance'].apply(f_distancediv)

    f_money = lambda x: x / 100
    jbc_all_lists_tmp['money'] = jbc_all_lists_tmp['money'].apply(f_money)

    f_dateda = lambda x: x / 100
    jbc_all_lists_tmp['dateforda'] = jbc_all_lists_tmp['dateforda'].apply(f_dateda)

    get_odd_even = lambda x: (10000 + x) / 100 if x % 2 == 0 else x / 100
#    get_odd_even = lambda x: x / 100
    jbc_all_lists_tmp['jockey'] = jbc_all_lists_tmp['jockey'].apply(get_odd_even)

    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='money')
    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='time')
    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='weight')
    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='jockey')

    jbc_all_lists = jbc_all_lists_tmp

    print(jbc_all_lists)

    if train_or_test == 0:
        t_train = torch.Tensor(jbc_all_lists['order'].values.astype(np.int64))
        x_train = torch.Tensor(jbc_all_lists.drop('order', axis=1).values.astype(np.float32))
    else:
        t_test = torch.Tensor(jbc_all_lists['order'].values.astype(np.int64))
        x_test = torch.Tensor(jbc_all_lists.drop('order', axis=1).values.astype(np.float32))

# numpyからtensorに変換
x_train = torch.tensor(x_train, dtype=torch.float32)
t_train = torch.tensor(t_train, dtype=torch.int64) 
x_test = torch.tensor(x_test, dtype=torch.float32)
t_test = torch.tensor(t_test, dtype=torch.int64) 

# シードを固定
torch.manual_seed(100)

net = nn.Sequential(
    nn.Linear(24 ,128),  
    nn.ReLU(),
    nn.Linear(128 ,64),  
    nn.ReLU(),  
    nn.Linear(64 ,32),  
    nn.ReLU(),  
    nn.Linear(32 ,16), 
    nn.ReLU(), 
    nn.Linear(16 ,8), 
    nn.ReLU(),      
    nn.Linear(8 ,4),     
    nn.ReLU(),          
    nn.Linear(4, 2)
)
net.train() #学習モードに切り替え

# 交差エントロピー誤差関数
loss_fnc = nn.CrossEntropyLoss()

# SGD
optimizer = optim.SGD(net.parameters(), lr=0.01)  # 学習率は0.01

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

    if i%100 == 0:
        print("Epoch:", i, "Loss_Train:", loss_train.item(), "Loss_Test:", loss_test.item())

y_test = net(x_test)
#print(y_test)
count = (y_test.argmax(1) == t_test).sum().item()
print("正解率:", str(count/len(y_test)*100) + "%")

sample = torch.tensor([
    # horse_id    sex  age  dateforda  track  weather  race_num  horse_num_anim  horse_num  popularity  order_complex        jockey  weight  dirt_grass  distance  condition time  same_track  g1_age3  g2_age3  g3_age3  g1_age4  g2_age4  g3_age4
    [201.9102383, 3,    4,     84.58,     44,       5,      11,              16,         1,          1,             1,       10.88,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.9103943, 3,    4,     84.13,     44,       5,      11,              16,         1,          1,             1,       10.88,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.8101012, 3,    5,     84.62,     44,       5,      11,              16,         1,          1,             1,        6.66,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.6100349, 3,    7,     84.58,     44,       5,      11,              16,         1,          1,             1,       11.16,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.7101010, 3,    6,     83.67,     44,       5,      11,              16,         1,          1,             1,       11.26,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.9101623, 3,    4,     84.72,     44,       5,      11,              16,         1,          1,             1,        6.66,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.7106404, 3,    6,     83.67,     44,       5,      11,              16,         1,          1,             1,       11.15,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.7105356, 3,    6,     84.38,     44,       5,      11,              16,         1,          1,             1,       55.24,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.4100370, 3,    9,     84.84,     44,       5,      11,              16,         1,          1,             1,           0,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.5104526, 3,    8,     84.59,     44,       5,      11,              16,         1,          1,             1,       53.42,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.8106265, 3,    5,     84.58,     44,       5,      11,              16,         1,          1,             1,     6558.45,     57,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [201.6105047, 3,    9,     84.85,     44,       5,      11,              16,         1,          1,             1,           0,     55,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [202.0104196, 3,    3,     84.46,     44,       5,      11,              16,         1,          1,             1,       53.42,     55,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
    [202.0100349, 3,    3,     84.64,     44,       5,      11,              16,         1,          1,             1,       52.99,     55,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
	[202.0104376, 3,    3,     84.64,     44,       5,      11,              16,         1,          1,             1,       54.04,     55,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],
	[201.8104021, 3,    5,     84.60,     44,	    5,	    11,	             16,	     1,	         1,	            1,       53.28,	    55,          2,     20.0,         4,    1,      0,       0,       0,       0,       1,       0,       0],

    ],dtype=torch.float32)

net.eval() #推論モードに切り替え
for i in range (0,16):
    y_test2 = net(sample[i])
    y_test2 = y_test2.softmax(dim=0)
    print(y_test2)

jbc_all_lists_test_tmp = jbc_all_lists_test[['age','order']]

age_order_totals = jbc_all_lists_test_tmp.groupby('age')['order'].mean()

age_order_totals.plot(kind='bar')
plt.xlabel('Age')
plt.ylabel('Total Orders')
plt.title('Total Orders by Age')
plt.show()
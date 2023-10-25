import pandas as pd
import numpy as np

# pytorch
import torch
import torch.nn as nn
import torch.optim as optim

#参考
#https://qiita.com/__Rossi__/items/a0ea3a8d6e24d0755737

lists =[
    "CHAMPIONSCUP_2018",
    "CHAMPIONSCUP_2019",
    "CHAMPIONSCUP_2020",
    "CHAMPIONSCUP_2021",
    "CHAMPIONSCUP_2022",    
    "TEIOU_2014", 
    "TEIOU_2015", 
    "TEIOU_2016", 
    "TEIOU_2017", 
    "TEIOU_2018", 
    "TEIOU_2019", 
    "TEIOU_2020", 
    "TEIOU_2021", 
    "TEIOU_2022", 
    "TEIOU_2023",
    "JBCCLASSIC_2013",
    "JBCCLASSIC_2014",
    "JBCCLASSIC_2015",
    "JBCCLASSIC_2016",
    "JBCCLASSIC_2017",
    "JBCCLASSIC_2018",
    "JBCCLASSIC_2019",            
    "JBCCLASSIC_2020",
    "JBCCLASSIC_2021",
    "JBCCLASSIC_2022",
    "DAISHOUTEN_2013",
    "DAISHOUTEN_2014",
    "DAISHOUTEN_2015",
    "DAISHOUTEN_2016",
    "DAISHOUTEN_2017",
    "DAISHOUTEN_2018",
    "DAISHOUTEN_2019",
    "DAISHOUTEN_2020",
    "DAISHOUTEN_2021",
    "DAISHOUTEN_2022",
    "KAWASAKI_2021",
    "KAWASAKI_2022",
    "KAWASAKI_2023",
    'JBCCLASSIC_2023',
]

jbc_all_lists_train = pd.DataFrame()
jbc_all_lists_test = pd.DataFrame()

for train_or_test in range (0,2):
    if(train_or_test == 0):
        jbc_all_lists_tmp = jbc_all_lists_train
        TRAIN_OR_TEST = 'train_'
    else:
        jbc_all_lists_tmp = jbc_all_lists_test
        TRAIN_OR_TEST = 'test_'
    for list in lists:
        try:
            horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/'+TRAIN_OR_TEST+list+'.csv'
            jbc_2021_df = pd.read_csv(horse_info_new_path,index_col=0)
            #print(jbc_2021_df)

            jbc_all_lists_tmp = jbc_all_lists_tmp.append(jbc_2021_df)
        except:
            print("file not found")

    horse_info_new_path ='/home/msuda/workspace/vscode/horserace/python_ci/csv/horse_id_new/JBC2022/JBC_CATALL.csv'

    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='horse_id')
    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='jockey')
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

    f_jockey = lambda x: x / 100
    jbc_all_lists_tmp['jockey'] = jbc_all_lists_tmp['jockey'].apply(f_jockey)

    f_money = lambda x: x / 100
    jbc_all_lists_tmp['money'] = jbc_all_lists_tmp['money'].apply(f_money)

    f_dateda = lambda x: x / 100
    jbc_all_lists_tmp['dateforda'] = jbc_all_lists_tmp['dateforda'].apply(f_dateda)

    get_odd_even = lambda x: 10000 + x if x % 2 == 0 else x
    f_dateda = lambda x: x / 100
    jbc_all_lists_tmp['jockey'] = jbc_all_lists_tmp['jockey'].apply(f_dateda)

    #jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='horse_id')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='money')
    jbc_all_lists_tmp = jbc_all_lists_tmp.drop(columns='time')
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
    nn.Linear(23 ,128),  
    nn.ReLU(),
    nn.Linear(128 ,128),  
    nn.ReLU(),
    nn.Linear(128 ,128),  
    nn.ReLU(),  
    nn.Linear(128 ,32),  
    nn.ReLU(),          
    nn.Linear(32, 8),
    nn.ReLU(),
    nn.Linear(8, 2)
)
net.train() #学習モードに切り替え

# 交差エントロピー誤差関数
loss_fnc = nn.CrossEntropyLoss()

# SGD
optimizer = optim.SGD(net.parameters(), lr=0.1)  # 学習率は0.01

# 損失のログ
record_loss_train = []
record_loss_test = []

# 1000エポック学習
for i in range(2000):

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
    [ 202.0104376    ,3   ,3     ,85.00,45       ,6      ,11.0             ,15         ,2    ,1.0         ,1.0        ,54.04    ,55.0          ,2      ,20.0         ,4            ,1       ,0       ,0       ,0       ,1       ,0       ,0],     
    ],dtype=torch.float32)

net.eval() #推論モードに切り替え
for i in range (0,1):
    y_test2 = net(sample[i])
    y_test2 = y_test2.softmax(dim=0)
    print(y_test2)

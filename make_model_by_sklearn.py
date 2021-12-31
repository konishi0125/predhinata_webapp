import os
import numpy as np
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import pickle

name_list = pd.read_csv("./member_list.csv")
name_list = name_list["name"].values.tolist()


def make_model_by_random_forest(x, y, max_depth_=13, n_estimators_=17):
    '''
    ランダムフォレスト
    モデル重くなるから非推奨
    '''
    x_train, x_test, y_train, y_test =\
        train_test_split(x, y, random_state=0, train_size=0.8)
    random_forest = RandomForestClassifier(max_depth=max_depth_, n_estimators=int(n_estimators_))
    random_forest.fit(x_train, y_train)
    y_pred = random_forest.predict(x_test)
    print(accuracy_score(y_test, y_pred))
    return random_forest

def make_model_by_perceptron(x, y):
    '''
    パーセプトロン
    '''
    x_train, x_test, y_train, y_test =\
        train_test_split(x, y, random_state=0, train_size=0.8)
    ppt = Perceptron()
    ppt.fit(x_train, y_train)
    y_pred = ppt.predict(x_test)
    print(accuracy_score(y_test, y_pred))
    return ppt

def make_model_by_SVC(x, y):
    '''
    サポートベクターマシン
    '''
    x_train, x_test, y_train, y_test =\
        train_test_split(x, y, random_state=0, train_size=0.8)
    svc = SVC(probability=True)
    svc.fit(x_train, y_train)
    y_pred = svc.predict(x_test)
    print(accuracy_score(y_test, y_pred))
    return svc

'''
x:(n,128) type np.array 
   face_recognition.encordingsで圧縮した特徴量の行列
   nは教師画像の枚数
y:(n) type np.array
   正解のラベル
   [りんご、バナナ、メロン]で画像がりんごなら0、バナナなら1、メロンなら2
'''
data = np.load("./pic_numpy/face_recognition_pic.npz", allow_pickle=True)
x = data["arr_0"]
y = data["arr_1"]
'''
元のyデータがone hotベクトルだったから変換している
例：(1,0,0)→0 (0,0,1)→2
'''
y_ = []
for y_ind in y:
    y_.append(y_ind.argmax())
y = np.array(y_)

print('loading data finished')

'''
学習
非線形のサポートベクターマシン
'''
model = make_model_by_SVC(x, y)
filename='./model/SVC_hinata_model.sav'
pickle.dump(model, open(filename, 'wb'))
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
import numpy as np
import cv2
import pandas as pd
import face_recognition
import os
import time
import pickle
import csv

SAVE_DIR = "./tmp"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_folder='tmp')

csv_file = open("./member_list.csv", "r", encoding="utf-8")
reader = csv.reader(csv_file, delimiter=",")
name_list = []
ja_name_list = []
for row in reader:
    name_list.append(row[1])
    ja_name_list.append(row[2])
name_list = name_list[1:]
ja_name_list = ja_name_list[1:]


@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/good')
def good():
    return 'aaa'

@app.route('/result', methods=["get", "post"])
def result():
    img_path_list = []
    i = 0
    for file in request.files.getlist("avatar"):
        img = file.stream
        img_array = np.asarray(bytearray(img.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        face = face_recognition.face_locations(img)
        for top, right, bottom, left in face:
            t = round(time.time()*10000)
            save_path = f'{SAVE_DIR}/{t}.jpg'
            cv2.imwrite(save_path, img[top:bottom,left:right])
            img_path_list.append(t)

    return render_template('./choose_img.html', img_path_list=img_path_list)

def get_ranking(similar_list, n=3):
    '''
    似ているメンバーのランキング表示
    '''
    similar_list = np.mean(similar_list, axis=0)
    m_list = []
    per_list = []
    for i in range(n):
        n = i+1
        m = ja_name_list[similar_list.argsort()[-n]]
        per = round(similar_list[similar_list.argsort()[-n]]*100)
        m_list.append(m)
        per_list.append(per)
    return m_list, per_list, n

@app.route('/pred', methods=["get", "post"])
def pred():
    path_list = request.form.getlist('img')
    for i in range(len(path_list)):
        img = face_recognition.load_image_file(f'{SAVE_DIR}/{path_list[i]}.jpg')
        cnv = face_recognition.face_encodings(img,\
            known_face_locations=[(0,img.shape[1],img.shape[0],0)])
        if i == 0:
            cnv_list = cnv[0]
        else:
            cnv_list = np.concatenate([cnv_list, cnv[0]])
    cnv_list = cnv_list.reshape((len(path_list),128))

    model = pickle.load(open('./model/SVC_hinata_model.sav', 'rb'))
    #print(model.predict(cnv_list))
    result = model.predict_proba(cnv_list)
    m_list, per_list, n = get_ranking(result)
    #print(m_list, per_list)
    return render_template('./result.html', m_list=m_list, per_list=per_list, n=n)

if __name__ == '__main__':
    app.run(debug=True)

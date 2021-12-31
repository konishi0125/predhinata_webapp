# -*- coding: utf-8 -*-
import pickle
import time
from pathlib import Path

import cv2
import numpy as np
from face_recognition import face_encodings, face_locations, load_image_file
from flask import render_template, request

from predhinata import BASEDIR, SAVE_DIR, init_app

app, ja_name_list = init_app()


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/good')
def good():
    return 'aaa'


@app.route('/result', methods=["get", "post"])
def result():
    img_path_list = []
    for file in request.files.getlist("avatar"):
        img = file.stream
        img_array = np.asarray(bytearray(img.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        face = face_locations(img)
        for top, right, bottom, left in face:
            t = round(time.time()*10000)
            save_path = f'{SAVE_DIR}/{t}.jpg'
            cv2.imwrite(save_path, img[top:bottom, left:right])
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
        img = load_image_file(f'{SAVE_DIR}/{path_list[i]}.jpg')
        known_face_locations = [(0, img.shape[1], img.shape[0], 0)]
        cnv = face_encodings(img, known_face_locations=known_face_locations)
        if i == 0:
            cnv_list = cnv[0]
        else:
            cnv_list = np.concatenate([cnv_list, cnv[0]])
    cnv_list = cnv_list.reshape((len(path_list), 128))

    model_path = Path(BASEDIR, 'model/SVC_hinata_model.sav')
    model = pickle.load(model_path.open('rb'))
    # print(model.predict(cnv_list))
    result = model.predict_proba(cnv_list)
    m_list, per_list, n = get_ranking(result)
    # print(m_list, per_list)
    context = {'m_list': m_list,
               'per_list': per_list,
               'n': n}
    return render_template('./result.html', **context)


if __name__ == '__main__':
    app.run(debug=True)

# -*- coding: utf-8 -*-
import hashlib
import pickle
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from face_recognition import face_encodings, face_locations, load_image_file
from flask import (redirect, render_template, request, send_from_directory,
                   url_for)

from predhinata import MODEL_DIR, SAVE_DIR, SAVE_DIR_NAME, STATIC_DIR, init_app

app, ja_name_list = init_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(Path(STATIC_DIR, 'image'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/result', methods=["get", "post"])
def result():
    if request.method == 'GET':
        return redirect(url_for('index'))
    elif request.method == 'POST':
        img_path_list = []
        avatar_list = request.files.getlist("avatar")
        if len(avatar_list) > 0:
            if SAVE_DIR.exists() is False:
                SAVE_DIR.mkdir(parent=True)
        for file in request.files.getlist("avatar"):
            img = file.stream
            img_array = np.asarray(bytearray(img.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, 1)
            face = face_locations(img)
            for top, right, bottom, left in face:
                # https://qiita.com/lyrical_magical_girl/items/2bd432d6820ef446c947
                t = datetime.now()
                t_str = t.strftime('%Y/%m/%d %H:%M:%S %f')
                filename = hashlib.sha256(t_str.encode()).hexdigest() + '.jpg'
                save_path = f'{SAVE_DIR}/{filename}'
                cv2.imwrite(save_path, img[top:bottom, left:right])
                print(Path(SAVE_DIR_NAME, filename))
                img_path_list.append(Path(SAVE_DIR_NAME, filename))
        return render_template('choose_img.html', img_path_list=img_path_list)


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
    if request.method == 'GET':
        return redirect(url_for('index'))
    elif request.method == 'POST':
        path_list = request.form.getlist('img')
        for i in range(len(path_list)):
            img = load_image_file(f'{STATIC_DIR}/{path_list[i]}')
            known_face_locations = [(0, img.shape[1], img.shape[0], 0)]
            cnv = face_encodings(
                img, known_face_locations=known_face_locations)
            if i == 0:
                cnv_list = cnv[0]
            else:
                cnv_list = np.concatenate([cnv_list, cnv[0]])
        cnv_list = cnv_list.reshape((len(path_list), 128))

        model_path = Path(MODEL_DIR, 'SVC_hinata_model.sav')
        model = pickle.load(model_path.open('rb'))
        # print(model.predict(cnv_list))
        result = model.predict_proba(cnv_list)
        m_list, per_list, n = get_ranking(result)
        # print(m_list, per_list)
        context = {'m_list': m_list,
                   'per_list': per_list,
                   'n': n}
        return render_template('result.html', **context)


if __name__ == '__main__':
    app.run(debug=True)

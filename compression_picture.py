import glob

import numpy as np
from face_recognition import face_encodings, load_image_file

import member_list

"""
教師データは顔部分を切り出し名前ごとのフォルダーに分けられているものとする
教師データのフォルダ構成
PICTUR_FOLDER
|--member1
|  |--member1_picture1.jpg
|  |--member1_picture2.jpg
|  ...
|--member2
|  |...
|
|...
"""

PICTURE_FOLDER = "C:/Users/koni/python/hinata/data"


def to_feature(path):
    """画像のファイルパスを指定して128次元の特徴ベクトルに圧縮する
    :param path:画像ファイルのパス
    :return feature_vector:face_recognition.face_encodingsで圧縮した特徴量ベクトル
    """
    im = load_image_file(path)
    # 教師画像データはすでに顔部分を切り出しているため、顔の位置を画像サイズで指定する
    face_locations = [(0, im.shape[1], im.shape[0], 0)]
    feature_vector = face_encodings(im, known_face_locations=face_locations)[0]
    return feature_vector


def main():
    label = []
    feature = []
    for name in member_list.member_list["name"]:
        print(f"{name} compression...")
        path_list = glob.glob(f"{PICTURE_FOLDER}/{name}/*")
        for path in path_list:
            feature_vector = to_feature(path)
            label.append(name)
            feature.append(feature_vector)
    label = np.array(label)
    feature = np.array(feature)
    np.savez("./../hinata/npz/feature_vectors", label, feature)


if __name__ == "__main__":
    main()

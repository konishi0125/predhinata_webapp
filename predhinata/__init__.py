import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASEDIR = Path(__file__).parent.parent

ENV_PREFIX = 'PREDHINATA_WEBAPP_'

CONFFILE_NAME = os.environ.get(f'{ENV_PREFIX}CONFFILE', 'etc/flask.conf.json')
CONFFILE = Path(BASEDIR, CONFFILE_NAME)

TEMPLATE_DIR_NAME = os.environ.get(f'{ENV_PREFIX}TEMPLATEDIR', 'templates')
TEMPLATE_DIR = Path(BASEDIR, TEMPLATE_DIR_NAME)

STATIC_DIR_NAME = os.environ.get(f'{ENV_PREFIX}STATICDIR', 'static')
STATIC_DIR = Path(BASEDIR, STATIC_DIR_NAME)

SAVE_DIR_NAME = os.environ.get(f'{ENV_PREFIX}SAVEDIR', 'tmp')
SAVE_DIR = Path(STATIC_DIR, SAVE_DIR_NAME)

SAVE_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR_NAME = os.environ.get(f'{ENV_PREFIX}MODELDIR', 'model')
MODEL_DIR = Path(BASEDIR, MODEL_DIR_NAME)


def init_app():
    from flask import Flask
    app = Flask(__name__,
                static_folder=STATIC_DIR,
                template_folder=TEMPLATE_DIR)
    app.config.from_file(CONFFILE, load=json.load)
    csv_file = open("./member_list.csv", "r", encoding="utf-8")
    reader = csv.reader(csv_file, delimiter=",")
    name_list = []
    ja_name_list = []
    for row in reader:
        name_list.append(row[1])
        ja_name_list.append(row[2])
    name_list = name_list[1:]
    ja_name_list = ja_name_list[1:]
    return app, ja_name_list

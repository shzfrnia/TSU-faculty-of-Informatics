#!/usr/local/bin/python3
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import Config

TMP_PATH = os.path.normpath("tmp")

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

from app import routes

bootstrap = Bootstrap(app)

#!/usr/local/bin/python3
import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from app.config import Config

TMP_PATH = os.path.normpath("tmp")

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message_category = "info"
# lm.login_message = "GO GO GO"

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

from app import routes, models, errors

db.create_all() # for generate tables

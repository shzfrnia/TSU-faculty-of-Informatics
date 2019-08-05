import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
database_dir = os.path.join(basedir, 'db')

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_dir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    # pagination
    NOTEPADS_PER_PAGE = 3

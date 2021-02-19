
DEGUG = True

import os
import pymysql
import creds
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(creds.dbuser, creds.dbpasswd, creds.dbhost, creds.dbname)

# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = conn

DATABASE_CONNECT_OPTIONS = {}

SESSION_TYPE = 'sqlalchemy'
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2

# CSRF_ENABLED = True

# CSRF_SESSION_KEY = "SECRETFORCSRF"

SECRET_KEY = "SECRETKEYFORAPP"


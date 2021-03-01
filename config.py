
DEGUG = True

import os
import pymysql
import creds
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(creds.dbuser, creds.dbpasswd, creds.dbhost, creds.dbname)
SQLALCHEMY_DATABASE_URI = conn

# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')

DATABASE_CONNECT_OPTIONS = {}
# CKEDITOR_PKG_TYPE = 'full'

SESSION_TYPE = 'sqlalchemy'
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2

# CSRF_ENABLED = True

# CSRF_SESSION_KEY = "SECRETFORCSRF"

SECRET_KEY = "SECRETKEYFORAPP"

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = creds.email_username
MAIL_PASSWORD = creds.email_passwd

SEND_FILE_MAX_AGE_DEFAULT = 0
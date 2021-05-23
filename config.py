
DEGUG = True

import os
import pymysql
import creds
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(creds.dbuser, creds.dbpasswd, creds.dbhost, creds.dbname)
# SQLALCHEMY_DATABASE_URI = conn

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')
# SQLALCHEMY_DATABASE_URI = "sqlite:///"

# DATABASE_CONNECT_OPTIONS = {}
# CKEDITOR_PKG_TYPE = 'full'

SESSION_TYPE = 'sqlalchemy'
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = creds.csrf_key

SECRET_KEY = creds.secret_key

MAIL_SERVER = creds.mail_server
MAIL_PORT = creds.mail_port
MAIL_USE_TLS = True
MAIL_USERNAME = creds.email_username
MAIL_PASSWORD = creds.email_passwd

SEND_FILE_MAX_AGE_DEFAULT = 0

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'image_uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


S3_BUCKET                 = "tzimageupload"
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

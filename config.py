
DEGUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

SESSION_TYPE = 'sqlalchemy'


THREADS_PER_PAGE = 2

# CSRF_ENABLED = True

# CSRF_SESSION_KEY = "SECRETFORCSRF"

SECRET_KEY = "SECRETKEYFORAPP"


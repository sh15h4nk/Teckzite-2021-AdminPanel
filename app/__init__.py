from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_session import Session



app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
Session(app)

from app.admin.controllers import admin as admin_module
app.register_blueprint(admin_module)
Bootstrap(app)

db.create_all()
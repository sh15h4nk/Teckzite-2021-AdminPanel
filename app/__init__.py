from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app.admin.controllers import admin as admin_module
app.register_blueprint(admin_module)
Bootstrap(app)

db.create_all()
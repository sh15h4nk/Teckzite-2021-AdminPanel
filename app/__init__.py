from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_session import Session
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_mail import Mail

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

app.config['SESSION_SQLALCHEMY'] = db
Session(app)

ckeditor = CKEditor(app)
mail = Mail(app)


from app.admin.controllers import admin as admin_module
app.register_blueprint(admin_module)

from app.coordinate.controllers import coordinate as coordinate_module
app.register_blueprint(coordinate_module)

from app.organiser.controllers import organiser as organiser_module
app.register_blueprint(organiser_module)

Bootstrap(app)
# db.create_all()
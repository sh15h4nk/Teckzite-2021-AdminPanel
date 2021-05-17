from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_session import Session
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_mail import Mail
import boto3, botocore

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

app.config['SESSION_SQLALCHEMY'] = db
Session(app)

ckeditor = CKEditor(app)
mail = Mail(app)


mail = Mail(app)
bcrypt = Bcrypt(app)

s3 = boto3.resource("s3")

from app.admin.controllers import admin as admin_module
app.register_blueprint(admin_module)

from app.event_manager.controllers import event_manager as event_manager_module
app.register_blueprint(event_manager_module)

from app.event_coordinator.controllers import event_coordinator as event_coordinator_module
app.register_blueprint(event_coordinator_module)

from app.event_organiser.controllers import event_organiser as event_organiser_module
app.register_blueprint(event_organiser_module)

from app.workshop_manager.controllers import workshop_manager as workshop_manager_module
app.register_blueprint(workshop_manager_module)

from app.workshop_coordinator.controllers import workshop_coordinator as workshop_coordinator_module
app.register_blueprint(workshop_coordinator_module)

Bootstrap(app)



if __name__ == '__main__':
	app.run('0.0.0.0', port = 1337)
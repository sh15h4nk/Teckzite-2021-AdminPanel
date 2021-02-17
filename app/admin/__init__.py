from flask import Blueprint

from app.models import User
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


roles = {1:"Super Admin", 2:"Coordinater", 3:"Organiser"}

# us = User.query.filter_by(id="admin").first()

# if not us:
#     us = User("admin", "admin", 1)
#     db.session.add(us)
#     db.session.commit()
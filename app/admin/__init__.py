from flask import Blueprint

from app.models import User
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


roles = {1:"Super Admin", 2:"Coordinater", 3:"Organiser"}


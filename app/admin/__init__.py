from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')


roles = {1:"Super Admin", 2:"Coordinater", 3:"Organiser"}
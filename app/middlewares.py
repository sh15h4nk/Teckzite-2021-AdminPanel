from app.models import CurrentId
from functools import wraps
from flask import Response, request, redirect
from flask.helpers import flash, url_for
from flask_login import current_user
from app import db

#common middleware to use for all the requied roles
def role_required(roles):
    def inner_function(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user.role in roles:
                return func(*args, **kwargs)
            flash("Unauthorized")
            return Response(status=403)
        return decorated_function
    return inner_function

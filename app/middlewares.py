from app.models import CurrentId
from functools import wraps
from flask import Response, request, redirect
from flask.helpers import flash, url_for
from flask_login import current_user
from app import db



def admin_authenticated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        role = current_user.role
        if role == 1:
            return func(*args, **kwargs)
        
        flash("Unauthorised access")
        return redirect(url_for('index'))
    
    return decorated_function


def coordinate_authenticated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        role = current_user.role
        if role == 2:
            return func(*args, **kwargs)
        
        flash("Unauthorised access")
        return redirect(url_for('index'))
    
    return decorated_function

def organiser_authenticated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        role = current_user.role
        if role == 3:
            return func(*args, **kwargs)
        
        flash("Unauthorised access")
        return redirect(url_for('index'))
    
    return decorated_function


#common middleware to use for all the requied roles
def role_required(roles):
    def inner_function(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user.role in roles:
                return func(*args, **kwargs)
            flash("Unauthorized")
            return redirect(url_for("index"))
        return decorated_function
    return inner_function

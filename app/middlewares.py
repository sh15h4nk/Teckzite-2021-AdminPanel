from functools import wraps
from flask import Response, request, redirect
from flask.helpers import flash, url_for
from flask_login import current_user

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

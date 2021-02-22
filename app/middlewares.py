from app.models import CurrentId
from functools import wraps
from flask import Response, request, redirect
from flask.helpers import flash, url_for
from flask_login import current_user
from app.models import CurrentId
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


def generate_techzite_id():

    currentId = CurrentId.query.first()
    current_techzite_id = currentId.current_techzite_id
    
    currentId.current_techzite_id += 1
    db.session.commit()
    
    return current_techzite_id

def generate_event_id():

    currentId = CurrentId.query.first()
    current_event_id = currentId.current_event_id
    
    currentId.current_event_id += 1
    db.session.commit()

    return current_event_id

def generate_workshop_id():

    currentId = CurrentId.query.first()
    current_workshop_id = currentId.current_workshop_id
    
    currentId.current_workshop_id += 1
    db.session.commit()

    return current_workshop_id
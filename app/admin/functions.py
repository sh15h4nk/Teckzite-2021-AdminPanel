from flask_migrate import branches
from app import db

from app.models import User, Event, Workshop
from app.functions import *

#fetching 
def getAdminsAll():
    rows = User.query.filter_by(role=1).all()
    return rows

def getCoordinatorsAll():
    rows = User.query.filter_by(role=2).all()
    return rows
    
def getOrganisersAll():
    rows = User.query.filter_by(role=3).all()
    return rows

def getEventsAll():
    rows = Event.query.all()
    return rows

def getWorkshopsAll():
    rows = Workshop.query.filter_by().all()
    return rows


    
from app import db
from app.models import User, Event, Workshop
from app.functions import *

#fetching 
def getAdminsAll():
    rows = User.query.filter_by(role="admin").all()
    return rows

def getEventManagersAll():
    rows = User.query.filter_by(role="event_manager").all()
    return rows

def getEventCoordinatorsAll():
    rows = User.query.filter_by(role="event_coordinator").all()
    return rows

def getEventOrganisersAll():
    rows = db.session.query(User, Event).filter(User.id == Event.organiser_id).all()
    return rows

def getWorkshopManagersAll():
    rows = User.query.filter_by(role="workshop_manager").all()
    return rows

def getWorkshopCoordinatorsAll():
    rows = db.session.query(User, Workshop).filter(User.id == Workshop.coordinator_id).all()
    return rows

def getEventsAll():
    rows = Event.query.all()
    return rows

def getWorkshopsAll():
    rows = Workshop.query.filter_by().all()
    return rows


    
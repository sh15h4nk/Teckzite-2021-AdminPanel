from app.functions import *
from app import db

def getEventOrganisersAll(dept):
    rows = db.session.query(User, Event).filter(User.dept==dept, User.id == Event.organiser_id).all()
    return rows

def getEventsAll(dept):
    rows = Event.query.filter_by(dept=dept)
    return rows
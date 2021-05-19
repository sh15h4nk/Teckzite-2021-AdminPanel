from app.models import *

def getEventCoordinatorsAll():
    rows = User.query.filter_by(role="event_coordinator").all()
    return rows

def getEventOrganisersAll():
    rows = User.query.filter_by(role="event_organiser").all()
    return rows

def getEventsAll():
    rows = Event.query.all()
    return rows
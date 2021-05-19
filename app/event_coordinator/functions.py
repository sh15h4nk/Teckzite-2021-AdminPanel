from app.functions import *

def getEventOrganisersAll(dept):
    rows = User.query.filter_by(role="event_organiser", dept=dept).all()
    return rows

def getEventsAll(dept):
    rows = Event.query.filter_by(dept=dept)
    return rows
from app.models import User, Event, db
from app.functions import *


def getEventCoordinatorsAll():
    rows = User.query.filter_by(role="event_coordinator").all()
    return rows

def getEventOrganisersAll():
    rows = db.session.query(User, Event).filter(User.id == Event.organiser_id).all()
    return rows

def getEventsAll():
    rows = Event.query.all()
    return rows
from app.models import Event
from app.functions import *

def getEventsAll(event_organiser_id):
    rows = Event.query.filter_by(organiser_id=event_organiser_id)
    return rows
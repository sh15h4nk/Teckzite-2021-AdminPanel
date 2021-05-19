
from app.models import Workshop

def getWorkshopsAll(workshop_coordinator_id):
    rows = Workshop.query.filter_by(coordinator_id = workshop_coordinator_id)
    return rows

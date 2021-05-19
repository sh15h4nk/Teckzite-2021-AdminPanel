from app.models import *


def getWorkshopManagersAll():
    rows = User.query.filter_by(role="workshop_manager").all()
    return rows

def getWorkshopCoordinatorsAll():
    rows = User.query.filter_by(role="workshop_coordinator").all()
    return rows

def getWorkshopsAll():
    rows = Workshop.query.filter_by().all()
    return rows

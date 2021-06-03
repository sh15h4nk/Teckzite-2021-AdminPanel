from app import db
from app.models import *
from app.functions import *
from sqlalchemy import func

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

def getCAAll():
    rows = CA.query.filter_by().all()
    # data = [i for i in rows]
    # for i in data:
    #     print(i)
    # print(type(rows))
    # rows = db.session.query(CA, TechUser).filter(TechUser.referral == CA.caId).all()
    # rows = db.session.query(CA, TechUser).join(TechUser,TechUser.referral == CA.caId).all()
    # for i in rows:
        # print(i)
    # users = 
    # rows = db.session.query(CA, func.count(TechUser.referral)).filter(TechUser.referral == CA.caId).all()
    # print(rows)
    # for row in rows:
    #     row.total = TechUser.query.filter_by(referral = row.caId).count()
    #     row.paid = TechUser.query.filter_by(referral = row.caId, payment_status = 1).count()
    return rows

def getTzUsers():
    rows = TechUser.query.filter_by(registration_status = 1).all()
    return rows
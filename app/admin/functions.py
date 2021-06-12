from app import db
from app.models import *
from app.functions import *
from sqlalchemy import func, case

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
    # rows = Workshop.query.filter_by().all()
    rows = db.session.query(Workshop, func.count(TechUser.id), func.count(case([((TechUser.workshop_payment_status == 1), TechUser.id)]))).join(TechUser, Workshop.workshopId == TechUser.workshop_id).group_by(Workshop.workshopId).all()
    return rows

def getCAAll():
    rows = db.session.query(CA, func.count(TechUser.id), func.count(case([((TechUser.payment_status == 1), TechUser.id)])), func.count(case([((TechUser.workshop_payment_status == 1), TechUser.id)]))).join(TechUser, or_(CA.caId == TechUser.referral, CA.caId == TechUser.workshop_referral)).group_by(CA.caId).all()
    return rows

def getTzUsers():
    rows = TechUser.query.filter_by(registration_status = 1).all()
    return rows

# def getWorkshopReg():
#     rows = TechUser.query.filter(workshop_id != None)
#     for i in rows:
#         print(i)
#     return rows
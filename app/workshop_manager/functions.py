from app.models import *
from app.functions import *

def getWorkshopManagersAll():
    rows = User.query.filter_by(role="workshop_manager").all()
    return rows

def getWorkshopCoordinatorsAll():
    rows = db.session.query(User, Workshop).filter(User.id == Workshop.coordinator_id).all()
    return rows

def getWorkshopsAll():
    # rows = Workshop.query.filter_by().all()
    rows = db.session.query(Workshop, func.count(TechUser.id), func.count(case([((TechUser.workshop_payment_status == 1), TechUser.id)]))).join(TechUser, Workshop.workshopId == TechUser.workshop_id).group_by(Workshop.workshopId).all()
    return rows
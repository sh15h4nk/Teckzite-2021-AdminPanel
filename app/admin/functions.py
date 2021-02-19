from flask_migrate import branches
from app import db

from app.models import User, Event

def getAdmins():
    rows = User.query.filter_by(role=1).all()

    rows = [(row.id, row.name, row.email, row.role) for row in rows]
    
    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}

def getCoordinaters():
    rows = User.query.filter_by(role=2).all()

    rows = [(row.id, row.name, row.email, row.role) for row in rows]
    
    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}

def getOrganisers(dept):
    rows = User.query.filter_by(role=3, dept=dept).all()

    rows = [(row.id, row.name, row.email, row.role) for row in rows]
    
    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}



def getEvents(dept):
    rows = Event.query.filter_by(dept=dept).all()
    rows = [(row.id, row.name, row.details) for row in rows]

    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}

def addEvent(eventId, eventName, teamSize ,html):
        
    event = Event(eventId, eventName, teamSize, html)

    db.session.add(event)
    db.session.commit()


def getWorkshops():
    rows = Event.query.filter_by().all()
    rows = [(row.name, row.details) for row in rows]

    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}



    


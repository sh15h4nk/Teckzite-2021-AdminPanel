from app import db

from app.admin.models import User, Event

def getAdmins(role):
    rows = User.query.filter_by(role=role).all()
    rows = [(row.id, row.name, row.email, row.role) for row in rows]
    
    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}

def getEvents():
    rows = Event.query.filter_by().all()
    rows = [(row.name, row.details, row.teamsize) for row in rows]

    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}

def getWorkshops():
    rows = Event.query.filter_by().all()
    rows = [(row.name, row.details) for row in rows]

    no_rows = len(rows)
    try:
        no_cols = len(rows[0])
    except:
        no_cols = 0

    return {"rows": rows, "no_rows": no_rows, "no_cols": no_cols}



    


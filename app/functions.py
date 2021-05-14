import re
from app import mail, db, app
from flask_mail import Message 
from flask.helpers import flash, url_for
from flask import escape, Markup
from app.models import User, Event, Workshop, CurrentId, Contact, FAQ, Sponsor
import json

def dict_escape(d:dict):
    for k,v in d.items():
        d[k] = str(escape(v))
    return d

def dict_markup(d:dict):
    for k,v in d.items():
        d[k] = Markup(v)
    return d

def sendMail(user):
	token = user.generate_token()
	msg = Message("Password Reset Link", sender='tz2021mailserver@gmail.com', recipients=[user.email])
	msg.body = f"To reset your password, Kindly visit the following link \n{url_for('resetPassword',token= token,_external=True)}\n If you didn't make this request then simply ignore it"
	mail.send(msg)

def generate_techzite_id():

    currentId = CurrentId.query.first()
    current_techzite_id = currentId.current_techzite_id
    
    currentId.current_techzite_id += 1
    db.session.commit()
    
    return current_techzite_id

def generate_event_id():

    currentId = CurrentId.query.first()
    current_event_id = currentId.current_event_id
    
    currentId.current_event_id += 1
    db.session.commit()

    return current_event_id

def generate_workshop_id():

    currentId = CurrentId.query.first()
    current_workshop_id = currentId.current_workshop_id
    
    currentId.current_workshop_id += 1
    db.session.commit()

    return current_workshop_id




#Creating
def addUser(userId, name, email, password, role, dept, phone):
    user = User(userId, name, email, password, role, dept, phone)
    db.session.add(user)
    db.session.commit()

    # sendMail(user)

    return user

def addEvent(title, dept, coordinater_id, organiser_id):
    eventId = generate_event_id()
        
    event = Event(eventId, title, dept, coordinater_id, organiser_id)
    db.session.add(event)
    db.session.commit()

    return event


def updateEvent(data):
  
    # data = dict_escape(data)
    del data['csrf_token']
    del data['submit']
    event = Event.query.filter_by(id = data['eventId']).update(data)
    db.session.commit()
    return event

def updateWorkshop(data):
  
    del data['csrf_token']
    del data['submit']
    workshop = Workshop.query.filter_by(id = data['workshopId']).update(data)
    db.session.commit()
    return workshop



def addWorkshop(title, dept, description, fee, status, about, timeline, resources, coordinator_id):
    workshop_id = generate_workshop_id()

    #sanitizing input
    description = str(escape(description))
    status = str(escape(status))
    about = str(escape(about))
    timeline = str(escape(timeline))
    resources = str(escape(resources))
    #adding workshop to db
    workshop = Workshop(workshop_id, title, dept, description, fee, status, about, timeline, resources, coordinator_id)
    db.session.add(workshop)
    db.session.commit()
    
    return workshop

def addContactToWorkshop(name, email, phone, workshop_id):

    workshop = Workshop.query.filter_by(id = workshop_id).first()
    if not workshop:
        return "Invalid Workshop ID"
    elif not (len(workshop.contacts) < 3):
        return "Overflow"

    contact = Contact.query.filter_by(email = email, phone = phone).first()
    if contact:
        if not contact.workshop_id:
            contact.workshop_id = workshop_id
            db.session.commit()
            return contact


    contact = Contact(name, email, phone)
    contact.workshop_id = workshop_id
    db.session.add(contact)
    db.session.commit()

    return contact
     
def addFaqToWorkshop(question, answer, workshop_id):

    workshop = Workshop.query.filter_by(id = workshop_id).first()
    if not workshop:
        return "Invalid Workshop ID"
    elif not (len(workshop.faqs) < 10):
        return "Overflow"


    faq = FAQ.query.filter_by(question = question, answer = answer, workshop_id = workshop_id).first()
    if faq:
        return "FAQ Already exists"

    
    faq = FAQ(question, answer)
    faq.workshop_id = workshop_id
    db.session.add(faq)
    db.session.commit()

    return faq

def addSponsorToWorkshop(title, url, workshop_id):
    workshop = Workshop.query.filter_by(id = workshop_id).first()
    if not workshop:
        return "Invalid Workshop ID"
    elif not (len(workshop.sponsors) < 3):
        return "Overflow"

    sponsor = Sponsor.query.filter_by(title = title, url = url, workshop_id = workshop_id).first()
    if sponsor:
        return "Sponsor Already exists"

    sponsor = Sponsor(title, url)
    sponsor.workshop_id = workshop_id
    db.session.add(sponsor)
    db.session.commit()
    return sponsor

def updateWorkshop(key, value, workshop_id):
    workshop = Workshop.query.filter_by(id = workshop_id).first()
    if not workshop:
        return "Invalid Workshop ID"
    # props = vars(workshop)
    print(hasattr(workshop, "name"))
    # for i in props:
    #     print(i)
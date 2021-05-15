from app.forms import Contacts
import re
from app import mail, db, app
from flask_mail import Message 
from flask.helpers import flash, url_for
from flask import escape, Markup
from app.models import User, Event, Workshop, CurrentId, Contact, FAQ, Sponsor
import json
from config import *

from PIL import Image
from io import BytesIO
import base64, cv2

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crop_and_save_image(imageString, crop, image_type, id):

    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.exists(f"{UPLOAD_FOLDER}/{image_type}/"):
        os.mkdir(f"{UPLOAD_FOLDER}/{image_type}/")
    
    image = Image.open(BytesIO(base64.b64decode(imageString.encode())))
    url = f"{UPLOAD_FOLDER}/{image_type}/{id}.{image.format.lower()}"
    image.save(url)

    image = cv2.imread(url)

    if crop['x'] < 0:
        crop['x'] = 0
    if crop['y'] < 0:
        crop['y'] = 0
    
    crop_image = image[ crop['y']:crop['y']+crop['height'], crop['x']:crop['x']+crop['width']]
    cv2.imwrite(url, crop_image)
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

def updateWorkshop(data, field_id, field):

    if not Workshop.query.filter_by(id = field_id):
        return "error"

    if field == "markup":
        del data['csrf_token']
        status =  Workshop.query.filter_by(id = field_id).update(data)
        return status
    
    elif field == "contact":
        del data['csrf_token']
        status =  Contact.query.filter_by(id = field_id).update(data)
        return status
    
    elif field == "sponsor":
        del data['csrf_token']
        status =  Sponsor.query.filter_by(id = field_id).update(data)
        return status

    elif field == "faq":
        del data['csrf_token']
        status =  FAQ.query.filter_by(id = field_id).update(data)
        return status

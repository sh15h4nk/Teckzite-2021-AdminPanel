from operator import contains
from os import stat, stat_result

from botocore.retries import bucket
import flask_sqlalchemy
from app.forms import Contacts
import re
from app import mail, db, app
from flask_mail import Message 
from flask.helpers import flash, url_for
from flask import escape, Markup
from app.models import User, Event, Workshop, CurrentId, Contact, FAQ, Sponsor
import json
from config import *
from app.models import Image

from PIL import Image as PIL_Image
from io import BytesIO
import base64, cv2, uuid, numpy as np
from app import s3, bcrypt
import asyncio, time

from sqlalchemy import and_, or_

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

    return "EV"+str(current_event_id)

def generate_workshop_id():

    currentId = CurrentId.query.first()
    current_workshop_id = currentId.current_workshop_id
    
    currentId.current_workshop_id += 1
    db.session.commit()

    return "WS"+str(current_workshop_id)



def upload_file_to_s3(file, filename, file_ext, acl="public-read"):

    bucket = s3.Bucket(S3_BUCKET)
    obj = bucket.Object(f"{filename}.{file_ext}")
    obj.upload_fileobj(
        file,
        ExtraArgs={
            "ACL": acl,
            "ContentType": f"image/{file_ext}"
        }
    )
    return "{}{}.{}".format(S3_LOCATION, filename, file_ext)

def crop_image(imageString, crop):
    
    # saving temp image
    image = PIL_Image.open(BytesIO(base64.b64decode(imageString.encode())))
    filename = uuid.uuid4()
    file_ext = image.format.lower()

    temp_path = f"{UPLOAD_FOLDER}/{filename}.{file_ext}"
    image.save(temp_path)

    # cropping image
    image = cv2.imread(temp_path)
    if crop['x'] < 0:
        crop['x'] = 0
    if crop['y'] < 0:
        crop['y'] = 0
    
    crop_image = image[ crop['y']:crop['y']+crop['height'], crop['x']:crop['x']+crop['width']]
    cv2.imwrite(temp_path, crop_image)
    

    with open(temp_path, "rb") as file:
        url = upload_file_to_s3(file, filename, file_ext)
        os.remove(temp_path)
        return url


#Creating
def addUser(userId, name, email, password, role, dept, phone):
    password = bcrypt.generate_password_hash(password)
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
    if not Event.query.filter_by(id = data['id']):
        return "Invalid Event ID"
    del data['csrf_token']
    del data['submit']
    
    data = dict_escape(data)
    try:
        event = Event.query.filter_by(id = data['id']).update(data)
    except:
        return "Error While updating"
    
    db.session.commit()
    return event

def addWorkshop(title, dept, coordinator_id, organiser_id):
    workshop_id = generate_workshop_id()

    #adding workshop to db
    workshop = Workshop(workshop_id, title, dept, coordinator_id, organiser_id)
    db.session.add(workshop)
    db.session.commit()
    
    return workshop

def updateWorkshop(data, workshop_id):
    if not Workshop.query.filter_by(id = workshop_id):
        return "Invalid Workshop ID"
    # return str(data)
    del data['csrf_token']
    del data['photo']
    
    data = dict_escape(data)
    try:
        workshop = Workshop.query.filter_by(id = workshop_id).update(data)
    except:
        return "Error While updating"
    
    db.session.commit()
    return Workshop.query.filter_by(id = workshop_id).first()

def addContact(name, email, phone, program_id):
    if program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    elif program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
    
    if not program:
        return "Invalid program ID"

    contacts = Contact.query.filter(and_(Contact.hidden == 0, or_(Contact.workshop_id == program.id, Contact.event_id == program.id))).count()
    if not contacts < 3 :
        return "Overflow"

    contact = Contact.query.filter_by(email = email, phone = phone).first()
    if contact:
        if program_id.startswith("WS") and not contact.workshop_id:
            contact.workshop_id = program.id
            db.session.commit()
            return contact
        elif program_id.startswith("EV") and not contact.event_id:
            contact.event_id = program.id
            db.session.commit()
            return contact
        else:
            return "Contact Already exists!"



    contact = Contact(name, email, phone)
    if program_id.startswith("WS"):
        contact.workshop_id = program.id
    else:
        contact.event_id = program.id
    db.session.add(contact)
    db.session.commit()

    return contact

     
def addFaq(question, answer, program_id):

    if program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    elif program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
    
    if not program:
        return "Invalid program ID"

    faqs = FAQ.query.filter(and_(FAQ.hidden == 0, or_(FAQ.workshop_id == program.id, FAQ.event_id == program.id))).count()
    if not faqs < 10 :
        return "Overflow"

    faq = FAQ.query.filter(and_(FAQ.question == question, FAQ.answer == answer, or_(FAQ.workshop_id == program.id, FAQ.event_id == program.id))).first()
    if faq:
        return "FAQ Already exists!"

    
    faq = FAQ(question, answer)
    if program_id.startswith("WS"):
        faq.workshop_id = program.id
    else:
        faq.event_id = program.id
    db.session.add(faq)
    db.session.commit()

    return faq

def addSponsor(name, url, program_id, image_url):
    if program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    elif program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
    
    if not program:
        return "Invalid program ID"


    sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, or_(Sponsor.workshop_id == program.id, Sponsor.event_id == program.id))).count()
    if not sponsors < 3 :
        return "Overflow"

    sponsor = Sponsor.query.filter(and_(Sponsor.name == name, Sponsor.url == url, or_(Sponsor.workshop_id == program.id, Sponsor.event_id == program.id))).first()
    if sponsor:
        return "Sponsor Already exists"

    sponsor = Sponsor(name, url, image_url)
    
    if program_id.startswith("WS"):
        sponsor.workshop_id = program.id
    else:
        sponsor.event_id = program.id

    db.session.add(sponsor)
    db.session.commit()
    return sponsor



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crop_and_save_image(imageString, crop, image_type, id):

    try:

        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        if not os.path.exists(f"{UPLOAD_FOLDER}/{image_type}/"):
            os.mkdir(f"{UPLOAD_FOLDER}/{image_type}/")
        
        image = PIL_Image.open(BytesIO(base64.b64decode(imageString.encode())))
        url = f"{UPLOAD_FOLDER}/{image_type}/{uuid.uuid4()}.{image.format.lower()}"
        image.save(url)

        # saving to database
        image = Image(url)
        if image_type == 'workshop':
            image.workshop_id = id
        elif image_type == 'event':
            image.event_id = id
        elif image_type == 'sponsor':
            return url

        db.session.add(image)
        db.session.commit()

        image = cv2.imread(url)

        if crop['x'] < 0:
            crop['x'] = 0
        if crop['y'] < 0:
            crop['y'] = 0
        
        crop_image = image[ crop['y']:crop['y']+crop['height'], crop['x']:crop['x']+crop['width']]
        cv2.imwrite(url, crop_image)
        return 1
    except:
        return 0

def updateContact(data, contact_id, program_id):
    del data['csrf_token']
    if program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    elif program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
    
    if not program:
        return "Invalid program ID"

    contact = Contact.query.filter(and_(Contact.id == contact_id, or_(Contact.workshop_id == program.id, Contact.event_id == program.id))).first()
    if not contact:
        return "Not a contact of the Program"


    contact = Contact.query.filter(and_(Contact.email == data['email'], Contact.phone == data['phone'], or_(Contact.workshop_id == program.id, Contact.event_id == program.id))).first()
    if contact:
        return "Contact Already Exists!"

    try:
        contact = Contact.query.filter_by(id = contact_id).update(data)
    except:
        return "Error While updating"
    db.session.commit()
    return contact

def updateFaq(data, faq_id, program_id):
    del data['csrf_token']
    if program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    elif program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
    
    if not program:
        return "Invalid program ID"

    faq = FAQ.query.filter(and_(FAQ.id == faq_id, or_(FAQ.workshop_id == program.id, FAQ.event_id == program.id))).first()
    if not faq:
        return "Not a faq of the Program"

    faq = FAQ.query.filter(and_(FAQ.question == data['question'], FAQ.answer == data['answer'], or_(FAQ.workshop_id == program.id, FAQ.event_id == program.id))).first()
    if faq:
        return "FAQ already exists!"

    try:
        faq = FAQ.query.filter_by(id = faq_id).update(data)
    except:
        return  "Error while updating"
    db.session.commit()
    return faq

def updateSponsor(data, sponsor_id, program_id, image_url=""):
    del data['csrf_token']
    del data['photo']
    if program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    elif program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
    
    if not program:
        return "Invalid program ID"

    sponsor = Sponsor.query.filter(and_(Sponsor.id == sponsor_id, or_(Sponsor.workshop_id == program.id, Sponsor.event_id == program.id))).first()
    if not sponsor:
        return "Not a sponsor of the Program"

    sponsor = Sponsor.query.filter(and_(Sponsor.name == data['name'], Sponsor.url == data['url'], or_(Sponsor.workshop_id == program.id, Sponsor.event_id == program.id))).first()
    if sponsor:
        return "Sponsor already exists!"
    if image_url:
        data['image_url'] = image_url
    try:
        sponsor = Sponsor.query.filter_by(id = sponsor_id).update(data)
    except:
        return  "Error while updating"
    db.session.commit()
    return Sponsor


# def updateWorkshop(data, workshop_id, image_url=""):

#     if not Workshop.query.filter_by(id = workshop_id):
#         return "Invalid Workshop ID"
#     del data['photo']
#     del data['csrf_token']

#     workshop = Workshop.query.filter_by(id = workshop_id).first()
#     # markup = dict_markup({
#     #     "status": workshop.status,
#     #     "description": workshop.description,
#     #     "about": workshop.about,
#     #     "timeline": workshop.timeline,
#     #     "resources": workshop.resources,
#     # })


#     data = dict_escape(data)
#     try:
        
#         if image_url:
#             data['image_url'] = image_url     
        
#         status =  Workshop.query.filter_by(id = field_id).update(data)
#         db.session.commit()

#     except:
#         return (workshop, markup,"Error while updating!")

#     workshop = Workshop.query.filter_by(id = field_id).first()
#     markup = dict_markup({
#         "status": workshop.status,
#         "description": workshop.description,
#         "about": workshop.about,
#         "timeline": workshop.timeline,
#         "resources": workshop.resources,
#     })

#     return (workshop, markup, "Workshop details updated successfully")

    
    # elif field == "contact":
    #     del data['csrf_token']
    #     contact = Contact.query.filter_by(email = data['email'], phone = data['phone']).first()
    #     workshop = Workshop.query.filter_by(id = workshop_id).first()
    #     if not contact:    
    #         try:
    #             contact = Contact.query.filter_by(id = field_id).update(data)
    #         except:
    #             return (workshop.contacts, "Error while updating!")

    #         workshop = Workshop.query.filter_by(id = workshop_id).first()
    #         return (workshop.contacts, "Contact updated successfully")
    #     else:            
    #         return (workshop.contacts, "Contact already exists")
                  
    
    # elif field == "sponsor":
    #     del data['csrf_token']
    #     del data['photo']
    #     sponsor = Sponsor.query.filter_by(name = data['name'], url = data['url']).first()
    #     workshop = Workshop.query.filter_by(id = workshop_id).first()
    #     if not sponsor:    
    #         try:
    #             if image_url:
    #                 data['image_url'] = image_url 
    #             sponsor = Sponsor.query.filter_by(id = field_id).update(data)
    #         except:
    #             return (workshop.contacts, "Error while updating!")

    #         workshop = Workshop.query.filter_by(id = workshop_id).first()
    #         return (workshop.sponsors, "Sponsor updated successfully")
    #     else:
    #         return (workshop.sponsors, "Sponsor already exists")

    # elif field == "faq":
    #     del data['csrf_token']
    #     faq = FAQ.query.filter_by(question = data['question'], answer = data['answer']).first()
    #     workshop = Workshop.query.filter_by(id = workshop_id).first()
    #     if not faq:    
    #         try:
    #             faq = FAQ.query.filter_by(id = field_id).update(data)
    #         except:
    #             return (workshop.contacts, "Error while updating!")

    #         workshop = Workshop.query.filter_by(id = workshop_id).first()
    #         return (workshop.faqs, "Faq updated successfully")
    #     else:
    #         return (workshop.faqs, "Faq already exists")

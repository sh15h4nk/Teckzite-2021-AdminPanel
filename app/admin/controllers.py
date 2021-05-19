from functools import singledispatch
from operator import add
from typing import Any
from flask import url_for, redirect, request, render_template, Blueprint, session, flash, escape, get_flashed_messages, Markup, jsonify, Response
import flask
from flask.ctx import after_this_request
from flask.globals import current_app
import flask_session
from werkzeug.utils import secure_filename
from app.models import User
from app.forms import CreateWorkshopForm, LoginForm, CreateEventForm, PhotoForm, RegisterForm, Contacts, FAQs, Sponsors, UpdateEventForm, UpdateWorkshopForm
from app import db, app, bcrypt
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import roles
import cv2
import os, asyncio

import urllib

from app.admin import admin
from app.admin.functions import *
from app.functions import *
from app.controllers import login_manager
from app.mynav import mynav

from app.middlewares import role_required
from app import ckeditor
from sqlalchemy import and_, or_



#default routes
@admin.route('/')
def home():
    return render_template('admin/index.html')

#login routes
@admin.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@admin.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session and session['role'] == "admin":
        flash("Already Logged In As Admin")
        return redirect(url_for('admin.dashboard'))
        

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "admin" and user.hidden == 0:
                login_user(user)
                session['id'] = user.id
                session['role'] = user.role
                return redirect(url_for("admin.dashboard"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form, role = "Admin")
    
        
#Data fetching routes
@admin.route('/dashboard/')
@login_required
@role_required("admin")
def dashboard():
    get_flashed_messages()
    return render_template("admin/dashboard.html",current_user = current_user)


@admin.route('/admins/')
@login_required
@role_required("admin")
def getAdminsView():
    data = getAdminsAll()
    return render_template("users.html",role = "Admin",data = data)


@admin.route('/event.manager/')
@login_required
@role_required("admin")
def getEventManagersView():
    data = getEventManagersAll()
    return render_template("users.html", role= "Event Manager",data = data)


@admin.route('/event.coordinators/')
@login_required
@role_required("admin")
def getEventCoordinatorsView():
    data = getEventCoordinatorsAll()
    return render_template("users.html", role= "Event Coordinator",data = data)

@admin.route('/event.organiser/')
@login_required
@role_required("admin")
def getEventOrganisersView():
    data = getEventOrganisersAll()
    return render_template("users.html", role= "Event Organiser",data = data)

@admin.route('/workshop.manager/')
@login_required
@role_required("admin")
def getWorkshopManagersView():
    data = getWorkshopManagersAll()
    return render_template("users.html", role= "Workshop Manager",data = data)

@admin.route('/workshop.coordinator/')
@login_required
@role_required("admin")
def getWorkshopCoordinatorsView():
    data = getWorkshopCoordinatorsAll()
    return render_template("users.html", role= "Workshop Coordinator",data = data)

@admin.route('/events/')
@login_required
@role_required("admin")
def getEventsView():
    data = getEventsAll()
    return render_template("events.html",data = data)


@admin.route('/workshops/')
@login_required
@role_required("admin")
def getWorkshopsView():
    data = getWorkshopsAll()
    return render_template("workshops.html",data =data)




#Data Adding routes
@admin.route('/admins/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addAdminView():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, "admin", form.dept.data, form.phone.data)

        flash("You Registered a Admin Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addAdminView'))   

    return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)


@admin.route('/event.manager/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addEventManagerView():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, "event_manager", form.dept.data, form.phone.data)

        flash("You Registered a Event Manager Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addEventManagerView'))   

    return render_template('admin/register.html',role="Event Manager", form = form,current_user = current_user)

@admin.route('/workshop.manager/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addWorkshopManagerView():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, "workshop_manager", form.dept.data, form.phone.data)

        flash("You Registered a Workshop Manager Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addWorkshopManagerView'))   

    return render_template('admin/register.html',role="Workshop Manager", form = form,current_user = current_user)



@admin.route('/event.coordinator/add', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def addEventCoordinator():
    form = RegisterForm(request.form)
    if form.validate_on_submit():

        user = User.query.filter_by(hidden = 0, role = "event_coordinator", dept = form.dept.data).count()
        if user:
            flash("Event Coordinator already exists for this Department")
            return render_template('admin/register.html',role="Events Coordinator", form = form,current_user = current_user)
        
        addUser(form.userId.data, form.name.data, form.email.data, "event_coordinator", form.dept.data, form.phone.data)

        flash("You Registered Event Coordinator Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addEventCoordinator'))   

    return render_template('admin/register.html',role="Events Coordinator", form = form,current_user = current_user)







# @admin.route('/coordinators/add', methods=['GET', 'POST'])
# @login_required
# @role_required("admin")
# def addCoordinator():
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
        

#         addUser(form.userId.data, form.name.data, form.email.data, 2, form.dept.data, form.phone.data)

#         flash("You Registered a Coordinator Succesfully")
#         flash("Email has been sent to reset the password")

#         return redirect(url_for('admin.addCoordinator')) 

#     return render_template('admin/register.html',role="Coordinator", form = form,current_user = current_user)


@admin.route('/event/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addEventView():
    form = CreateEventForm(request.form)
    if form.validate_on_submit():
        event_organiser = form.event_organiser.data
        event_coordinator = User.query.filter_by(dept=event_organiser['dept'], role="event_coordinator").first()
        if event_coordinator is None:
            flash("No coordinator for the Dept")
            return redirect(url_for('admin.addEventView'))
        
        organiser = addUser(event_organiser['userId'], event_organiser['name'], event_organiser['email'], "event_organiser", event_organiser['dept'], event_organiser['phone'])
        addEvent(form.title.data, event_coordinator.dept , event_coordinator.id, organiser.id)

        flash("Event added successfully")
        flash("Organiser added successfully")
        # flash("Check Email to reset password")
        return redirect(url_for('admin.addEventView'))

    return render_template('add_event.html', form=form)

# @admin.route('/event/update', methods= ['GET', 'POST'])
# @login_required
# @role_required("admin")
# def updateEventView():
#     form = UpdateEventForm(request.form)
#     if request.method == 'POST':

#         event_id = request.form['event_id']
#         event = Event.query.filter_by(eventId = event_id).first()
#         print("fucking eve#####", event.eventId)
#         if not event:
#             return "Invalid Event"

#         if not event.image_url:
#             event.image_url = "http://tzimageupload.s3.amazonaws.com/back.jpg"

#         markup = dict_markup({
#             "status": event.status,
#             "description": event.description,
#             "brief": event.brief,
#             "timeline": event.timeline,
#             "structure": event.structure,
#             "rules": event.rules,
#             })

#         if request.form.get('update-button'):                        
#             return render_template('update_event.html', form = form, event = event, markup = markup)

#         if form.validate_on_submit():
#             # return request.form
#             event_id = dict(request.form).get('update-event')

#             #update image            
#             crop = {}
#             base64image = form.photo.image.data

#             image_url = ""
#             if base64image:    
#                 crop['x'] = int(float(str(form.photo.cropX.data)))
#                 crop['y'] = int(float(str(form.photo.cropY.data)))
#                 crop['width'] = int(float(str(form.photo.cropWidth.data)))
#                 crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
#                 image_url = crop_image(form.photo.image.data, crop)     

#             markup = updateEvent(form.data, event_id, image_url)

#             flash(markup[2])
#             return render_template('update_event.html', form = form, event = markup[0], markup = markup[1])

#     return render_template('update_event.html', form = form, event = event, markup = markup)


@admin.route('/workshop/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addWorkshopView():
    form = CreateWorkshopForm(request.form)
    if form.validate_on_submit():
        # return request.form
        workshop_coordinator = form.workshop_coordinator.data
        coordinator_id = current_user.id

        workshop_coordinator = addUser(workshop_coordinator['userId'], workshop_coordinator['name'], workshop_coordinator['email'], "workshop_coordinator", workshop_coordinator['dept'], workshop_coordinator['phone'])
        addWorkshop(form.title.data, form.dept.data, coordinator_id)

        flash("Workshop Added Succesfully")
        flash("Organiser Added Succesfully")

        return redirect(url_for('admin.addWorkshopView'))

    return render_template('add_workshop.html', form = form)


# @admin.route('/workshop/update', methods=['GET', 'POST'])
# @login_required
# @role_required("admin")
# def updateWorkshopView():
#     form = UpdateWorkshopForm(request.form)
#     if request.method == 'POST':

#         workshop_id = request.form['workshop_id']
#         workshop = Workshop.query.filter_by(workshopId = workshop_id).first()
#         if not workshop:
#             return "Invalid Workshop"

#         if not workshop.image_url:
#             workshop.image_url = "http://tzimageupload.s3.amazonaws.com/back.jpg"

#         markup = dict_markup({
#             "status": workshop.status,
#             "description": workshop.description,
#             "about": workshop.about,
#             "timeline": workshop.timeline,
#             "resources": workshop.resources,
#             })

#         if request.form.get('update-button'):                        
#             return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup)

#         if form.validate_on_submit():
#             # return request.form
#             workshop_id = dict(request.form).get('update-workshop')

#             #update image            
#             crop = {}
#             base64image = form.photo.image.data

#             image_url = ""
#             if base64image:    
#                 crop['x'] = int(float(str(form.photo.cropX.data)))
#                 crop['y'] = int(float(str(form.photo.cropY.data)))
#                 crop['width'] = int(float(str(form.photo.cropWidth.data)))
#                 crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
#                 image_url = crop_image(form.photo.image.data, crop)     

#             markup = updateWorkshop(form.data, workshop_id, image_url)

#             flash(markup[2])
#             return render_template('update_workshop.html', form = form, workshop = markup[0], markup = markup[1])

#     return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup)


# @admin.route('/addData', methods=["POST"])
# @login_required
# @role_required("admin")
# def addDataView():
#     try:
#         program_id = request.form['programId']
#     except:
#         return Response(status = 400)

#     program_id = request.form['programId']

#     if program_id.startswith("EV"):
#         contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.event_id == program_id)).count()
#         faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.event_id == program_id)).count()
#         sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.event_id == program_id)).count()
#         # program = Event.query.filter_by(eventId= program_id).first()

#     elif program_id.startswith("WS"):
#         contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.workshop_id == program_id)).count()
#         faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.workshop_id == program_id)).count()
#         sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.workshop_id == program_id)).count()
#         # program = Workshop.query.filter_by(workshopId = program_id).first()
#     else:
#         return Response(status = 400)

#     if not program_id:
#         return Response(status = 400)

#     # contacts = Contact.query.filter(and_(Contact.hidden == 0, or_(Contact.workshop_id == program.workshopId, Contact.event_id == program.eventId))).count()
#     # faqs = FAQ.query.filter(and_(FAQ.hidden == 0, or_(FAQ.workshop_id == program.workshopId, FAQ.event_id == program.eventId))).count()
#     # sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, or_(Sponsor.workshop_id == program.workshopId, Sponsor.event_id == program.eventId))).count()
#     print("#########################", contacts)

#     #for FORMS
#     if request.form.get("add-faq-form"):
#         form = FAQs()
#         return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
    
#     elif request.form.get("add-contact-form"):
#         form = Contacts()
#         return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

#     elif request.form.get('add-sponsor-form'):
#         form = Sponsors()
#         return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)


#     #TO ADD the data
#     elif request.form.get("add-contact"):
#         form = Contacts()
#         if form.validate_on_submit():
#             contact = addContact(request.form['name'], request.form['email'], request.form['phone'], program_id)
#             if type(contact) == str:
#                 if contact == "Overflow":
#                     flash("Contacts Limit Exceeded!")
#                     return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
#                 flash(contact)
#                 return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
#             flash("Contact  Added!")
#         return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

#     elif request.form.get("add-faq"):
#         form = FAQs()
#         if form.validate_on_submit():
#             faq = addFaq(form.question.data, form.answer.data, program_id)
#             if type(faq) == str:
#                 if faq == "Overflow":
#                     flash("Faqs Limit Exceeded!")
#                     return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
#                 flash(faq)
#                 return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
#             flash("FAQ Added!")
#         return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

#     elif request.form.get("add-sponsor"):
#         form = Sponsors()
#         if form.validate_on_submit():
#             # return request.form

#             # adding image
#             #update image            
#             crop = {}
#             base64image = form.photo.image.data

#             image_url = ""
#             if base64image:    
#                 crop['x'] = int(float(str(form.photo.cropX.data)))
#                 crop['y'] = int(float(str(form.photo.cropY.data)))
#                 crop['width'] = int(float(str(form.photo.cropWidth.data)))
#                 crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
#                 image_url = crop_image(form.photo.image.data, crop)     
#             else: 
#                 flash("Please upload an image")
#                 return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
        
#             sponsor = addSponsor(form.name.data, form.url.data, program_id, image_url)
#             if type(sponsor) == str:
#                 if sponsor == "Overflow":
#                     flash("Sponsors Limit Exceeded!")
#                     return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
#                 flash(sponsor)
#                 return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
#             flash("Sponsor Added!")
#         return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

        
# @admin.route('/updateData', methods = ['POST'])
# @login_required
# @role_required("admin")
# def updateDataView():
#     # return request.form
#     try:
#         program_id = request.form['programId']
#     except:
#         return "No programId"
#         return Response(status = 400)

#     program_id = request.form['programId']


#     if program_id.startswith("EV"):
#         # contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.event_id == program_id)).count()
#         # faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.event_id == program_id)).count()
#         # sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.event_id == program_id)).count()
#         program = Event.query.filter_by(eventId= program_id).first()

#     elif program_id.startswith("WS"):
#         # contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.event_id == program_id)).count()
#         # faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.event_id == program_id)).count()
#         # sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.event_id == program_id)).count()
#         program = Workshop.query.filter_by(workshopId= program_id).first()

#     else:
#         return Response(status = 400)

#     if not program:
#         return Response(status = 400)

#     # return "caught"
#     if request.form.get('update-contacts-form'):
#         form = Contacts()
#         return render_template('update_contacts.html',form = form, contacts = program.contacts, program_id = program_id)

#     elif request.form.get('update-faqs-form'):
#         form = FAQs()
#         return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

#     elif request.form.get('update-sponsors-form'):
#         form = Sponsors()
#         return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)

#     elif request.form.get("update-contact"):
#         form = Contacts()
#         if form.validate_on_submit():
#             # return request.form
#             # updated
#             contact_id = dict(request.form).get('update-contact')
#             contact = updateContact(form.data, contact_id, program_id)
#             if type(contact) == str:
#                 flash(contact)
#                 return render_template('update_contacts.html', form = form, contacts = program.contacts, program_id = program_id)

#             flash("Contact Updated Succesfully!")
#         return render_template('update_contacts.html', form = form, contacts = program.contacts, program_id = program_id)

#     elif request.form.get("update-faq"):
#         form = FAQs()
#         if form.validate_on_submit():

#             faq_id = dict(request.form).get('update-faq')
#             faq = updateFaq(form.data, faq_id, program_id)
#             if type(faq) == str:
#                 flash(faq)
#                 return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

#             flash("FAQ Updated Succesfully!")
#         return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

#     elif request.form.get('update-sponsor'):
#         form = Sponsors()
#         if form.validate_on_submit():

#             sponsor_id = dict(request.form).get('update-sponsor')
#             #update image
#             crop = {}
#             image_url = ""
#             base64image = form.photo.image.data

#             if base64image:
#                 crop['x'] = int(float(str(form.photo.cropX.data)))
#                 crop['y'] = int(float(str(form.photo.cropY.data)))
#                 crop['width'] = int(float(str(form.photo.cropWidth.data)))
#                 crop['height'] = int(float(str(form.photo.cropHeight.data)))
            
#                 image_url = crop_image(form.photo.image.data, crop)

#             sponsor = updateSponsor(form.data, sponsor_id, program_id, image_url)
#             if type(sponsor) == str:
#                 flash(sponsor)
#                 return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)
#             flash("Sponsors Updated Succesfully!")
#         return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)
#     return "caught"

    

@login_required
@role_required("admin")
@admin.route('/hide_user', methods=['POST'])
def hideUser():
    user_id = request.form['id']
    field = request.form['field']
    value = request.form['value']
    return "got the request", user_id, field, value


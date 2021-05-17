from operator import add
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

    if "id" in session and session['role'] == 1:
        flash("Already Logged In As Admin")
        return redirect(url_for('admin.dashboard'))
        

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == 1 and user.hidden == 0:
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
@role_required([1])
def dashboard():
    get_flashed_messages()
    return render_template("admin/dashboard.html",current_user = current_user)


@admin.route('/admins/')
@login_required
@role_required([1])
def getAdminsView():
    data = getAdminsAll()
    return render_template("users.html",role = "Admin",data = data)


@admin.route('/coordinators/')
@login_required
@role_required([1])
def getCoordinatorsView():
    data = getCoordinatorsAll()
    return render_template("users.html", role= "Coordinator",data = data)


@admin.route('/organisers/')
@login_required
@role_required([1])
def getOrganisersView():
    data = getOrganisersAll()
    return render_template("users.html", role="Organiser",data = data)


@admin.route('/events/')
@login_required
@role_required([1])
def getEventsView():
    data = getEventsAll()
    return render_template("events.html",data = data)


@admin.route('/workshops/')
@login_required
@role_required([1])
def getWorkshopsView():
    data = getWorkshopsAll()
    return render_template("workshops.html",data =data)




#Data Adding routes
@admin.route('/admins/add', methods=['GET', 'POST'])
@login_required
@role_required([1])
def addAdmin():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, form.password.data, 1, form.dept.data, form.phone.data)

        flash("You Registered a Admin Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addAdmin'))   

    return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)


@admin.route('/coordinators/add', methods=['GET', 'POST'])
@login_required
@role_required([1])
def addCoordinator():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        form.password.data
        addUser(form.userId.data, form.name.data, form.email.data, form.password.data, 2, form.dept.data, form.phone.data)

        flash("You Registered a Coordinator Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addCoordinator')) 

    return render_template('admin/register.html',role="Coordinator", form = form,current_user = current_user)


@admin.route('/event/add', methods=['GET', 'POST'])
@login_required
@role_required([1])
def addEventView():
    form = CreateEventForm(request.form)
    if form.validate_on_submit():
        organiser = form.event_organiser.data
        coordinator = User.query.filter_by(dept=organiser['dept'], role=2).first()
        if coordinator is None:
            flash("No coordinator for the Dept")
            return redirect(url_for('admin.addEventView'))
        
        organiser = addUser(organiser['userId'], organiser['name'], organiser['email'], organiser['password'], 3, organiser['dept'], organiser['phone'])
        addEvent(form.title.data, coordinator.dept , coordinator.id, organiser.id)

        flash("Event added successfully")
        flash("Organiser added successfully")
        # flash("Check Email to reset password")
        return redirect(url_for('admin.addEventView'))

    return render_template('add_event.html', form=form)

@admin.route('/event/update', methods= ['GET', 'POST'])
@login_required
@role_required([1])
def updateEventView():
    form = UpdateEventForm()
    if request.method == 'POST':
        if request.form.get('update-button'):
            event_id = request.form['event_id']
            event = Event.query.filter_by(id = event_id).first()
            if not event:
                return "Invalid event"

            if not workshop.image_url:
                workshop.image_url = "http://tzimageupload.s3.amazonaws.com/back.jpg"

            markup = dict_markup({
                "description": event.description,
                "brief": event.brief,
                "status": event.status,
                "structure": event.structure,
                "timeline": event.timeline,
                "rules": event.rules,
            })
            return render_template('update_event.html', form = form, event = event, markup = markup)
        if form.validate_on_submit():
            return request.form


@admin.route('/workshop/add', methods=['GET', 'POST'])
@login_required
@role_required([1])
def addWorkshopView():
    form = CreateWorkshopForm(request.form)
    if form.validate_on_submit():
        # return request.form
        organiser = form.workshop_organiser.data
        coordinator_id = current_user.id

        organiser = addUser(organiser['userId'], organiser['name'], organiser['email'], organiser['password'], 3, organiser['dept'], organiser['phone'])
        addWorkshop(form.title.data, form.dept.data, coordinator_id, organiser.id)

        flash("Workshop Added Succesfully")
        flash("Organiser Added Succesfully")

        return redirect(url_for('admin.addWorkshopView'))

    return render_template('add_workshop.html', form = form)


@admin.route('/workshop/update', methods=['GET', 'POST'])
@login_required
@role_required([1])
def updateWorkshopView():
    form = UpdateWorkshopForm(request.form)
    if request.method == 'POST':
        if request.form.get('update-button'):
            workshop_id = request.form['workshop_id']
            workshop = Workshop.query.filter_by(id = workshop_id).first()
            if not workshop:
                return "Invalid Workshop"

            if not workshop.image_url:
                workshop.image_url = "http://tzimageupload.s3.amazonaws.com/back.jpg"

            markup = dict_markup({
                "status": workshop.status,
                "description": workshop.description,
                "about": workshop.about,
                "timeline": workshop.timeline,
                "resources": workshop.resources,
                })
            return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup)

        if form.validate_on_submit():
            # return request.form
            workshop = updateWorkshop(form.data, request.form['workshop_id'])
            if type(workshop) == str:
                return workshop
            markup = dict_markup({
                "status": workshop.status,
                "description": workshop.description,
                "about": workshop.about,
                "timeline": workshop.timeline,
                "resources": workshop.resources,
                })
            flash("Workshop Updated Succesfully!")
            return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup)


            #update image            
            # crop = {}
            # base64image = form.photo.image.data

            # image_url = ""
            # if base64image:    
            #     crop['x'] = int(float(str(form.photo.cropX.data)))
            #     crop['y'] = int(float(str(form.photo.cropY.data)))
            #     crop['width'] = int(float(str(form.photo.cropWidth.data)))
            #     crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
            #     image_url = crop_image(form.photo.image.data, crop)




    return redirect(url_for('admin.getWorkshopsView'))


@admin.route('/addData', methods=["POST"])
@login_required
@role_required([1])
def addDataView():
    try:
        program_id = request.form['programId']
    except:
        return Response(status = 400)

    program_id = request.form['programId']

    if program_id.startswith("EV"):
        program = Event.query.filter_by(eventId= program_id).first()
    elif program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
    else:
        return Response(status = 400)

    if not program:
        return Response(status = 400)

    contacts = Contact.query.filter(and_(Contact.hidden == 0, or_(Contact.workshop_id == program.id, Contact.event_id == program.id))).count()
    faqs = FAQ.query.filter(and_(FAQ.hidden == 0, or_(FAQ.workshop_id == program.id, FAQ.event_id == program.id))).count()
    sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, or_(Sponsor.workshop_id == program.id, Sponsor.event_id == program.id))).count()

    #for FORMS
    if request.form.get("add-faq-form"):
        form = FAQs()
        return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
    
    elif request.form.get("add-contact-form"):
        form = Contacts()
        return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

    elif request.form.get('add-sponsor-form'):
        form = Sponsors()
        return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)


    #TO ADD the data
    elif request.form.get("add-contact"):
        form = Contacts()
        if form.validate_on_submit():
            contact = addContact(request.form['name'], request.form['email'], request.form['phone'], program_id)
            if type(contact) == str:
                if contact == "Overflow":
                    flash("Contacts Limit Exceeded!")
                    return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
                flash(contact)
                return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
            flash("Contact  Added!")
        return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

    elif request.form.get("add-faq"):
        form = FAQs()
        if form.validate_on_submit():
            faq = addFaq(form.question.data, form.answer.data, program_id)
            if type(faq) == str:
                if faq == "Overflow":
                    flash("Faqs Limit Exceeded!")
                    return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
                flash(faq)
                return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
            flash("FAQ Added!")
        return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

    elif request.form.get("add-sponsor"):
        form = Sponsors()
        if form.validate_on_submit():
            # return request.form

            # adding image
            image_url = ""
            crop = {}
            try:
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
            except:
                flash("No image uploaded")
                return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

            
            url = crop_image(form.photo.image.data, crop)
            if not url:
                flash("Something went wrong")
            else:
                image_url = url
                
            
            sponsor = addSponsor(form.name.data, form.url.data, program_id, image_url)
            if type(sponsor) == str:
                if sponsor == "Overflow":
                    flash("Sponsors Limit Exceeded!")
                    return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
                flash(sponsor)
                return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
            flash("Sponsor Added!")
        return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

        
@admin.route('/updateData', methods = ['POST'])
@login_required
@role_required([1])
def updateDataView():
    # return request.form
    try:
        program_id = request.form['programId']
    except:
        return "No programId"
        return Response(status = 400)

    program_id = request.form['programId']

    if program_id.startswith("EV"):
        program = Event.query.filter_by(eventId = program_id).first()
        program_id = program.eventId
    elif program_id.startswith("WS"):
        program = Workshop.query.filter_by(workshopId = program_id).first()
        program_id = program.workshopId
    else:
        return Response(status = 400)

    if not program:
        return Response(status = 400)
    contacts = Contact.query.filter(and_(Contact.hidden == 0, or_(Contact.workshop_id == program.id, Contact.event_id == program.id))).count()
    faqs = FAQ.query.filter(and_(FAQ.hidden == 0, or_(FAQ.workshop_id == program.id, FAQ.event_id == program.id))).count()
    sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, or_(Sponsor.workshop_id == program.id, Sponsor.event_id == program.id))).count()

    # return "caught"
    if request.form.get('update-contacts-form'):
        form = Contacts()
        return render_template('update_contacts.html',form = form, contacts = program.contacts, program_id = program_id)

    elif request.form.get('update-faqs-form'):
        form = FAQs()
        return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

    elif request.form.get('update-sponsors-form'):
        form = Sponsors()
        return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)

    elif request.form.get("update-contact"):
        form = Contacts()
        if form.validate_on_submit():
            # return request.form
            # updated
            contact_id = dict(request.form).get('update-contact')
            contact = updateContact(form.data, contact_id, program_id)
            if type(contact) == str:
                flash(contact)
                return render_template('update_contacts.html', form = form, contacts = program.contacts, program_id = program_id)

            flash("Contact Updated Succesfully!")
        return render_template('update_contacts.html', form = form, contacts = program.contacts, program_id = program_id)

    elif request.form.get("update-faq"):
        form = FAQs()
        if form.validate_on_submit():

            faq_id = dict(request.form).get('update-faq')
            faq = updateFaq(form.data, faq_id, program_id)
            if type(faq) == str:
                flash(faq)
                return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

            flash("FAQ Updated Succesfully!")
        return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

    elif request.form.get('update-sponsor'):
        form = Sponsors()
        if form.validate_on_submit():

            sponsor_id = dict(request.form).get('update-sponsor')
            #update image
            crop = {}
            image_url = ""
            base64image = form.photo.image.data

            if base64image:
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
            
                image_url = crop_image(form.photo.image.data, crop)

            sponsor = updateSponsor(form.data, sponsor_id, program_id, image_url)
            if type(sponsor) == str:
                flash(sponsor)
                return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)
            flash("Sponsors Updated Succesfully!")
        return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)
    return "caught"

    

@login_required
@role_required([1])
@admin.route('/hide_user', methods=['POST'])
def hideUser():
    user_id = request.form['id']
    field = request.form['field']
    value = request.form['value']
    return "got the request", user_id, field, value


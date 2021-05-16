from operator import add
from flask import url_for, redirect, request, render_template, Blueprint, session, flash, escape, get_flashed_messages, Markup, jsonify
import flask
from flask.ctx import after_this_request
from flask.globals import current_app
import flask_session
from werkzeug.utils import secure_filename
from app.models import User
from app.forms import AddWorkshopForm, LoginForm, CreateEventForm, PhotoForm, RegisterForm, Contacts, FAQs, Sponsors, UpdateEventForm, UpdateWorkshopForm
from app import db, app, bcrypt
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import roles
import cv2
import os

import urllib

from app.admin import admin
from app.admin.functions import *
from app.functions import *
from app.controllers import login_manager
from app.mynav import mynav

from app.middlewares import role_required
from app import ckeditor



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
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        addUser(form.userId.data, form.name.data, form.email.data, hashed_password, 1, form.dept.data, form.phone.data)

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
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        addUser(form.userId.data, form.name.data, form.email.data, hashed_password, 2, form.dept.data, form.phone.data)

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
        
        hashed_password = bcrypt.generate_password_hash(organiser['password'])
        organiser = addUser(organiser['userId'], organiser['name'], organiser['email'], hashed_password, 3, organiser['dept'], organiser['phone'])
        addEvent(form.title.data, coordinator.dept , coordinator.id, organiser.id)

        flash("Event added successfully")
        flash("Organiser added successfully")
        # flash("Check Email to reset password")
        return redirect(url_for('admin.addEventView'))

    return render_template('add_event.html', form=form)





@admin.route('/workshop/add', methods=['GET', 'POST'])
@login_required
@role_required([1])
def addWorkshopView():
    form = AddWorkshopForm(request.form)
    if request.method == "POST":

        print(form.errors)

        if request.form.get("skip"):
            return redirect(url_for("admin.dashboard"))
        elif request.form.get('add-workshop') or request.form.get('add-contact') or request.form.get('add-faq') or request.form.get('add-sponsor'):
            form = AddWorkshopForm()
            if form.validate_on_submit():
                                
                #adding image
                crop = {}
                try:
                    crop['x'] = int(float(str(form.photo.cropX.data)))
                    crop['y'] = int(float(str(form.photo.cropY.data)))
                    crop['width'] = int(float(str(form.photo.cropWidth.data)))
                    crop['height'] = int(float(str(form.photo.cropHeight.data)))
                except:
                    flash("No image uploaded")
                    return render_template('add_workshop.html', form=form)

                workshop = addWorkshop(form.title.data, form.dept.data, form.description.data, form.fee.data, form.status.data, form.about.data, form.timeline.data, form.resources.data, current_user.id)

                
                status = crop_and_save_image(form.photo.image.data, crop, 'workshop', workshop.id)
                if not status:
                    flash("Something went wrong")
                
                contact = addContactToWorkshop(request.form['primary_contact-name'], request.form['primary_contact-email'], request.form['primary_contact-phone'], workshop.id)
                if type(contact) == str:
                    flash(contact)
                    return render_template('add_workshop.html', form=form)

                flash("Workshop Added Succesfully")

                if request.form.get('submit'):
                    return redirect(url_for('admin.dashboard'))

                elif request.form.get('add-contact'):
                    form = Contacts()
                    return render_template('add_contacts.html', form=form, program_id = workshop.id, count = 2)

                elif request.form.get('add-faq'):
                    form = FAQs()
                    return render_template('add_faqs.html', form=form, program_id = workshop.id, count = 1)
                
                elif request.form.get('add-sponsor'):
                    # return "On Sponsors"
                    form = Sponsors()
                    return render_template('add_sponsors.html', form = form, program_id = workshop.id, count = 1)
            return render_template('add_workshop.html', form=form)


        workshop_id = request.form['programId']
        workshop = Workshop.query.filter_by(id = workshop_id).first()
        if not workshop:
            flash("Invalid Request")
            return redirect(url_for('admin.dashboard'))

        if request.form.get("add-faq-from"):
            form = FAQs()
            return render_template('add_faqs.html', form = form, program_id = workshop_id, count = len(workshop.faqs)+1)
            
        elif request.form.get("add-contact-from"):
            form = Contacts()
            return render_template('add_contacts.html', form = form, program_id = workshop_id, count = len(workshop.contacts)+1)

        elif request.form.get('add-sponsor-from'):
            form = Sponsors()
            return render_template('add_sponsors.html', form = form, program_id = workshop_id, count = len(workshop.sponsors)+1)


        elif request.form.get("add-contact-to-program"):
            form = Contacts()
            if form.validate_on_submit():
                contact = addContactToWorkshop(request.form['name'], request.form['email'], request.form['phone'], workshop_id)
                if type(contact) == str:
                    if contact == "Overflow":
                        flash("Contacts Limit Exceeded!")
                        return render_template('add_contacts.html', form = form, program_id = workshop_id, count = len(workshop.contacts)+1, hide_form = 1)
                    flash(contact)
                    return render_template('add_contacts.html', form = form, program_id = workshop_id, count = len(workshop.contacts)+1)
                flash("Contact "+str(len(workshop.contacts))+" Added!")
            return render_template('add_contacts.html', form = form, program_id = workshop_id, count = len(workshop.contacts)+1)

        elif request.form.get("add-faq-to-program"):
            form = FAQs()
            if form.validate_on_submit():
                faq = addFaqToWorkshop(form.question.data, form.answer.data, workshop_id)
                if type(faq) == str:
                    if faq == "Overflow":
                        flash("Faqs Limit Exceeded!")
                        return render_template('add_faqs.html', form = form, program_id = workshop_id, count = len(workshop.faqs)+1, hide_form = 1)
                    flash(faq)
                    return render_template('add_faqs.html', form = form, program_id = workshop_id, count = len(workshop.faqs) +1)
                flash("FAQ "+ str(len(workshop.faqs)) + "Added!")
            return render_template('add_faqs.html', form = form, program_id = workshop_id, count = len(workshop.faqs) +1)

        elif request.form.get("add-sponsor-to-program"):
            app.logger.warning(str("kkjsdkfjlskdjflksdjflksdjflksdjflksdjflksdjflks")+ str(workshop_id))
            form = Sponsors()
            if form.validate_on_submit():
                # return request.form

                #adding image
                image_url = ""
                crop = {}
                try:
                    crop['x'] = int(float(str(form.photo.cropX.data)))
                    crop['y'] = int(float(str(form.photo.cropY.data)))
                    crop['width'] = int(float(str(form.photo.cropWidth.data)))
                    crop['height'] = int(float(str(form.photo.cropHeight.data)))
                except:
                    flash("No image uploaded")
                    return render_template('add_sponsors.html', form = form, program_id = workshop_id, count = len(workshop.sponsors))

                
                url = crop_and_save_image(form.photo.image.data, crop, 'sponsor', workshop.id)
                if not url:
                    flash("Something went wrong")
                else:
                    image_url = url
                    
                
                sponsor = addSponsorToWorkshop(form.name.data, form.url.data, workshop_id, image_url)
                if type(sponsor) == str:
                    if sponsor == "Overflow":
                        flash("Sponsors Limit Exceeded!")
                        return render_template('add_sponsors.html', form = form, program_id = workshop_id, count = len(workshop.sponsors)+1, hide_form = 1)
                    flash(sponsor)
                    return render_template('add_sponsors.html', form = form, program_id = workshop_id, count = len(workshop.sponsors) +1)
                flash("Sponsor "+ str(len(workshop.sponsors)) + "Added!")
            return render_template('add_sponsors.html', form = form, program_id = workshop_id, count = len(workshop.sponsors) +1)

    return render_template('add_workshop.html', form=form)

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

            if len(workshop.images):
                image_url = workshop.images[0].image_url
            else:
                image_url = "/static/back.jpg"

            markup = dict_markup({
                "status": workshop.status,
                "description": workshop.description,
                "about": workshop.about,
                "timeline": workshop.timeline,
                "resources": workshop.resources,
                })
            return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup, image_url=image_url)
        
        elif request.form.get('update-contacts-from'):
            workshop_id = request.form['update-contacts-from']
            workshop = Workshop.query.filter_by(id = workshop_id).first()
            if not workshop:
                return "Invalid"
            form = Contacts()
            return render_template('update_contacts.html',form = form, contacts = workshop.contacts, workshop_id = workshop.id)

        # elif request.form.get("upload-image-to-program"):
        #     form = PhotoForm()
        #     workshop_id = request.form['programId']
        #     workshop = Workshop.query.filter_by(id = workshop_id).first()
        #     if form.validate_on_submit():
        #         return request.form
        #     return form.errors
        elif request.form.get('update-faqs-from'):
            workshop_id = request.form['update-faqs-from']
            workshop = Workshop.query.filter_by(id = workshop_id).first()
            if not workshop:
                return "Invalid"
            form = FAQs()
            return render_template('update_faqs.html',form = form, faqs = workshop.faqs, workshop_id = workshop.id)

        elif request.form.get('update-sponsors-from'):
            workshop_id = request.form['update-sponsors-from']
            workshop = Workshop.query.filter_by(id = workshop_id).first()
            if not workshop:
                return "Invalid"
            form = Sponsors()
            return render_template('update_sponsors.html',form = form, sponsors = workshop.sponsors, workshop_id = workshop.id)

  
        elif request.form.get("update-contact"):
            form = Contacts()
            if form.validate_on_submit():
                # updated
                contact_id = dict(request.form).get('update-contact')
                workshop_id =  dict(request.form).get('workshop_id')
                contacts = updateWorkshop(form.data, contact_id, workshop_id,'contact')

                flash(contacts[1])
                return render_template('update_contacts.html',form = form, contacts =contacts[0], workshop_id = workshop_id)

            else:
                workshop_id = request.form['workshop_id']
                workshop = Workshop.query.filter_by(id = workshop_id).first()
                if not workshop:
                    return "Invalid"
                return render_template('update_contacts.html',form = form, contacts = workshop.contacts, workshop_id = workshop.id)

        elif request.form.get("update-faq"):
            form = FAQs()
            if form.validate_on_submit():

                faq_id = dict(request.form).get('update-faq')
                workshop_id =  dict(request.form).get('workshop_id')
                faqs = updateWorkshop(form.data, faq_id, workshop_id,'faq')
            
                flash(faqs[1])
                return render_template('update_faqs.html',form = form, faqs =faqs[0], workshop_id = workshop_id)

            else:
                workshop_id = request.form['workshop_id']
                workshop = Workshop.query.filter_by(id = workshop_id).first()
                if not workshop:
                    return "Invalid"
                return render_template('update_faqs.html',form = form, faqs = workshop.faqs, workshop_id = workshop.id)

        elif request.form.get('update-sponsor'):
            form = Sponsors()
            if form.validate_on_submit():

                sponsor_id = dict(request.form).get('update-sponsor')
                workshop_id = dict(request.form).get('workshop_id')
                #update image
                crop = {}

                try:
                    crop['x'] = int(float(str(form.photo.cropX.data)))
                    crop['y'] = int(float(str(form.photo.cropY.data)))
                    crop['width'] = int(float(str(form.photo.cropWidth.data)))
                    crop['height'] = int(float(str(form.photo.cropHeight.data)))
                except:
                    flash("Please add an image")
                
                image_url = crop_and_save_image(form.photo.image.data, crop, 'sponsor', sponsor_id)
                form.data['image_url'] = image_url

                sponsors = updateWorkshop(form.data, sponsor_id, workshop_id,  'sponsor')                

                flash(sponsors[1])
                return render_template('update_sponsors.html',form = form, sponsors =sponsors[0], workshop_id = workshop_id)

            else:
                workshop_id = request.form['workshop_id']
                workshop = Workshop.query.filter_by(id = workshop_id).first()
                if not workshop:
                    return "Invalid"
                return render_template('update_sponsors.html',form = form, sponsors = workshop.sponsors, workshop_id = workshop.id)


        elif form.validate_on_submit():#update-workshop


            workshop_id = dict(request.form).get('update-workshop')

            #update image
            crop = {}

            try:
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
            except:
                flash("Please add an image")
            image_status = crop_and_save_image(form.photo.image.data, crop, 'workshop', workshop_id)

            markup = updateWorkshop(form.data, workshop_id, 'markup')
        
            flash(markup[1])
            return render_template('update_sponsors.html',form = form, markup =markup[0], workshop_id = workshop_id)

            
        else:
            return form.errors
    return redirect(url_for('admin.getWorkshopsView'))

@login_required
@role_required([1])
@admin.route('/hide_user', methods=['POST'])
def hideUser():
    user_id = request.form['id']
    field = request.form['field']
    value = request.form['value']
    return "got the request", user_id, field, value


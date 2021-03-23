from operator import add
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask.ctx import after_this_request
from flask.globals import current_app
from werkzeug.utils import secure_filename
from app.models import User
from app.forms import AddWorkshopForm, LoginForm, CreateEventForm, RegisterForm, PhotoForm
from app import db
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import roles
# from PIL import Image
import os

import urllib

from app.admin import admin
from app.admin.functions import *
from app.functions import *
from app.controllers import login_manager
from app.mynav import mynav

from app.middlewares import admin_authenticated
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

        if user and user.password == form.password.data:
            if user.role == 1 and user.hidden == 0:
                login_user(user)
                session['id'] = user.id
                session['role'] = user.role
                return redirect(url_for("admin.dashboard"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form)
    
        
#Data fetching routes
@admin.route('/dashboard/')
@login_required
@admin_authenticated
def dashboard():
    return render_template("admin/dashboard.html",current_user = current_user)


@admin.route('/admins/')
@login_required
@admin_authenticated
def getAdminsView():
    data = getAdminsAll()
    return render_template("users.html",role = "Admin",data = data)


@admin.route('/coordinators/')
@login_required
@admin_authenticated
def getCoordinatorsView():
    data = getCoordinatorsAll()
    return render_template("users.html", role= "Coordinator",data = data)


@admin.route('/organisers/')
@login_required
@admin_authenticated
def getOrganisersView():
    data = getOrganisersAll()
    return render_template("users.html", role="Organiser",data = data)


@admin.route('/events/')
@login_required
@admin_authenticated
def getEventsView():
    data = getEventsAll()
    return render_template("events.html",data = data)


@admin.route('/workshops/')
@login_required
@admin_authenticated
def getWorkshopsView():
    data = getWorkshopsAll()
    return render_template("workshops.html",data =data)




#Data Adding routes
@admin.route('/admins/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
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
@admin_authenticated
def addCoordinator():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        addUser(form.userId.data, form.name.data, form.email.data, form.password.data, 2, form.dept.data, form.phone.data)

        flash("You Registered a Coordinator Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addCoordinator')) 

    return render_template('admin/register.html',role="Coordinator", form = form,current_user = current_user)


@admin.route('/event/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
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
        flash("Check Email to reset password")
        return redirect(url_for('admin.addEventView'))

    return render_template('add_event.html', form=form)


@admin.route('/workshop/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
def addWorkshopView():
    form = AddWorkshopForm(request.form)

    if request.method == 'POST':
        # print(form)
        return "GOtcha"
        # return request.form['description']

      
        data = request.form['uri']

        response = urllib.request.urlopen(data)
        with open('app/uploads/fuck.jpg', 'wb') as f:  
            f.write(response.file.read())

        return "Success"

    return render_template('add_workshop.html', form=form)




@login_required
@admin_authenticated
@admin.route('/hide_user', methods=['POST'])
def hideUser():
    user_id = request.form['id']
    field = request.form['field']
    value = request.form['value']
    return "got the request", user_id, field, value


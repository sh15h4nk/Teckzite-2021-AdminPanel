from operator import add
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask.ctx import after_this_request
from flask.globals import current_app
from app.models import User
from app.forms import AddWorkshopForm, LoginForm, CreateEventForm, RegisterForm
from app import db
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import roles


from app.admin import admin
from app.admin.functions import *
from app.functions import sendMail
from app.controllers import login_manager
from app.mynav import mynav

from app.middlewares import admin_authenticated
from app import ckeditor

from app.middlewares import generate_event_id, generate_workshop_id, generate_techzite_id

@admin.route('/')
def home():
    return render_template('admin/index.html')

@admin.route("/logout/")
def logout():
    logout_user()
    session.pop('userId', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))


@admin.route('/login/', methods=['GET', 'POST'])
def login():

    if "userId" in session:
        if session['role']==1:
            flash("Already Logged In As Admin")
            return redirect(url_for('admin.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and user.password == form.password.data:
            if user.role == 1:
                login_user(user)
                session['id'] = form.userId.data
                session['role'] = user.role
                return redirect(url_for("admin.dashboard"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form)
    
        


@admin.route('/admins/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
def addAdmin():

    form = RegisterForm(request.form)

    if request.method == "POST":

        if not form.validate_on_submit():
            return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)

        user = User.query.filter_by(userId = form.userId.data).first()

        if not user:

            email_already_exists = User.query.filter_by(email=form.email.data).first()

            if email_already_exists:
                flash('Email already exists! ')
                return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)
            
            phone_already_exists = User.query.filter_by(phone=form.phone.data).first()

            if phone_already_exists:
                flash('Phone Number already exists! ')
                return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)

            user = User(form.userId.data, form.name.data, form.email.data, form.password.data, 1, form.dept.data, form.phone.data)  #updated
            db.session.add(user)
            db.session.commit()


            sendMail(user)

            flash("You Registered a Admin Succesfully")
            flash("Email has been sent to reset the password")


            return redirect(url_for('admin.addAdmin'))
            
        else:
            flash("User already exists")    

    return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)
   
@admin.route('/coordinators/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
def addCoordinator():

    form = RegisterForm(request.form)
    if request.method == "POST":
        
        if not form.validate_on_submit():
            return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)
            
        user = User.query.filter_by(userId = form.userId.data).first()

        if not user:

            email_already_exists = User.query.filter_by(email=form.email.data).first()

            if email_already_exists:
                flash('Email already exists! ')
                return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)
            
            phone_already_exists = User.query.filter_by(phone=form.phone.data).first()

            if phone_already_exists:
                flash('Phone Number already exists! ')
                return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)

            user = User(form.userId.data, form.name.data, form.email.data, form.password.data, 2, form.dept.data, form.phone.data)  #updated
            db.session.add(user)
            db.session.commit()


            sendMail(user)

            flash("You Registered a Coordinator Succesfully")
            flash("Email has been sent to reset the password")


            return redirect(url_for('admin.addCoordinator'))
            
        else:
            flash("User already exists")    

    return render_template('admin/register.html',role="Coordinator", form = form,current_user = current_user)
        


@admin.route('/dashboard/')
@login_required
@admin_authenticated
def dashboard():
    return render_template("admin/dashboard.html",current_user = current_user)


@admin.route('/admins/')
@login_required
@admin_authenticated
def getAdminsView():
    data = getAdmins()
    return render_template("users.html",role = "Admin",data = data)
    
@admin.route('/coordinators/')
@login_required
@admin_authenticated
def getCoordinatorsView():
    data = getCoordinators()
    return render_template("users.html", role= "Coordinator",data = data)

@admin.route('/organisers/<dept>')
@login_required
@admin_authenticated
def getOrganisersView(dept):
    data = getOrganisers(dept)
    return render_template("users.html", role= dept+" Organiser",data = data)
    


@admin.route('/events/<dept>')
@login_required
@admin_authenticated
def getEventsView(dept):
    data = getEvents(dept)
    # res = data['no_cols']
    # return data
    return render_template("events.html",role=dept+" Events",data = data)


@admin.route('/event/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
def addEventView():

    form = CreateEventForm(request.form)

    if form.validate_on_submit():       
        # return "Validated"
        organiser = form.event_organiser.data

        coordinator = User.query.filter_by(dept=organiser['dept'], role=2).first()
        if coordinator is None:
            flash("No coordinator for the Dept")
            return redirect(url_for('admin.addEventView'))
        # return organiser['dept']
        organiser = User(organiser['userId'], organiser['name'], organiser['email'], organiser['password'], 3, organiser['dept'], organiser['phone'])
        db.session.add(organiser)
        db.session.commit()

        

        eventId = generate_event_id()
        
        event = Event(eventId, form.title.data, coordinator.dept , coordinator.id, organiser.id)
        db.session.add(event)
        db.session.commit()
        flash("Event added successfully")
        return redirect(url_for('admin.addEventView'))

    return render_template('add_event.html', form=form)

        

        


@admin.route('/workshops/')
@login_required
@admin_authenticated
def getWorkshopsView():
    data = getWorkshops()
    return data


@admin.route('/workshop/add')
@login_required
@admin_authenticated
def addWorkshopView():
    form = AddWorkshopForm(request.form)

    if request.method == 'GET':
        return render_template("add_workshop.html", form=form)

    else:
        eventId = request.form.get('eventid')
        eventName = request.form.get('eventname')
        teamSize = request.form.get('teamsize')
        data = request.form.get('text')

        addEvent(eventId, eventName, teamSize, data)    #yet to update

        return redirect(url_for('admin.addWorkshopView'))









@login_required
@admin_authenticated
@admin.route('/hide_user', methods=['POST'])
def hideUser():
    user_id = request.form['id']
    field = request.form['field']
    value = request.form['value']
    return "got the request", user_id, field, value


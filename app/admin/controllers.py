from operator import add
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask.ctx import after_this_request
from flask.globals import current_app
from app.models import User
from app.admin.forms import RegisterForm
from app.forms import LoginForm
from app import db
from app import app
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import roles

from app.admin import admin
from app.admin.functions import *
from app.controllers import login_manager
from app.mynav import mynav

from app.middlewares import admin_authenticated


@admin.route('/')
def home():
    return render_template('admin/index.html')

@admin.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))


@admin.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session:
        if session['role']==1:
            flash("Already Logged In As Admin")
            return redirect(url_for('admin.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(id=form.id.data).first()

        if user and user.password == form.password.data:
            if user.role == 1:
                login_user(user)
                session['id'] = form.id.data
                session['role'] = user.role
                return redirect(url_for("admin.dashboard"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form)
    
        


@admin.route('/admins/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
def addAdmin():

    if request.method == "POST":
        form = RegisterForm(request.form)

        user = User.query.filter_by(id = form.id.data).first()

        if not user:
            user = User(form.id.data, form.password.data, role=1)
            db.session.add(user)
            db.session.commit()
            session['id'] = form.id.data
            flash("You Registered a User Succesfully")
            
        else:
            flash("User already exists")    
    form = RegisterForm()
    return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)
   
@admin.route('/coordinaters/add', methods=['GET', 'POST'])
@login_required
@admin_authenticated
def addCoordinater():

    if request.method == "POST":
        form = RegisterForm(request.form)

        user = User.query.filter_by(id = form.id.data).first()

        if not user:
            user = User(form.id.data, form.password.data, role=2)
            db.session.add(user)
            db.session.commit()
            session['id'] = form.id.data
            flash("You Registered a User Succesfully")
            
        else:
            flash("User already exists")    
    form = RegisterForm()
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
    
@admin.route('/coordinaters/')
@login_required
@admin_authenticated
def getCoordinatersView():
    data = getCoordinaters()
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
    if request.method == 'GET':
        return render_template("admin/add_event.html")

    else:
        eventId = request.form.get('eventid')
        eventName = request.form.get('eventname')
        teamSize = request.form.get('teamsize')
        data = request.form.get('text')

        addEvent(eventId, eventName, teamSize, data)

        return redirect(url_for('admin.addEventView'))


@admin.route('/workshop/show')
@login_required
@admin_authenticated
def getWorkshopsView():
    data = getWorkshops()
    return data

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
from app.admin.functions import addEventToDb, getAdmins, getEvents, getWorkshops
from app.controllers import login_manager
from app.mynav import mynav

mynav.init_app(app)



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
        flash("Already Logged In")
        return redirect(url_for('admin.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(id=form.id.data).first()

        if user and user.password == form.password.data:
            if user.role == 1:
                login_user(user)
                session['id'] = form.id.data
                session['role'] = user.role
                flash("Login successful")
                return redirect(url_for("admin.dashboard"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form)
    
        


@admin.route('/register/', methods=['GET', 'POST'])
@login_required
def register():

    if request.method == "POST":
        form = RegisterForm(request.form)

        user = User.query.filter_by(id = form.id.data).first()

        if not user and ( session['role'] < form.role.data or session['role'] == 1) :
            user = User(form.id.data, form.password.data, form.role.data)
            db.session.add(user)
            db.session.commit()
            session['id'] = form.id.data
            flash("You Registered a User Succesfully")
            
        else:
            flash("Not Authorised or User already exists")    
    form = RegisterForm()
    return render_template('admin/register.html', form = form,current_user = current_user)
   

@admin.route('/dashboard/')
@login_required
def dashboard():
    return render_template("admin/dashboard.html",current_user = current_user)


@admin.route('/admin/show/<role>')
@login_required
def retriveAdminRows(role):
    if current_user.role != 1: 
        if current_user.role < role:
            return "403"
    data = getAdmins(int(role))
    return data
    

@admin.route('/event/show')
@login_required
def retriveEvents():
    data = getEvents()
    # res = data['no_cols']
    # return data
    return render_template("admin/events.html",data = data)


@admin.route('/event/add', methods=['GET', 'POST'])
@login_required
def addEvent():
    if request.method == 'GET':
        return render_template("admin/add_event.html")

    else:
        eventId = request.form.get('eventid')
        eventName = request.form.get('eventname')
        teamSize = request.form.get('teamsize')
        data = request.form.get('text')

        addEventToDb(eventId, eventName, teamSize, data)

        return redirect(url_for('admin.addEvent'))


@admin.route('/workshop/show')
@login_required
def retriveWorkshops():
    data = getWorkshops()
    return data


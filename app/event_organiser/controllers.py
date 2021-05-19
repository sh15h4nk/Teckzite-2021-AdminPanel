from types import resolve_bases
from app.middlewares import role_required
from app import app, db, bcrypt
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import LoginForm
from app.models import User
from app.controllers import login_manager
from app.mynav import mynav
from app.event_organiser.functions import *
mynav.init_app(app)



from app.event_organiser import event_organiser



@event_organiser.route('/')
def home():
    return render_template('event_organiser/index.html')



@event_organiser.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@event_organiser.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session and session['role'] == "event_organiser":
        flash("Already Logged In As Coordinator")
        return redirect(url_for('event_organiser.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "event_organiser" and user.hidden == 0:
            	login_user(user)
            	session['id'] = user.id
            	session['role'] = user.role
            	return redirect(url_for('event_organiser.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form = form, role = "Event Organiser")

@event_organiser.route('/dashboard/')
@login_required
@role_required(['event_organiser'])
def dashboard():
    return render_template("event_organiser/dashboard.html",current_user = current_user)




@event_organiser.route('/events/')
@login_required
@role_required("event_organiser")
def getEventsView():
    data = getEventsAll(event_organiser_id = current_user.id)
    return render_template("events.html",data = data)
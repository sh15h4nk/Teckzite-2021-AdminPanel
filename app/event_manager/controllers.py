from app.middlewares import role_required
from app import app, db, bcrypt
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import *
from app.models import User
from app.controllers import login_manager
from app.mynav import mynav
from app.event_manager.functions import *
from app.functions import *
mynav.init_app(app)



from app.event_manager import event_manager


@event_manager.route('/')

def home():
    return render_template('workshop_manager/index.html')



@event_manager.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@event_manager.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session and session['role'] == "event_manager":
        flash("Already Logged In As event_manager")
        return redirect(url_for('event_manager.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "event_manager" and user.hidden == 0:
            	login_user(user)
            	session['id'] = user.id
            	session['role'] = user.role
            	return redirect(url_for('event_manager.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form = form, role = "Event Manager")

@event_manager.route('/dashboard/')
@login_required
@role_required(["event_manager"])
def dashboard():
    return render_template("event_manager/dashboard.html",current_user = current_user)


#DATA retrival

@event_manager.route('/event.coordinators/')
@login_required
@role_required("event_manager")
def getEventCoordinatorsView():
    data = getEventCoordinatorsAll()
    return render_template("users.html", role= "Event Coordinator",data = data)

@event_manager.route('/event.organiser/')
@login_required
@role_required("event_manager")
def getEventOrganisersView():
    data = getEventOrganisersAll()
    return render_template("users.html", role= "Event Organiser",data = data)


@event_manager.route('/events/')
@login_required
@role_required("event_manager")
def getEventsView():
    data = getEventsAll()
    return render_template("events.html",data = data)

# DATA adding routes

# @event_manager.route('/event/add', methods=['GET', 'POST'])
# @login_required
# @role_required("event_manager")
# def addEventView():
#     form = CreateEventForm(request.form)
#     if form.validate_on_submit():
#         event_organiser = form.event_organiser.data
#         event_coordinator = User.query.filter_by(dept=event_organiser['dept'], role="event_coordinator").first()
#         if event_coordinator is None:
#             flash("No coordinator for the Dept")
#             return redirect(url_for('event_manager.addEventView'))
        
#         organiser = addUser(event_organiser['userId'], event_organiser['name'], event_organiser['email'], "event_organiser", event_organiser['dept'], event_organiser['phone'])
#         addEvent(form.title.data, event_coordinator.dept , event_coordinator.id, organiser.id)

#         flash("Event added successfully")
#         flash("Organiser added successfully")
#         # flash("Check Email to reset password")
#         return redirect(url_for('admin.addEventView'))

#     return render_template('add_event.html', form=form)


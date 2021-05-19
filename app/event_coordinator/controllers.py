from sqlalchemy.sql.expression import false
from app.middlewares import role_required
from app import app, db, bcrypt
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import CreateEventForm, LoginForm, UpdateProfileForm
from app.models import User
from app.controllers import login_manager
from app.mynav import mynav
from app.event_coordinator.functions import *
mynav.init_app(app)



from app.event_coordinator import event_coordinator


@event_coordinator.route('/')

def home():
    return render_template('event_coordinator/index.html')



@event_coordinator.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@event_coordinator.route('/login/', methods=['GET', 'POST'])
def login():
    
    if "id" in session and session['role'] == "event_coordinator":
        flash("Already Logged In As Coordinator")
        return redirect(url_for('event_coordinator.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "event_coordinator" and user.hidden == 0:
            	login_user(user)
            	session['id'] = user.id
            	session['role'] = user.role
            	return redirect(url_for('event_coordinator.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form = form, role = "Event Coordinator")

@event_coordinator.route('/dashboard/')
@login_required
@role_required(["event_coordinator"])
def dashboard():
    return render_template("event_coordinator/dashboard.html",current_user = current_user)



@event_coordinator.route('/event.organiser/')
@login_required
@role_required("event_coordinator")
def getEventOrganisersView():
    data = getEventOrganisersAll(dept = current_user.dept)
    return render_template("users.html", role= "Event Organiser",data = data)


@event_coordinator.route('/events/')
@login_required
@role_required("event_coordinator")
def getEventsView():
    data = getEventsAll(dept = current_user.dept)
    return render_template("events.html",data = data)

@event_coordinator.route('/event/add', methods=['GET', 'POST'])
@login_required
@role_required("event_coordinator")
def addEventView():
    form = CreateEventForm(request.form)
    if form.validate_on_submit():
        event_organiser = form.event_organiser.data
        
        if current_user.dept != event_organiser['dept']:
            flash("You can only add an event under your department!")
            return redirect(url_for('event_coordinator.addEventView'))

        organiser = addUser(event_organiser['userId'], event_organiser['name'], event_organiser['email'], "event_organiser", event_organiser['dept'], event_organiser['phone'])
        addEvent(form.title.data, current_user.dept , current_user.id, organiser.id)

        flash("Event added successfully")
        flash("Organiser added successfully")
        # flash("Check Email to reset password")
        return redirect(url_for('event_coordinator.addEventView'))

    return render_template('add_event.html', form=form)


@event_coordinator.route('/profile', methods=['GET'])
@login_required
@role_required("event_coordinator")
def getProfileView():
    return render_template('profile.html', role = "Event Coordinator", user=current_user)


@event_coordinator.route('/profile/update', methods=["GET", "POST"])
@login_required
@role_required("event_coordinator")
def updateProfileView():
    form = UpdateProfileForm(request.form)
    if form.validate_on_submit():
        try:
            updateProfile(current_user.id, form.data)
            flash("Your profile has been updated successfully!")
        except:
            flash("Something went wrong!")        
        
    return render_template('update_profile.html', role = "Event Coordinator", user=current_user, form=form)
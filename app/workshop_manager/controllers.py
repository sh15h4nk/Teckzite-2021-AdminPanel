from app.middlewares import role_required
from app import app, db, bcrypt
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import CreateWorkshopForm, LoginForm, UpdateProfileForm
from app.models import User
from app.controllers import login_manager
from app.mynav import mynav
from app.workshop_manager.functions import *
from app.functions import *
mynav.init_app(app)



from app.workshop_manager import workshop_manager


@workshop_manager.route('/')

def home():
    return render_template('workshop_manager/index.html')



@workshop_manager.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@workshop_manager.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session and session['role'] == "workshop_manager":
        flash("Already Logged In As workshop_manager")
        return redirect(url_for('workshop_manager.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "workshop_manager" and user.hidden == 0:
            	login_user(user)
            	session['id'] = user.id
            	session['role'] = user.role
            	return redirect(url_for('workshop_manager.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form = form, role = "Workshop Manager")

@workshop_manager.route('/dashboard/')
@login_required
@role_required(["workshop_manager"])
def dashboard():
    return render_template("workshop_manager/dashboard.html",current_user = current_user)

@workshop_manager.route('/workshop.manager/')
@login_required
@role_required("workshop_manager")
def getWorkshopManagersView():
    data = getWorkshopManagersAll()
    return render_template("users.html", role= "Workshop Manager",data = data)

@workshop_manager.route('/workshop.coordinator/')
@login_required
@role_required("workshop_manager")
def getWorkshopCoordinatorsView():
    data = getWorkshopCoordinatorsAll()
    return render_template("users.html", role= "Workshop Coordinator",data = data)

@workshop_manager.route('/workshops/')
@login_required
@role_required("workshop_manager")
def getWorkshopsView():
    data = getWorkshopsAll()
    return render_template("workshops.html",data =data)


@workshop_manager.route('/workshop/add', methods=['GET', 'POST'])
@login_required
@role_required("workshop_manager")
def addWorkshopView():
    form = CreateWorkshopForm(request.form)
    if form.validate_on_submit():
        # return request.form
        workshop_coordinator = form.workshop_coordinator.data
        coordinator_id = current_user.id

        workshop_coordinator = addUser(workshop_coordinator['userId'], workshop_coordinator['name'], workshop_coordinator['email'], "workshop_coordinator", workshop_coordinator['dept'], workshop_coordinator['phone'])
        addWorkshop(form.title.data, form.dept.data, coordinator_id)

        flash("Workshop Added Succesfully")
        flash("Worshop Coordinator Added Succesfully")

        return redirect(url_for('workshop_manager.addWorkshopView'))

    return render_template('add_workshop.html', form = form)



@workshop_manager.route('/profile', methods=['GET'])
@login_required
@role_required("workshop_manager")
def getProfileView():
    return render_template('profile.html', role = "Workshop Manager", user=current_user)


@workshop_manager.route('/profile/update', methods=["GET", "POST"])
@login_required
@role_required("workshop_manager")
def updateProfileView():
    form = UpdateProfileForm(request.form)
    if form.validate_on_submit():
        try:
            updateProfile(current_user.id, form.data)
            flash("Your profile has been updated successfully!")
        except: 
            flash("Something went wrong!")        
        
    return render_template('update_profile.html', role = "Workshop Manager", user=current_user, form=form)
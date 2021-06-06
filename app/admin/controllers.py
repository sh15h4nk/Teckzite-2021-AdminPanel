from flask import url_for, redirect, request, render_template, Blueprint, session, flash, escape, get_flashed_messages, Markup, jsonify, Response
from flask.ctx import after_this_request
from flask.globals import current_app
from werkzeug.utils import secure_filename
from app.models import User
from app.forms import UpdateProfileForm, CreateWorkshopForm, LoginForm, CreateEventForm, PhotoForm, RegisterForm, Contacts, FAQs, Sponsors, UpdateEventForm, UpdateWorkshopForm
from app import db, app, bcrypt, ckeditor
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import admin
from app.admin.functions import *
from app.functions import *
from app.mynav import mynav
from app.middlewares import role_required
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

    if "id" in session and session['role'] == "admin":
        flash("Already Logged In As Admin")
        return redirect(url_for('admin.dashboard'))
        

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "admin" and user.hidden == 0:
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
@role_required("admin")
def dashboard():    
    get_flashed_messages()
    rgukt_n = TechUser.query.filter_by(college = "RGUKT-N", payment_status = 1).count()
    rgukt_sklm = TechUser.query.filter_by(college = "RGUKT-SKLM", payment_status = 1).count()
    rgukt_ong = TechUser.query.filter_by(college = "RGUKT-ONG", payment_status = 1).count()
    rgukt_rkv = TechUser.query.filter_by(college = "RGUKT-RKV", payment_status = 1).count()
    other = TechUser.query.filter(and_(TechUser.college != "RGUKT-RKV", TechUser.college != "RGUKT-SKLM", TechUser.college != "RGUKT-ONG", TechUser.college != "RGUKT-N", TechUser.payment_status == 1)).count()
    tz_users = {"rguktn": rgukt_n, "rguktsklm": rgukt_sklm, "rguktong": rgukt_ong, "rguktrkv": rgukt_rkv, "other":other}


    cse = TechUser.query.filter_by(college = "RGUKT-N", branch = "CSE", payment_status = 1).count()
    ece = TechUser.query.filter_by(college = "RGUKT-N", branch = "ECE", payment_status = 1).count()
    mec = TechUser.query.filter_by(college = "RGUKT-N", branch = "MEC", payment_status = 1).count()
    civ = TechUser.query.filter_by(college = "RGUKT-N", branch = "CIV", payment_status = 1).count()
    che = TechUser.query.filter_by(college = "RGUKT-N", branch = "CHE", payment_status = 1).count()
    mme = TechUser.query.filter_by(college = "RGUKT-N", branch = "MME", payment_status = 1).count()
    puc = TechUser.query.filter_by(college = "RGUKT-N", branch = "PUC", payment_status = 1).count()
    other = TechUser.query.filter(and_(TechUser.college == "RGUKT-N", TechUser.payment_status == 1, TechUser.branch != "CSE", TechUser.branch != "ECE", TechUser.branch != "MEC", TechUser.branch != "CHE", TechUser.branch != "MME", TechUser.branch != "CIV", TechUser.branch != "PUC")).count()
    rguktn_data = {"cse": cse, "ece": ece, "mec": mec, "civ": civ, "che": che, "mme": mme, "puc": puc, "other": other}


    workshops = db.session.query(Workshop, func.count(TechUser.id), func.count(case([((TechUser.workshop_payment_status == 1), TechUser.id)]))).join(TechUser, Workshop.workshopId == TechUser.workshop_id).group_by(Workshop.title).all()


    puc1 = TechUser.query.filter( TechUser.collegeId.like("N2%"), TechUser.college == "RGUKT-N", TechUser.payment_status == 1).count()
    puc2 = TechUser.query.filter( TechUser.collegeId.like("N19%"), TechUser.college == "RGUKT-N", TechUser.payment_status == 1).count()
    e1 = TechUser.query.filter( TechUser.collegeId.like("N18%"), TechUser.college == "RGUKT-N", TechUser.payment_status == 1).count()
    e2 = TechUser.query.filter( TechUser.collegeId.like("N17%"), TechUser.college == "RGUKT-N", TechUser.payment_status == 1).count()
    e3 = TechUser.query.filter( TechUser.collegeId.like("N16%"), TechUser.college == "RGUKT-N", TechUser.payment_status == 1).count()
    e4 = TechUser.query.filter( TechUser.collegeId.like("N15%"), TechUser.college == "RGUKT-N", TechUser.payment_status == 1).count()
    rguktn_year  = {"puc1": puc1, "puc2": puc2, "e1": e1, "e2": e2, "e3": e3, "e4": e4}

    return render_template("admin/dashboard.html",current_user = current_user, tz_users = tz_users, rguktn_data = rguktn_data, workshops = workshops, rguktn_year = rguktn_year)


@admin.route('/admins/')
@login_required
@role_required("admin")
def getAdminsView():
    data = getAdminsAll()
    return render_template("users.html",role = "Admin",data = data)


@admin.route('/event.manager/')
@login_required
@role_required("admin")
def getEventManagersView():
    data = getEventManagersAll()
    return render_template("users.html", role= "Event Manager",data = data)


@admin.route('/event.coordinators/')
@login_required
@role_required("admin")
def getEventCoordinatorsView():
    data = getEventCoordinatorsAll()
    return render_template("users.html", role= "Event Coordinator",data = data)

@admin.route('/event.organiser/')
@login_required
@role_required("admin")
def getEventOrganisersView():
    data = getEventOrganisersAll()
    return render_template("users.html", role= "Event Organiser",data = data)

@admin.route('/workshop.manager/')
@login_required
@role_required("admin")
def getWorkshopManagersView():
    data = getWorkshopManagersAll()
    return render_template("users.html", role= "Workshop Manager",data = data)

@admin.route('/workshop.coordinator/')
@login_required
@role_required("admin")
def getWorkshopCoordinatorsView():
    data = getWorkshopCoordinatorsAll()
    return render_template("users.html", role= "Workshop Coordinator",data = data)

@admin.route('/events/')
@login_required
@role_required("admin")
def getEventsView():
    data = getEventsAll()
    return render_template("events.html",data = data)


@admin.route('/workshops/')
@login_required
@role_required("admin")
def getWorkshopsView():
    data = getWorkshopsAll()
    payments = TechUser.query.filter_by(workshop_payment_status = 1).count()
    return render_template("workshop_stats.html",data =data, payment = payments)




#Data Adding routes
@admin.route('/admins/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addAdminView():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, "admin", form.dept.data, form.phone.data)

        flash("You Registered a Admin Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addAdminView'))   

    return render_template('admin/register.html',role="Admin", form = form,current_user = current_user)


@admin.route('/event.manager/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addEventManagerView():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, "event_manager", form.dept.data, form.phone.data)

        flash("You Registered a Event Manager Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addEventManagerView'))   

    return render_template('admin/register.html',role="Event Manager", form = form,current_user = current_user)

@admin.route('/workshop.manager/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addWorkshopManagerView():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        addUser(form.userId.data, form.name.data, form.email.data, "workshop_manager", form.dept.data, form.phone.data)

        flash("You Registered a Workshop Manager Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addWorkshopManagerView'))   

    return render_template('admin/register.html',role="Workshop Manager", form = form,current_user = current_user)



@admin.route('/event.coordinator/add', methods=['GET', 'POST'])
@login_required
@role_required(["admin"])
def addEventCoordinator():
    form = RegisterForm(request.form)
    if form.validate_on_submit():

        user = User.query.filter_by(hidden = 0, role = "event_coordinator", dept = form.dept.data).count()
        if user:
            flash("Event Coordinator already exists for this Department")
            return render_template('admin/register.html',role="Events Coordinator", form = form,current_user = current_user)
        
        addUser(form.userId.data, form.name.data, form.email.data, "event_coordinator", form.dept.data, form.phone.data)

        flash("You Registered Event Coordinator Succesfully")
        flash("Email has been sent to reset the password")

        return redirect(url_for('admin.addEventCoordinator'))   

    return render_template('admin/register.html',role="Events Coordinator", form = form,current_user = current_user)




@admin.route('/event/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addEventView():
    form = CreateEventForm(request.form)
    if form.validate_on_submit():
        event_organiser = form.event_organiser.data
        event_coordinator = User.query.filter_by(dept=event_organiser['dept'], role="event_coordinator").first()
        if event_coordinator is None:
            flash("No coordinator for the Dept")
            return redirect(url_for('admin.addEventView'))
        
        organiser = addUser(event_organiser['userId'], event_organiser['name'], event_organiser['email'], "event_organiser", event_organiser['dept'], event_organiser['phone'])
        addEvent(form.title.data, event_coordinator.dept , event_coordinator.id, organiser.id)

        flash("Event added successfully")
        flash("Organiser added successfully")
        # flash("Check Email to reset password")
        return redirect(url_for('admin.addEventView'))

    return render_template('add_event.html', form=form)



@admin.route('/workshop/add', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def addWorkshopView():
    form = CreateWorkshopForm(request.form)
    if form.validate_on_submit():
        # return request.form
        workshop_coordinator = form.workshop_coordinator.data
        coordinator_id = current_user.id

        workshop_coordinator = addUser(workshop_coordinator['userId'], workshop_coordinator['name'], workshop_coordinator['email'], "workshop_coordinator", workshop_coordinator['dept'], workshop_coordinator['phone'])
        addWorkshop(form.title.data, form.dept.data, workshop_coordinator.id)

        flash("Workshop Added Succesfully")
        flash("Organiser Added Succesfully")

        return redirect(url_for('admin.addWorkshopView'))

    return render_template('add_workshop.html', form = form)




@login_required
@role_required("admin")
@admin.route('/hide_user', methods=['POST'])
def hideUser():
    user_id = request.form['id']
    field = request.form['field']
    value = request.form['value']
    return "got the request", user_id, field, value


@admin.route('/profile', methods=['GET'])
@login_required
@role_required("admin")
def getProfileView():
    return render_template('profile.html', role = "Admin", user=current_user)

@admin.route('/profile/update', methods=["GET", "POST"])
@login_required
@role_required("admin")
def updateProfileView():
    form = UpdateProfileForm(request.form)
    if form.validate_on_submit():
        try:
            updateProfile(current_user.id, form.data)
            flash("Your profile has been updated successfully!")
        except Exception as e:
            raise e       
        
    return render_template('update_profile.html', role = "Admin", user=current_user, form=form)

@admin.route('/CA/')
@login_required
@role_required("admin")
def getCAsView():
    data = getCAAll()
    return render_template("ca.html",role = "CA",data = data)


@admin.route('/tzuser')
@login_required
@role_required('admin')
def getTzUserView():
    data = getTzUsers()
    tz_payment = TechUser.query.filter_by(payment_status = 1).count()
    wksp_payment = TechUser.query.filter_by(workshop_payment_status = 1).count()
    return render_template("tzuser.html",role = "Tz Users", data = data, tz_payment = tz_payment, wksp_payment = wksp_payment)

@admin.route("/workshopReg/")
@login_required
@role_required("admin")
def workshopReg():
    data = getWorkshopReg()
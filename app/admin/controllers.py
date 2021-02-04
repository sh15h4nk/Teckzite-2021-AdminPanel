from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask.ctx import after_this_request
from flask.globals import current_app
from app.admin.models import User
from app.admin.forms import LoginForm, RegisterForm
from app import db
from app import app
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.admin import roles
from app.admin.mynav import nav

from app.admin.functions import getAdmins, getEvents, getWorkshops

nav.init_app(app)

admin = Blueprint('admin', __name__, url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must login ")
    return redirect(url_for('admin.login'))


@admin.route('/')
def home():
    return render_template('admin/index.html')

@admin.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('admin.home'))

@admin.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session:
        flash("Already Logged In")
        return redirect(url_for('admin.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(id=form.id.data).first()

        if user and user.password == form.password.data:
            login_user(user)
            session['id'] = form.id.data
            session['role'] = user.role
            flash("Login successful")
            return redirect(url_for("admin.dashboard"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("admin/login.html",form= form)
    
        


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


@admin.route('/admindata/<role>')
@login_required
def retriveAdminRows(role):
    if current_user.role != 1: 
        if current_user.role < role:
            return "403"
    data = getAdmins(int(role))
    return data
    

@admin.route('/eventsdata')
@login_required
def retriveEvents():
    data = getEvents()
    return data

@admin.route('/eventsdata')
@login_required
def retriveWorkshops():
    data = getWorkshops()
    return data
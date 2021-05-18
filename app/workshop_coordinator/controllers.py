from app.middlewares import role_required
from app import app, db, bcrypt
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import LoginForm
from app.models import User
from app.controllers import login_manager
from app.mynav import mynav
mynav.init_app(app)



from app.workshop_coordinator import workshop_coordinator



@workshop_coordinator.route('/')

def home():
    return render_template('workshop_coordinator/index.html')



@workshop_coordinator.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@workshop_coordinator.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session and session['role'] == "workshop_coordinator":
        flash("Already Logged In As Coordinator")
        return redirect(url_for('workshop_coordinator.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.userId.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.role == "workshop_coordinator" and user.hidden == 0:
            	login_user(user)
            	session['id'] = user.id
            	session['role'] = user.role
            	return redirect(url_for('workshop_coordinator.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form = form, role = "Workshop Coordinator")

@workshop_coordinator.route('/dashboard/')
@login_required
@role_required(['workshop_coordinator'])
def dashboard():
    return render_template("workshop_coordinator/dashboard.html",current_user = current_user)





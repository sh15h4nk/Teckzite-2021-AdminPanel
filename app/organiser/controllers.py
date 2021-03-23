from app import app, db
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import LoginForm
from app.models import User
from app.controllers import login_manager


from app.organiser import organiser
from app.middlewares import organiser_authenticated



@organiser.route('/')
def home():
    return render_template('organiser/index.html')



@organiser.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('role', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@organiser.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session and session['role'] == 3:
        flash("Already Logged In As Organiser")
        return redirect(url_for('organiser.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(userId=form.id.data).first()

        if user and user.password == form.password.data:
            if user.role == 3 and user.hidden == 0:
            	login_user(user)
            	session['id'] = user.id
            	session['role'] = user.role
            	return redirect(url_for('organiser.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form)
 

@organiser.route('/dashboard/')
@login_required
@organiser_authenticated
def dashboard():
    return render_template("organiser/dashboard.html",current_user = current_user)

from app import app, db
from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from app.forms import LoginForm
from app.models import User
from app.controllers import login_manager
from app.mynav import mynav
mynav.init_app(app)



from app.coordinate import coordinate




@coordinate.route('/')
def home():
    return render_template('coordinate/index.html')



@coordinate.route("/logout/")
def logout():
    logout_user()
    session.pop('id', None)
    session.pop('_flashes', None)
    flash("You have been logged out")
    return redirect(url_for('index'))

@coordinate.route('/login/', methods=['GET', 'POST'])
def login():

    if "id" in session:
    	if session['role'] == 2:
	        flash("Already Logged In")
	        return redirect(url_for('coordinate.dashboard'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(id=form.id.data).first()

        if user and user.password == form.password.data:
            if user.role == 2:
            	login_user(user)
            	session['id'] = form.id.data
            	session['role'] = user.role
            	flash("Login Sucessfull")
            	return redirect(url_for('coordinate.dashboard'))
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("login.html",form= form)
 
@coordinate.route('/dashboard/')
@login_required
def dashboard():
    return render_template("coordinate/dashboard.html",current_user = current_user)





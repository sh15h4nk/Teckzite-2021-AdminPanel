from operator import imatmul
from flask import url_for, redirect, request, render_template, Blueprint, session, flash, Response
from flask_login import LoginManager, login_required, current_user
from flask_migrate import current
from sqlalchemy.sql.sqltypes import Date
from werkzeug.utils import secure_filename
from app import app, db
from app.models import User, Event
from app.forms import ChangePassword, ResetRequest
from app.functions import sendMail
import os
# from PIL import Image

response = Response()
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


login_manager = LoginManager(app)

login_manager.login_view = 'index'



@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must login ")
    return redirect(url_for('index'))




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset_password/<token>', methods=['GET','POST'])
def resetPassword(token):
	user = User.verify_token(token)
	if user is None:
		flash('That is an invalid or expired token','warning')
		return redirect(url_for('resetRequest'))
	form = ChangePassword()
	if form.validate_on_submit():
		user.password = form.password.data
		db.session.commit()

		flash("Password Updated Successfully")
		return redirect(url_for('index'))

	return render_template('change_password.html',Title="Change Password",form=form)

@app.route('/reset_request/', methods=['GET','POST'])
def resetRequest():
	form = ResetRequest()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		sendMail(user)
		flash("Check your mail",'info')
		return redirect(url_for('index'))
	return render_template('change_password.html',Title="Reset Password",form = form)
	
@login_required
@app.route('/hideUser', methods=['POST'])
def hideUserView():

	if current_user.role == 1:
		user = User.query.filter_by(id=request.form['id']).first()
		if user:
			if request.form['value'] == 'hide':
				user.hidden = 1
				return "Success"
			elif request.form['value'] == 'unhide':
				user.hidden = 0
				return "Success"
			else:
				return "Invalid operation"
		
		else:
			return "Failed"
		
		
	elif current_user.role == 2:
		user = User.query.filter_by(id=request.form['id'], role=3).first()
		if user:
			if request.form['value'] == 'hide':
				user.hidden = 1
				return "Success"
			elif request.form['value'] == 'unhide':
				user.hidden = 0
				return "Success"
			else:
				return "Invalid operation"
		
		else:
			return "Failed"

	else:
		return "Unauthorised"


@login_required
@app.route('/uploadImage', methods=['POST'])
def uploadImageView():
	
		
	file = request.files
	return "Success"



@login_required
@app.route('/hideEvent', methods=['POST'])
def hideEventView():

	if current_user.role == 1:
		event = Event.query.filter_by(id=request.form['id']).first()
		if event:
			if request.form['value'] == 'hide':
				event.hidden = 1
				return "Success"
			elif request.form['value'] == 'unhide':
				event.hidden = 0
				return "Success"
			else:
				return "Invalid operation"
		
		else:
			return "Failed"
		
		
	elif current_user.role == 2:
		event = Event.query.filter_by(id=request.form['id'], dept=current_user.dept).first()
		if event:
			if request.form['value'] == 'hide':
				event.hidden = 1
				return "Success"
			elif request.form['value'] == 'unhide':
				event.hidden = 0
				return "Success"
			else:
				return "Invalid operation"
		
		else:
			return "Failed"

	else:
		return "Unauthorised"

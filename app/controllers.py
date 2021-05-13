from operator import imatmul
from types import WrapperDescriptorType
from flask import url_for, redirect, request, render_template, Blueprint, session, flash, Response
from flask.wrappers import Request
from flask_login import LoginManager, login_required, current_user
from flask_migrate import current
from sqlalchemy.sql.sqltypes import Date
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from app.models import User, Event, Workshop
from app.forms import ChangePassword, CreateEventForm, ResetRequest, UpdateEventForm, UpdateWorkshopForm
from app.functions import sendMail, updateEvent, updateWorkshop
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
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user.password = hashed_password
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
	

@app.route('/hideUser', methods=['POST'])
@login_required
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




@app.route('/uploadImage', methods=['POST'])
@login_required
def uploadImageView():
	
		
	file = request.files
	return "Success"



@app.route('/hideEvent', methods=['POST'])
@login_required
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


@app.route('/hideWorkshop', methods=['POST'])
@login_required
def hideWorkshopView():

	if current_user.role == 1:
		workshop = Workshop.query.filter_by(id=request.form['id']).first()
		if workshop:
			if request.form['value'] == 'hide':
				workshop.hidden = 1
				return "Success"
			elif request.form['value'] == 'unhide':
				workshop.hidden = 0
				return "Success"
			else:
				return "Invalid operation"
		
		else:
			return "Failed"
		
		
	elif current_user.role == 2:
		workshop = Event.query.filter_by(id=request.form['id'], dept=current_user.dept).first()
		if workshop:
			if request.form['value'] == 'hide':
				workshop.hidden = 1
				return "Success"
			elif request.form['value'] == 'unhide':
				workshop.hidden = 0
				return "Success"
			else:
				return "Invalid operation"
		
		else:
			return "Failed"

	else:
		return "Unauthorised"



@app.route('/event/update', methods=['GET','POST'])
@login_required
def updateEventView():
	form = UpdateEventForm(request.form)

	if form.validate_on_submit():
		status = updateEvent(form.data)
		if status:
			return redirect(url_for('admin.getEventsView'))
		

	eventId = request.args.get('id')
	event = Event.query.filter_by(id = int(eventId)).first()
	return render_template('update_event.html', form=form, event=event)

@app.route('/workshop/update', methods=['GET','POST'])
@login_required
def updateWorkshopView():
	form = UpdateWorkshopForm(request.form)

	if form.validate_on_submit():
		status = updateWorkshop(form.data)		
		if status:
			return redirect(url_for('admin.getWorkshopsView'))
		
	workshopId = request.args.get('id')
	workshop = Workshop.query.filter_by(id = int(workshopId)).first()
	return render_template('update_workshop.html', form=form, workshop=workshop)


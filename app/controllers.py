from operator import imatmul
from types import WrapperDescriptorType
from flask import url_for, redirect, request, render_template, Blueprint, session, flash, Response
from flask.wrappers import Request
from flask_login import LoginManager, login_required, current_user
from flask_migrate import current
from sqlalchemy.sql.sqltypes import Date
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from app.models import User, Event, Workshop, Contact, FAQ, Sponsor
from app.forms import ChangePassword, CreateEventForm, ResetRequest, UpdateEventForm, UpdateWorkshopForm
from app.functions import *
from app.middlewares import role_required
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
	if current_user.role == "admin":
		user = User.query.filter_by(id=request.form['id']).first()
		if user:
			if request.form['value'] == 'hide':
				user.hidden = 1
				db.session.commit()
				return Response(status = 200)
			elif request.form['value'] == 'unhide':
				user.hidden = 0
				db.session.commit()
				return Response(status = 200)
			else:
				return "Invalid operation"
		else:
			return "Failed"
	elif current_user.role == "event_manager":
		# user = User.query.filter_by(id=request.form['id'], role="event_organiser").first()
		user = User.query.filter(User.id == request.form['id'], or_(User.role == "event_organiser", User.role == "event_coordinator")).first()
		if user:
			if request.form['value'] == 'hide':
				user.hidden = 1
				db.session.commit()
				return Response(status = 200)
			elif request.form['value'] == 'unhide':
				user.hidden = 0
				db.session.commit()
				return Response(status = 200)
			else:
				return Response(status = 400)
		else:
			return Response(status = 400)
	elif current_user.role == "event_coordinator":
		user = User.query.filter_by(id=request.form['id'], role="event_organiser").first()
		if user:
			if request.form['value'] == 'hide':
				user.hidden = 1
				db.session.commit()
				return Response(status = 200)
			elif request.form['value'] == 'unhide':
				user.hidden = 0
				db.session.commit()
				return Response(status = 200)
			else:
				return Response(status = 400)
		else:
			return Response(status = 400)

	elif current_user.role == "workshop_manager":
		user = User.query.filter_by(id=request.form['id'], role="workshop_coordinator").first()
		if user:
			if request.form['value'] == 'hide':
				user.hidden = 1
				db.session.commit()
				return Response(status = 200)
			elif request.form['value'] == 'unhide':
				user.hidden = 0
				db.session.commit()
				return Response(status = 200)
			else:
				return Response(status = 400)
		else:
			return Response(status = 400)
	else:
		return Response(status = 403)

@app.route('/uploadImage', methods=['POST'])
@login_required
def uploadImageView():
	
		
	file = request.files
	return "Success"



@app.route('/hideEvent', methods=['POST'])
@login_required
def hideEventView():
	# print(request.form)
	if current_user.role in ["admin", "event_manager"]:
		event = Event.query.filter_by(eventId=request.form['id']).first()
		if event:
			if request.form['value'] == 'hide':
				event.hidden = 1
				db.session.commit()
				return Response(status = 200)
			elif request.form['value'] == 'unhide':
				event.hidden = 0
				db.session.commit()
				return Response(status = 200)
			else:
				return Response(status = 400)
		
		else:
			return Response(status = 403)
		
	elif current_user.role == "event_coordinator":
		event = Event.query.filter_by(eventId=request.form['id'], dept=current_user.dept).first()
		if event:
			if request.form['value'] == 'hide':
				event.hidden = 1
				db.session.commit()
				return Response(status = 200)
			elif request.form['value'] == 'unhide':
				event.hidden = 0
				db.session.commit()
				return Response(status = 200)
			else:
				return Response(status = 400)
		
		else:
			return Response(status = 400)

	else:
		return Response(status = 403)


@app.route('/hideWorkshop', methods=['POST'])
@login_required
@role_required(["admin", "workshop_manager"])
def hideWorkshopView():
	workshop = Workshop.query.filter_by(workshopId=request.form['id']).first()
	if workshop:
		if request.form['value'] == 'hide':
			workshop.hidden = 1
			db.session.commit()
			return Response(status = 200)
		elif request.form['value'] == 'unhide':
			workshop.hidden = 0
			db.session.commit()
			return Response(status = 200)
		else:
			return Response(status = 400)
	else:
		return Response(status = 400)


@app.route('/hideContact', methods=['POST'])
@login_required
def hideContactView():
	if not request.form['id'] or not request.form['value'] or not request.form['workshop_id']:
		return Response(status=400)
	contact = Contact.query.filter_by(id=request.form['id']).first()
	if contact:
		if request.form['value'] == 'hide':
			if Contact.query.filter_by(hidden = 0, workshop_id = request.form['workshop_id']).count() >= 2:
				contact.hidden = 1
				db.session.commit()
				return Response(status=200)
			else:
				return Response(status=400)
		elif request.form['value'] == 'unhide':
			contact.hidden = 0
			db.session.commit()
			return Response(status=200)
		else:
			return Response(status=400)
	else:
		return Response(status=400)

@app.route('/hideFaq', methods=['POST'])
@login_required
def hideFaqView():
	if not request.form['id'] or not request.form['value'] or not request.form['workshop_id']:
		return Response(status=400)
	faq = FAQ.query.filter_by(id=request.form['id']).first()
	if faq:
		if request.form['value'] == 'hide':
			faq.hidden = 1
			db.session.commit()
			return Response(status=200)
		elif request.form['value'] == 'unhide':
			faq.hidden = 0
			db.session.commit()
			return Response(status=200)
		else:
			return Response(status=400)
	else:
		return Response(status=400)			

@app.route('/hideSponsor', methods=['POST'])
@login_required
def hideSponsorView():
	if not request.form['id'] or not request.form['value'] or not request.form['workshop_id']:
		return Response(status=400)
	sponsor = Sponsor.query.filter_by(id=request.form['id']).first()
	if sponsor:
		if request.form['value'] == 'hide':
			sponsor.hidden = 1
			db.session.commit()
			return Response(status=200)
		elif request.form['value'] == 'unhide':
			sponsor.hidden = 0
			db.session.commit()
			return Response(status=200)
		else:
			return Response(status=400)
	else:
		return Response(status=400)

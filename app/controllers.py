from flask import url_for, redirect, request, render_template, Blueprint, session, flash, Response
from flask.wrappers import Request
from flask_login import LoginManager, login_required, current_user
from flask_migrate import current
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Date
from werkzeug.utils import secure_filename
from app import app, db, bcrypt
from app.models import *
from app.forms import ChangePassword, CreateEventForm, ResetRequest, UpdateEventForm, UpdateWorkshopForm
from app.functions import *
from app.middlewares import role_required
from app.forms import *
import os
from sqlalchemy import func
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
			if user.userId in ['N170295', 'N170076']:
				return Response(status=403)
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
				return Response(status = 406)
		else:
			return Response(status = 406)
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
				return Response(status = 406)
		else:
			return Response(status = 406)

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
				return Response(status = 406)
		else:
			return Response(status = 406)
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
				return Response(status = 406)
		
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
				return Response(status = 406)
		
		else:
			return Response(status = 406)

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
			return Response(status = 406)
	else:
		return Response(status = 406)


@app.route('/hideContact', methods=['POST'])
@login_required
def hideContactView():
	print(request.form)
	if not request.form['id'] or not request.form['value'] or not request.form['program_id']:
		return Response(status=406)

	program_id = request.form['program_id']
	#ACCESS CONTROL
	if not current_user.role == "admin":
		if program_id.startswith("EV") and current_user.role in ["event_manager", "event_coordinator", "event_organiser"]:
			if current_user.role == "event_coordinator" and not Event.query.filter_by(eventId = program_id, dept = current_user.dept).first():
				return Response(status = 406)
			elif current_user.role == "event_organiser" and not Event.query.filter_by(eventId = program_id, organiser_id = current_user.id).first():
				return Response(status = 406)
		elif program_id.startswith("WS") and current_user.role in ["workshop_manager", "workshop_coordinator"]:
			if current_user.role == "workshop_coordinator" and not Workshop.query.filter_by(workshopId = program_id, coordinator_id = current_user.id).first():
				return Response(status = 406)
		else:
			return Response(status = 403)

	contact = Contact.query.filter_by(id=request.form['id']).first()
	if contact:
		if request.form['value'] == 'hide':
			if program_id.startswith("EV") and Contact.query.filter_by(hidden = 0, event_id = program_id).count() >= 2:
				contact.hidden = 1
				db.session.commit()
				return Response(status=200)
			
			elif program_id.startswith("WS") and Contact.query.filter_by(hidden = 0, workshop_id = program_id.count() >= 2):
				contact.hidden = 1
				db.session.commit()
				return Response(status=200)

			else:
				return Response(status=406)

		elif request.form['value'] == 'unhide':
			if program_id.startswith("EV") and Contact.query.filter_by(hidden = 0, event_id = program_id).count() < 3:
				contact.hidden = 0
				db.session.commit()
				return Response(status=200)

			elif program_id.startswith("WS") and Contact.query.filter_by(hidden = 0, workshop_id = program_id.count() < 3):
				contact.hidden = 0
				db.session.commit()
				return Response(status=200)

			else:
				return Response(status=406)

		else:
			return Response(status=406)
	else:
		return Response(status=406)

@app.route('/hideFaq', methods=['POST'])
@login_required
def hideFaqView():
	if not request.form['id'] or not request.form['value'] or not request.form['program_id']:
		return Response(status=406)

	program_id = request.form['program_id']
	#ACCESS CONTROL
	if not current_user.role == "admin":
		if program_id.startswith("EV") and current_user.role in ["event_manager", "event_coordinator", "event_organiser"]:
			if current_user.role == "event_coordinator" and not Event.query.filter_by(eventId = program_id, dept = current_user.dept).first():
				return Response(status = 406)
			elif current_user.role == "event_organiser" and not Event.query.filter_by(eventId = program_id, organiser_id = current_user.id).first():
				return Response(status = 406)
		elif program_id.startswith("WS") and current_user.role in ["workshop_manager", "workshop_coordinator"]:
			if current_user.role == "workshop_coordinator" and not Workshop.query.filter_by(workshopId = program_id, coordinator_id = current_user.id).first():
				return Response(status = 406)
		else:
			return Response(status = 403)

	faq = FAQ.query.filter_by(id=request.form['id']).first()
	if faq:

		if request.form['value'] == 'hide':
			if program_id.startswith("EV") and FAQ.query.filter_by(hidden = 0, event_id = program_id).count() >= 2:
				faq.hidden = 1
				db.session.commit()
				return Response(status=200)
			
			elif program_id.startswith("WS") and FAQ.query.filter_by(hidden = 0, workshop_id = program_id.count() >= 2):
				faq.hidden = 1
				db.session.commit()
				return Response(status=200)

			else:
				return Response(status=406)

		elif request.form['value'] == 'unhide':
			faq.hidden = 0
			db.session.commit()
			return Response(status=200)
		else:
			return Response(status=406)
	else:
		return Response(status=406)			

@app.route('/hideSponsor', methods=['POST'])
@login_required
def hideSponsorView():
	print(request.form)
	if not request.form['id'] or not request.form['value'] or not request.form['program_id']:
		return Response(status=406)

	program_id = request.form["program_id"]
	#ACCESS CONTROL
	if not current_user.role == "admin":
		if program_id.startswith("EV") and current_user.role in ["event_manager", "event_coordinator", "event_organiser"]:
			if current_user.role == "event_coordinator" and not Event.query.filter_by(eventId = program_id, dept = current_user.dept).first():
				return Response(status = 406)
			elif current_user.role == "event_organiser" and not Event.query.filter_by(eventId = program_id, organiser_id = current_user.id).first():
				return Response(status = 406)
		elif program_id.startswith("WS") and current_user.role in ["workshop_manager", "workshop_coordinator"]:
			if current_user.role == "workshop_coordinator" and not Workshop.query.filter_by(workshopId = program_id, coordinator_id = current_user.id).first():
				return Response(status = 406)
		else:
			return Response(status = 403)

	sponsor = Sponsor.query.filter_by(id=request.form['id']).first()
	if sponsor:
		if request.form['value'] == 'hide':
			if program_id.startswith("EV") and Sponsor.query.filter_by(hidden = 0, event_id = program_id).count() >= 2:
				sponsor.hidden = 1
				db.session.commit()
				return Response(status=200)
			
			elif program_id.startswith("WS") and Sponsor.query.filter_by(hidden = 0, workshop_id = program_id.count() >= 2):
				sponsor.hidden = 1
				db.session.commit()
				return Response(status=200)

			else:
				return Response(status=406)

		elif request.form['value'] == 'unhide':
			if program_id.startswith("EV") and Sponsor.query.filter_by(hidden = 0, event_id = program_id).count() < 3:
				sponsor.hidden = 0
				db.session.commit()
				return Response(status=200)

			elif program_id.startswith("WS") and Sponsor.query.filter_by(hidden = 0, workshop_id = program_id).count() < 3:
				sponsor.hidden = 0
				db.session.commit()
				return Response(status=200)
			else:
				return Response(status = 406)
		else:
			return Response(status=406)
	else:
		return Response(status=406)


@app.route('/stopReg', methods=['POST'])
def stop_registration():
	try:
		eventId = request.form['id'].split('-')[0]
	except:
		return Response(status = 406)
	event = Event.query.filter_by(eventId=eventId).first()
	if event:
		if request.form['value'] == 'stop':
			event.stop_reg = 1
			db.session.commit()
			return Response(status = 200)
		elif request.form['value'] == 'open':
			event.stop_reg = 0
			db.session.commit()
			return Response(status = 200)
		else:
			return Response(status = 406)
	else:
		return Response(status = 406)


@app.route('/togglePayment', methods=['POST'])
@login_required
@role_required(["admin"])
def togglePaymentView():
	try:
		userId, payment_type = request.form['id'].split('-')
	except:
		return Response(status = 406)

	user = TechUser.query.filter_by(userId=userId).first()
	if user:
		if request.form['value'] == 'pay':
			if payment_type == 'teckzite':
				user.payment_status = 1
			else:
				user.workshop_payment_status = 1
			db.session.commit()
			return Response(status = 200)
		elif request.form['value'] == 'unpay':
			if payment_type == 'teckzite':
				user.payment_status = 0
			else:
				user.workshop_payment_status = 0
			db.session.commit()
			return Response(status = 200)
		else:
			return Response(status = 406)
	else:
		return Response(status = 406)



@app.route('/addData', methods=["POST"])
@login_required
def addDataView():
    try:
        program_id = request.form['programId']
    except:
        return Response(status = 406)

    program_id = request.form['programId']

    if program_id.startswith("EV"):
        contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.event_id == program_id)).count()
        faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.event_id == program_id)).count()
        sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.event_id == program_id)).count()
        # program = Event.query.filter_by(eventId= program_id).first()

    elif program_id.startswith("WS"):
        contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.workshop_id == program_id)).count()
        faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.workshop_id == program_id)).count()
        sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.workshop_id == program_id)).count()
        # program = Workshop.query.filter_by(workshopId = program_id).first()
    else:
        return Response(status = 406)

    if not program_id:
        return Response(status = 406)

    #ACCESS CONTROL
    if not current_user.role == 'admin':

    	if current_user.role in ['event_manager', 'workshop_manager']:
    		if program_id.startswith("EV") and current_user.role == "workshop_manager":
    			return Response(status=406)
    		elif program_id.startswith("WS") and current_user.role == 'event_manager':
    			return Response(status=406)

    	elif current_user.role in ['event_coordinator', 'workshop_coordinator']:
    		if program_id.startswith("EV") and current_user.role == "workshop_coordinator":
    			return Response(status=406)
    		elif program_id.startswith("WS") and current_user.role == "event_coordinator":
    			return Response(status=406)
    		else:
    			if program_id.startswith("EV") and not Event.query.filter_by(eventId = program_id, coordinator_id = current_user.id).first():
    				return Response(status=406)
    			elif program_id.startswith("WS") and not Workshop.query.filter_by(workshopId = program_id, coordinator_id = current_user.id).first():
    				return Response(status=406)
    	elif current_user.role == "event_organiser":
    		if program_id.startswith("EV") and not Event.query.filter_by(eventId = program_id, organiser_id = current_user.id).first():
    			return Response(status=406)

    # contacts = Contact.query.filter(and_(Contact.hidden == 0, or_(Contact.workshop_id == program.workshopId, Contact.event_id == program.eventId))).count()
    # faqs = FAQ.query.filter(and_(FAQ.hidden == 0, or_(FAQ.workshop_id == program.workshopId, FAQ.event_id == program.eventId))).count()
    # sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, or_(Sponsor.workshop_id == program.workshopId, Sponsor.event_id == program.eventId))).count()
    # print("#########################", contacts)

    #for FORMS
    if request.form.get("add-faq-form"):
        form = FAQs()
        return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
    
    elif request.form.get("add-contact-form"):
        form = Contacts()
        return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

    elif request.form.get('add-sponsor-form'):
        form = Sponsors()
        return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)


    #TO ADD the data
    elif request.form.get("add-contact"):
        form = Contacts()
        if form.validate_on_submit():
            contact = addContact(request.form['name'], request.form['email'], request.form['phone'], program_id)
            if type(contact) == str:
                if contact == "Overflow":
                    flash("Contacts Limit Exceeded!")
                    return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
                flash(contact)
                return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
            flash("Contact  Added!")
        return render_template('add_contacts.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

    elif request.form.get("add-faq"):
        form = FAQs()
        if form.validate_on_submit():
            faq = addFaq(form.question.data, form.answer.data, program_id)
            if type(faq) == str:
                if faq == "Overflow":
                    flash("Faqs Limit Exceeded!")
                    return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
                flash(faq)
                return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
            flash("FAQ Added!")
        return render_template('add_faqs.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

    elif request.form.get("add-sponsor"):
        form = Sponsors()
        if form.validate_on_submit():
            # return request.form

            # adding image
            #update image            
            crop = {}
            base64image = form.photo.image.data

            image_url = ""
            if base64image:    
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
                image_url = crop_image(form.photo.image.data, crop)     
            else: 
                flash("Please upload an image")
                return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
        
            sponsor = addSponsor(form.name.data, form.url.data, program_id, image_url)
            if type(sponsor) == str:
                if sponsor == "Overflow":
                    flash("Sponsors Limit Exceeded!")
                    return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
                flash(sponsor)
                return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)
            flash("Sponsor Added!")
        return render_template('add_sponsors.html', form = form, program_id = program_id, contacts = contacts, faqs = faqs, sponsors = sponsors)

        
@app.route('/updateData', methods = ['POST'])
@login_required
def updateDataView():
    # return request.form
    try:
        program_id = request.form['programId']
    except:
        return "No programId"
        return Response(status = 406)

    program_id = request.form['programId']


    if program_id.startswith("EV"):
        # contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.event_id == program_id)).count()
        # faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.event_id == program_id)).count()
        # sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.event_id == program_id)).count()
        program = Event.query.filter_by(eventId= program_id).first()

    elif program_id.startswith("WS"):
        # contacts = Contact.query.filter(and_(Contact.hidden == 0, Contact.event_id == program_id)).count()
        # faqs = FAQ.query.filter(and_(FAQ.hidden == 0, FAQ.event_id == program_id)).count()
        # sponsors = Sponsor.query.filter(and_(Sponsor.hidden == 0, Sponsor.event_id == program_id)).count()
        program = Workshop.query.filter_by(workshopId= program_id).first()

    else:
        return Response(status = 406)

    if not program:
        return Response(status = 406)

    #ACCESS CONTROL
    if not current_user.role == 'admin':

    	if current_user.role in ['event_manager', 'workshop_manager']:
    		if program_id.startswith("EV") and current_user.role == "workshop_manager":
    			return Response(status=406)
    		elif program_id.startswith("WS") and current_user.role == 'event_manager':
    			return Response(status=406)

    	elif current_user.role in ['event_coordinator', 'workshop_coordinator']:
    		if program_id.startswith("EV") and current_user.role == "workshop_coordinator":
    			return Response(status=406)
    		elif program_id.startswith("WS") and current_user.role == "event_coordinator":
    			return Response(status=406)
    		else:
    			if program_id.startswith("EV") and not Event.query.filter_by(eventId = program_id, coordinator_id = current_user.id).first():
    				return Response(status=406)
    			elif program_id.startswith("WS") and not Workshop.query.filter_by(workshopId = program_id, coordinator_id = current_user.id).first():
    				return Response(status=406)
    	elif current_user.role == "event_organiser":
    		if program_id.startswith("EV") and not Event.query.filter_by(eventId = program_id, organiser_id = current_user.id).first():
    			return Response(status=406)

    # return "caught"
    if request.form.get('update-contacts-form'):
        form = Contacts()
        return render_template('update_contacts.html',form = form, contacts = program.contacts, program_id = program_id)

    elif request.form.get('update-faqs-form'):
        form = FAQs()
        return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

    elif request.form.get('update-sponsors-form'):
        form = Sponsors()
        return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)

    elif request.form.get("update-contact"):
        form = Contacts()
        if form.validate_on_submit():
            # return request.form
            # updated
            contact_id = dict(request.form).get('update-contact')
            contact = updateContact(form.data, contact_id, program_id)
            if type(contact) == str:
                flash(contact)
                return render_template('update_contacts.html', form = form, contacts = program.contacts, program_id = program_id)

            flash("Contact Updated Succesfully!")
        return render_template('update_contacts.html', form = form, contacts = program.contacts, program_id = program_id)

    elif request.form.get("update-faq"):
        form = FAQs()
        if form.validate_on_submit():

            faq_id = dict(request.form).get('update-faq')
            faq = updateFaq(form.data, faq_id, program_id)
            if type(faq) == str:
                flash(faq)
                return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

            flash("FAQ Updated Succesfully!")
        return render_template('update_faqs.html',form = form, faqs = program.faqs, program_id = program_id)

    elif request.form.get('update-sponsor'):
        form = Sponsors()
        if form.validate_on_submit():

            sponsor_id = dict(request.form).get('update-sponsor')
            #update image
            crop = {}
            image_url = ""
            base64image = form.photo.image.data

            if base64image:
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
            
                image_url = crop_image(form.photo.image.data, crop)

            sponsor = updateSponsor(form.data, sponsor_id, program_id, image_url)
            if type(sponsor) == str:
                flash(sponsor)
                return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)
            flash("Sponsors Updated Succesfully!")
        return render_template('update_sponsors.html',form = form, sponsors = program.sponsors, program_id = program_id)
    return "caught"



@app.route('/event/update', methods= ['POST'])
@login_required
def updateEventView():
    form = UpdateEventForm(request.form)
    if request.method == 'POST':

        event_id = request.form['event_id']
        event = Event.query.filter_by(eventId = event_id).first()
        # print("fucking eve#####", event.eventId)
        if not event:
            return "Invalid Event"

        #ACCESS CONTROL
        if not current_user.role in ['admin', 'event_manager']:
        	if current_user.role in ['workshop_manager', 'workshop_coordinator']:
        		return Response(status=406)
        	elif current_user.role == 'event_coordinator' and not event.coordinator_id == current_user.id:
        		return Response(status=406)
        	elif current_user.role == 'event_organiser' and not event.organiser_id == current_user.id:
        		return Response(status=406)
		

        if not event.image_url:
            event.image_url = "http://tzimageupload.s3.amazonaws.com/back.jpg"

        markup = dict_markup({
            "status": event.status,
            "description": event.description,
            "brief": event.brief,
            "timeline": event.timeline,
            "structure": event.structure,
            "rules": event.rules,
            })

        if request.form.get('update-button'):                        
            return render_template('update_event.html', form = form, event = event, markup = markup, role = current_user.role)

        if form.validate_on_submit():
            # return request.form
            event_id = dict(request.form).get('update-event')
            data = form.data
            if current_user.role not in ['admin', 'event_manager']:
            	del data['priority']

            #update image            
            crop = {}
            base64image = form.photo.image.data		

            image_url = ""
            if base64image:    
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
                image_url = crop_image(form.photo.image.data, crop)     

		

            markup = updateEvent(data, event_id, image_url)

            flash(markup[2])
            return render_template('update_event.html', form = form, event = markup[0], markup = markup[1],role = current_user.role)

    # return form.errors
    return render_template('update_event.html', form = form, event = event, markup = markup, role = current_user.role)





@app.route('/workshop/update', methods=['POST'])
@login_required
def updateWorkshopView():
    form = UpdateWorkshopForm(request.form)
    if request.method == 'POST':

        workshop_id = request.form['workshop_id']
        workshop = Workshop.query.filter_by(workshopId = workshop_id).first()
        if not workshop:
            return "Invalid Workshop"

        #ACCESS CONTROL
        if not current_user.role in ['admin', 'workshop_manager']:
        	if current_user.role in ['event_manager', 'event_coordinator', 'event_organiser']:
        		return Response(status=406)
        	elif current_user.role == 'workshop_coordinator' and not workshop.coordinator_id == current_user.id:
        		return Response(status=406)

        if not workshop.image_url:
            workshop.image_url = "http://tzimageupload.s3.amazonaws.com/back.jpg"

        markup = dict_markup({
            "status": workshop.status,
            "description": workshop.description,
            "about": workshop.about,
            "timeline": workshop.timeline,
            "resources": workshop.resources,
            })

        if request.form.get('update-button'):                        
            return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup, role = current_user.role)

        if form.validate_on_submit():
            # return request.form
            workshop_id = dict(request.form).get('update-workshop')

            data = form.data
            if current_user.role not in ['admin', 'workshop_manager']:
            	del data['priority']

            #update image            
            crop = {}
            base64image = form.photo.image.data

            file_url = ""
            pdf = request.files['pdf']
            if pdf:
            	filename = uuid.uuid4()
            	file_url = upload_file_to_s3(pdf, filename, 'pdf')

            image_url = ""
            if base64image:    
                crop['x'] = int(float(str(form.photo.cropX.data)))
                crop['y'] = int(float(str(form.photo.cropY.data)))
                crop['width'] = int(float(str(form.photo.cropWidth.data)))
                crop['height'] = int(float(str(form.photo.cropHeight.data)))
                
                image_url = crop_image(form.photo.image.data, crop)     
           

            markup = updateWorkshop(data, workshop_id, image_url, file_url)

            flash(markup[2])
            return render_template('update_workshop.html', form = form, workshop = markup[0], markup = markup[1], role = current_user.role)

    return render_template('update_workshop.html', form = form, workshop = workshop, markup = markup, role = current_user.role)


@app.route("/teams", methods = ["POST"])
@login_required
def eventTeamsView():
	if request.method == "POST":
		try:
			event_id = request.form["event_id"]
		except Exception as e:
			raise e
			flash("No event ID")
			return Response(status = 406)
		event = Event.query.filter_by(eventId = request.form["event_id"]).first()
		accepted_count = Team.query.filter_by(event_id=event.id, team_status=1).count()
		awaited_count = Team.query.filter_by(event_id=event.id, team_status=0).count()

		return render_template("teams.html", data = event.teams, event = event, accepted_count=accepted_count,awaited_count=awaited_count)

@app.route("/deleteTeam", methods = ["POST"])
@login_required
def deleteTeamView():
	try:
		teamId = request.form['teamId']
	except Exception as e:
		raise e
		return Response(status = 406)

	team = Team.query.filter_by(teamId = teamId).first()
	if not team:
		return Response(status = 406)

	#ACCESS CONTROL
	if current_user.role not in ["admin", "event_manager"]:
		if current_user.role in ["workshop_manager", "workshop_coordinator"]:
			return Response(status = 400)
		elif current_user.role == "event_organiser" and not team in Event.query.filter_by(organiser_id = current_user.id).first().teams:
			return Response(status = 406)

	if not delete_team(team.teamId):
		return Response(status = 400)
	return Response(status = 200)

@app.route("/wkspReg", methods = ['POST'])
@login_required
def wkspRegView():
	try:
		wkspId = request.form['workshop_id']
	except Exception as e:
		raise e
		flash("No wksp id")
		return Response(status = 406)
	users = TechUser.query.filter_by(workshop_id = request.form['workshop_id'], workshop_payment_status = 1).all()
	return render_template("wksp_reg.html", users = users)


@app.route('/notAddedwksp',  methods=['GET'])
@login_required
def notAddedwkspView():
	users = TechUser.query.filter(TechUser.workshop_payment_status == 1, TechUser.workshop_id.is_(None)).all()
	return render_template('not_added_wksp.html', users=users)


@app.route("/contacts/<eventId>", methods = ["GET"])
@login_required
def contactsView(eventId):
	if request.method == "GET":
		print(eventId)
		event = Event.query.filter_by(eventId = eventId).first()
		print("eeee", event)
		return render_template("cryptx.html", data = event.teams, event = event)
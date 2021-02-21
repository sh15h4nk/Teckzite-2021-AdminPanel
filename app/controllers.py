from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import LoginManager
from app import app, db
from app.models import User
from app.forms import ChangePassword, ResetRequest
from app.functions import sendMail

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
	
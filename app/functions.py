from app import mail
from flask_mail import Message 
from flask.helpers import flash, url_for
from app.models import User

def sendMail(user):
	token = user.generate_token()
	msg = Message("Password Reset Link", sender='tz2021mailserver@gmail.com', recipients=[user.email])
	msg.body = f"To reset your password, Kindly visit the following link \n{url_for('resetPassword',token= token,_external=True)}\n If you didn't make this request then simply ignore it"
	mail.send(msg)
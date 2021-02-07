from flask_wtf import FlaskForm
from sqlalchemy.sql.sqltypes import String

from wtforms import TextField, PasswordField, IntegerField, SubmitField
from wtforms.fields.simple import TextAreaField

from wtforms.validators import Required, Email, EqualTo

class LoginForm(FlaskForm):
    id = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    submit = SubmitField('Login')
from flask_wtf import FlaskForm
from sqlalchemy.sql.sqltypes import String

from wtforms import TextField, PasswordField, IntegerField, SubmitField

from wtforms.validators import Required, Email, EqualTo

class LoginForm(FlaskForm):
    sid = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    sid = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    role = IntegerField('Role', [
                Required(message='Must provide a role. ;-)')])
    submit = SubmitField("submit")
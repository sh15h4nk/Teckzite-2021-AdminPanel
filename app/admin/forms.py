from flask_wtf import Form
from sqlalchemy.sql.sqltypes import String

from wtforms import TextField, PasswordField

from wtforms.validators import Required, Email, EqualTo, NumberRange

class LoginForm(Form):
    sid = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])


class RegisterForm(Form):
    sid = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    role = NumberRange(min=1, max=3, message='Must provide a role')
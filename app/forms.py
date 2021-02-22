from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.sqltypes import String
from flask_ckeditor import CKEditorField


from wtforms import TextField, StringField, PasswordField, IntegerField, SubmitField, SelectField, FieldList, FormField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import NumberRange, Required, Email, EqualTo, Length, DataRequired,ValidationError

from app.models import User 


class LoginForm(FlaskForm):
    userId = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    submit = SubmitField('Login')


# BRANCH_CHOICES = ['CSE', 'ECE', ('MEC', 'MECH'), 'CIV', ('CHE', 'CHEM'), 'MME', 'PUC']
BRANCH_CHOICES = [('CSE','CSE'), ('ECE','ECE'), ('MEC', 'MECH'), ('CIV','CIV'), ('CHE', 'CHEM'), ('MME','MME'), ('PUC','PUC'),]


class RegisterForm(FlaskForm):
    userId = TextField('Student ID', [
        Required(), Length(min=7, max=7)])  

    name = TextField('Student Name', [
        Required(), Length(min=7, max=20)])

    email = StringField('Email Address', [Email("provide a valid email")])

    phone = IntegerField('Phone Number',
        [Required(), NumberRange(min=6000000000, max=9999999999, message="Enter a valid number")]
    )
    
    dept =  SelectField('Department', choices=BRANCH_CHOICES)

    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
    submit = SubmitField("submit")


    def validate_userId(self, userId):
        user = User.query.filter_by(userId=userId.data).first()
        if user:
            raise ValidationError("User already exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists")
    
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError("Phone already exists")

     

class CreateEventForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=5)])
    event_organiser = FormField(RegisterForm)

    

class UpdateEventForm():
    title = StringField('Title', [DataRequired(), Length(min=5)])
    prize = IntegerField('Fee', [DataRequired()])
    description = CKEditorField('Description', [DataRequired(), Length(min=20)])
    brief = CKEditorField('Status', [DataRequired()])
    status = CKEditorField('Status', [DataRequired()])
    structure = CKEditorField('Timeline', [DataRequired()])
    timeline = CKEditorField('Timeline', [DataRequired()])
    rules = CKEditorField('Timeline', [DataRequired()])
    
    min_teamsize = IntegerField('Minimum team size', 
        [Required(), NumberRange(min=1, max=6, message="Team size is must be 1 to 6")])
    max_teamsize = IntegerField('Maximum team size', 
        [Required(), NumberRange(min=1, max=6, message="Team size is must be 1 to 6")])
    

class Contacts(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email Address', [Email("provide a valid email")])
    phone = IntegerField('Phone Number',
        [Required(), NumberRange(min=6000000000, max=9999999999, message="Enter a valid number")]
    )

class FAQs(FlaskForm):
    question = TextField('Question', [DataRequired()])
    answer = TextField('Answer', [DataRequired()])

class AddWorkshopForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=5)])
    name = StringField('Name', [DataRequired()])
    dept =  SelectField('BRACH', choices=BRANCH_CHOICES)
    description = CKEditorField('Description', [DataRequired(), Length(min=20)])
    fee = IntegerField('Fee', [DataRequired()])
    status = CKEditorField('Status', [DataRequired()])
    about = CKEditorField('About', [DataRequired()])
    timeline = CKEditorField('Timeline', [DataRequired()])
    resources = CKEditorField('About', [DataRequired()])
    submit = SubmitField('Submit')


class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
    submit = SubmitField("Change Password")

class ResetRequest(FlaskForm):
    email = StringField('Email Address', [DataRequired(),Email()])

    submit = SubmitField("Change Password")

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("Email doesn't exists")

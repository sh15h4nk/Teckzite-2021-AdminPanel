from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.sqltypes import String
from flask_ckeditor import CKEditorField


from wtforms import TextField, StringField, PasswordField, IntegerField, SubmitField, SelectField, FieldList, FormField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import NumberRange, Required, Email, EqualTo, Length, DataRequired
 

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
        Required()])

    email = StringField('Email Address', [Email("provide a valid email")])

    phone = IntegerField('Phone Number',
        [Required(), NumberRange(min=6000000000, max=9999999999, message="Enter a valid number")]
    )
    
    dept =  SelectField('BRACH', choices=BRANCH_CHOICES)

    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
    submit = SubmitField("submit")

class CreateEventForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=5)])
    event_coordinator = StringField('Coordinator ID', [DataRequired(), Length(min=7, max=7)])
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
    resources = CKEditorField('Resources', [DataRequired()])
    


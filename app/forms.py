from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.sqltypes import String
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileRequired

from wtforms import TextField, StringField, PasswordField, IntegerField, SubmitField, SelectField, FieldList, FormField, Form
from wtforms.validators import NumberRange, Required, Email, EqualTo, Length, DataRequired,ValidationError

from app.models import User, Workshop

class LoginForm(FlaskForm):
    userId = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    submit = SubmitField('Login')


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


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])  

    

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
    name = StringField('Name')
    email = StringField('Email Address', [Email("provide a valid email")])
    phone = IntegerField('Phone Number',
        [NumberRange(min=6000000000, max=9999999999, message="Enter a valid number")]
    )
    def validate_name(self, name):
        if not name:
            raise ValidationError("Name is Required")

    def validate_email(self, email):
        if not email:
            raise ValidationError("Email is Required")

    def validate_phone(self, phone):
        if not phone:
            raise ValidationError("Phone is Required")

class FAQs(FlaskForm):
    question = StringField('Question')
    answer = StringField('Answer')

    def validate_question(self, question):
        if len(question.data) == 0:
            raise ValidationError("Question is Required")
    def validate_answer(self, answer):
        if len(answer.data) == 0:
            raise ValidationError("Answer is Required")

class AddWorkshopForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=5)])
    dept =  SelectField('BRACH', choices=BRANCH_CHOICES)
    description = CKEditorField('Description', [DataRequired(), Length(min=20)])
    fee = IntegerField('Fee', [DataRequired(message="Enter a valid number"), NumberRange(min=0, max=99999, message="Enter a valid number")])
    status = CKEditorField('Status', [DataRequired()])
    about = CKEditorField('About', [DataRequired()])
    timeline = CKEditorField('Timeline', [DataRequired()])
    resources = CKEditorField('Resources', [DataRequired()])
    primary_contact = FormField(Contacts)
    # contacts = FieldList(FormField(Contacts), min_entries=1, max_entries=3 )

    def validate_title(self, title):
        workshop = Workshop.query.filter_by(title=title.data).first()
        if workshop:
            raise ValidationError("workshop title already exists")
    # def validate_fee(self, fee):
    #     if :
    #         pass

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

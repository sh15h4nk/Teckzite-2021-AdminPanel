from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.sql.sqltypes import Integer, String
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileAllowed, FileField, FileRequired

from wtforms import TextField, StringField, PasswordField, IntegerField, SubmitField, SelectField, FieldList, FormField, Form, RadioField
from wtforms.fields.simple import HiddenField
from wtforms.validators import NumberRange, Required, Email, EqualTo, Length, DataRequired, ValidationError, URL, Optional
from wtforms.widgets.core import HiddenInput

from app.models import Event, Image, User, Workshop

class LoginForm(FlaskForm):
    userId = TextField('Student ID', [
                Required(message='Forgot your college ID')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])
    submit = SubmitField('Login')



BRANCH_CHOICES = [('OPE','OPEN TO ALL'), ('CSE','CSE'), ('ECE','ECE'), ('MEC', 'MECH'), ('CIV','CIV'), ('CHE', 'CHEM'), ('MME','MME'), ('PUC','PUC'),('MAN','MANAGEMENT'),]


class PhotoForm(FlaskForm):
    image = StringField('')
    cropX = StringField('')
    cropY = StringField('')
    cropWidth = StringField('')
    cropHeight = StringField('')

    def validate_image(self, image):
        if not image:
            raise ValidationError("Field is Required")
    def validate_cropX(self, cropX):
        if not cropX:
            raise ValidationError("Field is Required")
    def validate_cropY(self, cropY):
        if not cropY:
            raise ValidationError("Field is Required")
    def validate_cropWidth(self, cropWidth):
        if not cropWidth:
            raise ValidationError("Field is Required")
    def validate_cropHeight(self, cropHeight):
        if not cropHeight:
            raise ValidationError("Field is Required")
    

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
    # profile = FileField('Profile', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])



class UpdateEventForm(FlaskForm):
    title = StringField('Title', [Length(min=5)])
    event_url = TextField('Exam Link', [URL(message="Must be a valid URL"),Optional() ])
    prize = IntegerField('Prize')
    description = CKEditorField('Description', [Length(min=20)])
    brief = CKEditorField('Brief')
    status = CKEditorField('Status')
    structure = CKEditorField('structure')
    timeline = CKEditorField('Timeline')
    rules = CKEditorField('Rules')
    photo = FormField(PhotoForm)

    priority = IntegerField('Priority')
    min_teamsize = IntegerField('Minimum team size', 
        [DataRequired(message = "Enter Valid Number"), NumberRange(min=1, max=6, message="Team size is must be 1 to 6")])
    max_teamsize = IntegerField('Maximum team size', 
        [DataRequired(message = "Enter a Valid Number"), NumberRange(min=1, max=6, message="Team size is must be 1 to 6")])

    def validate_max_teamsize(self, max_teamsize):
        # print(self, max_teamsize.data)
        if max_teamsize.data < self.min_teamsize.data:
            raise ValidationError("Maximum size must be less than or equal Minimum size")
    # # submit = SubmitField('Submit')

class UpdateWorkshopForm(FlaskForm):
    title = StringField('Title', [Length(min=5)])
    fee = IntegerField('Fee', [NumberRange(min=0, max=99999, message="Enter a valid number")])
    priority = IntegerField('Priority')
    description = CKEditorField('Description', [Length(min=20)])
    status = CKEditorField('Status')
    about = CKEditorField('About')
    timeline = CKEditorField('Timeline')
    resources = CKEditorField('Resources')
    pdf = FileField('Upload Resources File')
    photo = FormField(PhotoForm)
   
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
class Sponsors(FlaskForm):
    name = StringField('Name', [Length(min=5)])
    url = TextField('Url', [URL(message="Must be a valid URL")])
    photo = FormField(PhotoForm)
   

class CreateWorkshopForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=5)])
    fee = IntegerField('Fee', [NumberRange(min=0, max=99999, message="Enter a valid number")])
    dept =  SelectField('BRACH', choices=BRANCH_CHOICES)
    workshop_coordinator = FormField(RegisterForm)

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


class UpdateProfileForm(FlaskForm):
    name = TextField('Student Name', [
        Required(), Length(min=7, max=20)])

    email = StringField('Email Address', [Email("provide a valid email")])
    
    gender =  SelectField('Gender', choices=[("male","Male"),("female","Female")])

    phone = IntegerField('Phone Number',
        [Required(), NumberRange(min=6000000000, max=9999999999, message="Enter a valid number")]
    )
    
    dept =  SelectField('Department', choices=BRANCH_CHOICES)

    gender = SelectField('Gender', choices=[('F', 'Female'), ('M', 'Male')])

    submit = SubmitField("Update")



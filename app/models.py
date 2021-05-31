from app import app, db, bcrypt

from sqlalchemy.orm import backref
from sqlalchemy import Column, String, SmallInteger, DateTime, ForeignKey, Boolean, Integer
from enum import unique

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Base(db.Model):
    __abstract__ = True
    id = db.Column(Integer, nullable=False, primary_key=True)
    date_created = db.Column(DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Sponsor(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    url = db.Column(String(128))
    image_url = db.Column(String(128))
    hidden = db.Column(SmallInteger, default=0) # if true, sponsor is inactive

    event_id = db.Column(String(7), ForeignKey('event.eventId'))
    workshop_id = db.Column(String(7), ForeignKey('workshop.workshopId'))

    def __init__(self, name, url, image_url):
        self.name = name
        self.url = url
        self.image_url = image_url


class Image(db.Model):
    id = db.Column(Integer, primary_key=True)
    image_url = db.Column(String(128), nullable=False)
    hidden = db.Column(SmallInteger, default=0) # if true, image is inactive

    def __init__(self, image_url):
        self.image_url = image_url


class Event(Base):
    eventId = db.Column(String(7), nullable=False, unique=True)
    dept = db.Column(String(5))
    title = db.Column(String(128), nullable=False, unique=True)
    prize = db.Column(Integer)
    description = db.Column(String(2000))
    brief = db.Column(String(100))
    status = db.Column(String(200))
    structure = db.Column(String(2000))
    timeline = db.Column(String(2000))
    image_url = db.Column(String(128))
    rules = db.Column(String(2000))
    hidden = db.Column(SmallInteger, default=0) # if true, event is inactive
    priority = db.Column(Integer, default=0)

    contacts = db.relationship('Contact')
    faqs = db.relationship('FAQ')
    sponsors = db.relationship('Sponsor')


    min_teamsize = db.Column(SmallInteger)
    max_teamsize = db.Column(SmallInteger)


    coordinator_id = db.Column(Integer, ForeignKey('user.id'))
    organiser_id = db.Column(Integer, ForeignKey('user.id'),unique=True)

    teams = db.relationship('Team')

    def __init__(self, eventId, title, dept, coordinater_id, organiser_id) -> None:
        self.eventId = eventId
        self.title = title
        self.dept = dept
        self.coordinator_id = coordinater_id
        self.organiser_id = organiser_id

class Workshop(Base):
    workshopId = db.Column(String(7), nullable=False, unique=True)
    title = db.Column(String(128), nullable=False)
    dept = db.Column(String(5))
    description = db.Column(String(256))
    fee = db.Column(Integer, default = 0)
    status = db.Column(String(100))
    about = db.Column(String(500))
    timeline = db.Column(String(500))
    resources = db.Column(String(500))
    file_url = db.Column(String(128))
    image_url = db.Column(String(128))
    priority = db.Column(Integer, default=0)


    coordinator_id = db.Column(Integer, ForeignKey('user.id'), unique=True)
    
    hidden = db.Column(SmallInteger, default=0) # if true, workshop is inactive

    contacts = db.relationship('Contact')
    faqs = db.relationship('FAQ')
    sponsors = db.relationship('Sponsor')

    tech_users = db.relationship('TechUser')

    def __init__(self, workshop_id, title, dept, coordinator_id):
        self.workshopId = workshop_id
        self.title = title
        self.dept = dept
        self.coordinator_id = coordinator_id



class User(UserMixin,Base):
    userId = db.Column(String(7), nullable=False, unique=True)
    name = db.Column(String(128), nullable=False)
    email = db.Column(String(128), nullable=False, unique=True)
    password = db.Column(String(192), nullable=False)
    role = db.Column(String(25), nullable=False)
    dept = db.Column(String(3), nullable=False)
    phone = db.Column(String(10), unique=True)
    gender = db.Column(String(1))
    hidden = db.Column(SmallInteger, default=0) # if true, user is inactive
    # status = db.Column(SmallInteger, default=0) # if false, user is inactive # added to check migrations

    coordinated_events = db.relationship('Event', foreign_keys=[Event.coordinator_id])
    organised_events = db.relationship('Event', foreign_keys=[Event.organiser_id])
    
    coordinated_workshops = db.relationship('Workshop', foreign_keys=[Workshop.coordinator_id])
   
    def generate_token(self, expires_sec=1800):
        serial = Serializer(app.config['SECRET_KEY'], expires_sec)
        return serial.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, userId, name, email, password, role, dept, phone):

        self.userId = userId
        self.name = name
        self.email = email
        self.dept = dept              
        self.password = password
        self.role = role
        self.phone = phone


    def __repr__(self):
        return '<User %r>' % (self.userId)
    
    

class Contact(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    email = db.Column(String(128), nullable=False)
    phone = db.Column(String(10))
    hidden = db.Column(SmallInteger, default=0) # if true, contacr is inactive


    event_id = db.Column(String(7), ForeignKey('event.eventId'))
    workshop_id = db.Column(String(7), ForeignKey('workshop.workshopId'))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class FAQ(db.Model):
    id = db.Column(Integer, primary_key=True)
    question = db.Column(String(100))
    answer = db.Column(String(500))
    hidden = db.Column(SmallInteger, default=0) # if true, faq is inactive

    event_id = db.Column(String(7), ForeignKey('event.eventId'))
    workshop_id = db.Column(String(7), ForeignKey('workshop.workshopId'))

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


class CurrentId(db.Model):
    current_techzite_id = db.Column(Integer, default=10001, primary_key=True)
    current_event_id = db.Column(Integer, default=10001)
    current_workshop_id = db.Column(Integer, default=10001)
    current_ca_id = db.Column(Integer, default=10001)


class Member(db.Model):
    id = db.Column(Integer, primary_key=True,nullable=False)
    stauts = db.Column(Integer, default=0)
    team_id = db.Column(Integer, ForeignKey('team.id'))
    user_id = db.Column(Integer, ForeignKey('tech_user.id'))


class Team(db.Model):
    id = db.Column(Integer, primary_key= True,nullable=False)
    teamId = db.Column(String(7), unique=True, nullable=False)
    event_id = db.Column(Integer, ForeignKey('event.id'))

    members = db.relationship('Member')

class Address(db.Model):
    id = db.Column(Integer, primary_key=True,nullable=False)
    state = db.Column(String(192))
    district = db.Column(String(192))
    city = db.Column(String(192))
    pin = db.Column(String(10))
    t_userId = db.Column(String(7), ForeignKey('tech_user.userId'), unique=True)

    def __init__(self, state, district, city, pin):
        self.state = state
        self.district = district
        self.city = city
        self.pin = pin

class TechUser(Base, UserMixin):
    userId = db.Column(String(7), unique=True, nullable=False)
    gid = db.Column(String(100), unique=True)
    name = db.Column(String(30))
    email = db.Column(String(128), nullable=False, unique=True)
    gender = db.Column(String(1))
    college = db.Column(String(200))
    rgukt_location = db.Column(String(50))
    collegeId = db.Column(String(30))
    idcard_url = db.Column(String(128))
    year = db.Column(String(4))
    branch = db.Column(String(3))
    phone = db.Column(String(10), unique=True)
    registration_status = db.Column(Integer, default=0)
    payment_status = db.Column(Integer, default=0)
    workshop_payment_status = db.Column(Integer, default=0)
    hidden = db.Column(Integer, default=0)

    referral = db.Column(String(30))
    survey = db.Column(String(100))

    address = db.relationship('Address')
    member_of_teams = db.relationship('Member')

    workshop_id = db.Column(String(7), ForeignKey('workshop.workshopId'))

    def __init__(self, userId, gid, name, email):
        self.userId = userId
        self.gid = gid
        self.name = name
        self.email = email


class CA(Base, UserMixin):
    caId = db.Column(String(7), unique=True, nullable=False)
    name = db.Column(String(30))
    email = db.Column(String(128), nullable=False, unique=True)
    phone = db.Column(String(10), unique=True, nullable=False)
    gender = db.Column(String(1))
    college = db.Column(String(200))
    collegeId = db.Column(String(30))
    year = db.Column(String(4))
    branch = db.Column(String(3))
    hidden = db.Column(Integer, default=0)

    def __init__(self, caId, name, email, phone, gender, college, collegeId, year, branch):
        self.caId = caId
        self.name = name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.college = college
        self.collegeId = collegeId
        self.year = year
        self.branch = branch


class Payment(Base):
    tzId = db.Column(String(7), nullable=False)
    time_stamp = db.Column(String(25))
    paid = db.Column(Integer, default=0)
    recipt_no = db.Column(Integer, default=0)
    tkt_type = db.Column(String(30))
    barcode_no = db.Column(Integer, default=0)

    def __init__(self, tzId, time_stamp, paid, recipt_no, tkt_type, barcode_no):
        self.tzId = tzId
        self.time_stamp = time_stamp
        self.paid = paid
        self.recipt_no = recipt_no
        self.tkt_type = tkt_type
        self.barcode_no = barcode_no



# db.create_all()


# Admins
# us = User.query.filter_by(userId="N170076").first()
# if not us:
#     us = User("N170076","admin","N170076@rguktn.ac.in",bcrypt.generate_password_hash("bCrypt#l33t"),"admin","CSE", '9505848891')
#     db.session.add(us)
#     db.session.commit()

# us = User.query.filter_by(userId="N170295").first()
# if not us:
#     us = User("N170295","admin","N170295@rguktn.ac.in",bcrypt.generate_password_hash("bCrypt#l33t"),"admin","CSE", '8331987780')
#     db.session.add(us)
#     db.session.commit()


 
# currentIds = db.session.query(CurrentId).count()
# if currentIds == 0:
#     currentId = CurrentId()
#     db.session.add(currentId)
#     db.session.commit()

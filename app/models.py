from enum import unique
from flask_migrate import branches, current

from sqlalchemy.orm import backref

from app import db, app, bcrypt
from sqlalchemy import Column, String, SmallInteger, DateTime, ForeignKey, Boolean, Integer
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
    hidden = db.Column(SmallInteger, default=0) # if true, event is inactive

    event_id = db.Column(Integer, ForeignKey('event.eventId'))
    workshop_id = db.Column(Integer, ForeignKey('workshop.workshopId'))

    def __init__(self, name, url, image_url):
        self.name = name
        self.url = url
        self.image_url = image_url


class Image(db.Model):
    id = db.Column(Integer, primary_key=True)
    image_url = db.Column(String(128), nullable=False)
    hidden = db.Column(SmallInteger, default=0) # if true, event is inactive

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
    

    contacts = db.relationship('Contact')
    faqs = db.relationship('FAQ')
    sponsors = db.relationship('Sponsor')


    min_teamsize = db.Column(SmallInteger)
    max_teamsize = db.Column(SmallInteger)


    coordinator_id = db.Column(Integer, ForeignKey('user.id'))
    organiser_id = db.Column(Integer, ForeignKey('user.id'),unique=True)

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
    image_url = db.Column(String(128))

    coordinator_id = db.Column(Integer, ForeignKey('user.id'))
    organiser_id = db.Column(Integer, ForeignKey('user.id'),unique=True)
    
    hidden = db.Column(SmallInteger, default=0) # if true, workshop is inactive

    contacts = db.relationship('Contact')
    faqs = db.relationship('FAQ')
    sponsors = db.relationship('Sponsor')

    coordinator_id = db.Column(Integer, ForeignKey('user.id'))

    def __init__(self, workshop_id, title, dept, coordinator_id, organiser_id):
        self.workshopId = workshop_id
        self.title = title
        self.dept = dept
        self.coordinator_id = coordinator_id
        self.organiser_id = organiser_id



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

    coordinated_events = db.relationship('Event', foreign_keys=[Event.coordinator_id])
    organised_events = db.relationship('Event', foreign_keys=[Event.organiser_id])
    
    coordinated_workshops = db.relationship('Workshop', foreign_keys=[Workshop.coordinator_id])
    organised_workshops = db.relationship('Workshop', foreign_keys = [Workshop.organiser_id])
   
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
    hidden = db.Column(SmallInteger, default=0) # if true, event is inactive


    event_id = db.Column(Integer, ForeignKey('event.eventId'))
    workshop_id = db.Column(Integer, ForeignKey('workshop.workshopId'))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class FAQ(db.Model):
    id = db.Column(Integer, primary_key=True)
    question = db.Column(String(100))
    answer = db.Column(String(500))
    hidden = db.Column(SmallInteger, default=0) # if true, event is inactive

    event_id = db.Column(Integer, ForeignKey('event.eventId'))
    workshop_id = db.Column(Integer, ForeignKey('workshop.workshopId'))

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


class CurrentId(db.Model):
    current_techzite_id = db.Column(Integer, default=10001, primary_key=True)
    current_event_id = db.Column(Integer, default=10001)
    current_workshop_id = db.Column(Integer, default=10001)




# class TechUser(Base):
#     name = db.Column(String(128), nullable=False)
#     email = db.Column(String(128), nullable=True, unique=True)
#     password = db.Column(String(192), nullable=False)
#     dept = db.Column(String(128))
#     payment = db.Column(Boolean, nullable=False)
    
#     workshops = db.relationship('Workshop', backref='techUser')

#     team_id = db.Column(db.Integer, ForeignKey('team.id'))

#     event_organiser_id = db.Column(db.Integer, ForeignKey('event.id'))
#     # event_coordinator_id = db.Column(db.Integer, ForeignKey('event.id'))

#     # workshop_coordinator_id = db.Column(db.Integer, ForeignKey('workshop.id'))
#     workshop_organiser_id = db.Column(db.Integer, ForeignKey('workshop.id'))

#     team_id = db.Column(db.Integer, ForeignKey('team.id'))





# class Team(Base):
#     techUsers = db.relationship('TechUser', backref='team')

#     event_id = db.Column(Integer, ForeignKey('event.id'))



db.create_all()

us = User.query.filter_by(userId="admin").first()
if not us:
    us = User("admin","admin","admin@gmail.com",bcrypt.generate_password_hash("admin"),"admin","CSE", 'XXXXXXXXXX')
    db.session.add(us)
    db.session.commit()


us = User.query.filter_by(userId="event_manager").first()
if not us:
    us = User("event_manager","event_manager","event_manager@gmail.com",bcrypt.generate_password_hash("event_manager"),"event_manager","CSE", 'XXX3XXXXXX')
    db.session.add(us)
    db.session.commit()


us = User.query.filter_by(userId="event_coordinator").first()
if not us:
    us = User("event_coordinator","event_coordinator","event_coordinator@gmail.com",bcrypt.generate_password_hash("event_coordinator"),"event_coordinator","CSE", 'XX4XXXXXXX')
    db.session.add(us)
    db.session.commit()


us = User.query.filter_by(userId="event_organiser").first()
if not us:
    us = User("event_organiser","event_organiser","event_organiser@gmail.com",bcrypt.generate_password_hash("event_organiser"),"event_organiser","CSE", 'XX4XXXX4XX')
    db.session.add(us)
    db.session.commit()


us = User.query.filter_by(userId="workshop_manager").first()
if not us:
    us = User("workshop_manager","workshop_manager","workshop_manager@gmail.com",bcrypt.generate_password_hash("workshop_manager"),"workshop_manager","CSE", 'XX5XXXXXXX')
    db.session.add(us)
    db.session.commit()


us = User.query.filter_by(userId="workshop_coordinator").first()
if not us:
    us = User("workshop_coordinator","workshop_coordinator","workshop_coordinator@gmail.com",bcrypt.generate_password_hash("workshop_coordinator"),"workshop_coordinator","CSE", 'XXX5XXXXXX')
    db.session.add(us)
    db.session.commit() 

currentIds = db.session.query(CurrentId).count()
if currentIds == 0:
    currentId = CurrentId()
    db.session.add(currentId)
    db.session.commit()
 
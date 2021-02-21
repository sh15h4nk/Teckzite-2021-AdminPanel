from enum import unique
from typing import Tuple
from flask_migrate import branches

from sqlalchemy.orm import backref

from app import db, app
from sqlalchemy import Column, String, SmallInteger, DateTime, ForeignKey, Boolean, Integer
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Base(db.Model):
    __abstract__ = True
    id = db.Column(Integer, nullable=False, primary_key=True)
    date_created = db.Column(DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Event(Base):
    eventId = db.Column(String(6), nullable=False, unique=True)
    dept = db.Column(String(5), nullable=False)
    title = db.Column(String(128), nullable=False, unique=True)
    prize = db.Column(Integer)
    description = db.Column(String(2000))
    brief = db.Column(String(100))
    status = db.Column(String(200))
    structure = db.Column(String(2000))
    timeline = db.Column(String(2000))
    rules = db.Column(String(2000))

    contacts = db.relationship('Contact')
    faqs = db.relationship('FAQ')

    min_teamsize = db.Column(SmallInteger)
    max_teamsize = db.Column(SmallInteger)

    # organiser_id = db.Column(String(7),unique=True)

    coordinator_id = db.Column(Integer, ForeignKey('user.id'))
    organiser_id = db.Column(Integer, ForeignKey('user.id'),unique=True)

    def __init__(self, id, name, teamsize, details) -> None:
        self.id = id
        self.name = name
        self.teamsize = teamsize
        self.details = details




class User(UserMixin,Base):
    userId = db.Column(String(7), nullable=False, unique=True)
    name = db.Column(String(128), nullable=False)
    email = db.Column(String(128), nullable=False, unique=True)
    password = db.Column(String(192), nullable=False)
    role = db.Column(SmallInteger, nullable=False)
    dept = db.Column(String(3), nullable=False)
    phone = db.Column(String(10), unique=True)
    gender = db.Column(String(1))
    hidden = db.Column(SmallInteger, default=0) # if true, user is inactive

    coordinated_events = db.relationship('Event', foreign_keys=[Event.coordinator_id])
    organised_event = db.relationship('Event', foreign_keys=[Event.organiser_id])
    
    coordinated_workshop = db.relationship('Workshop')
   
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




class Workshop(Base):
    workshopId = db.Column(String(6), nullable=False, unique=True)
    name = db.Column(String(128), nullable=False)
    dept = db.Column(String(5))
    description = db.Column(String(256))
    fee = db.Column(Integer)
    status=db.Column(String(100))
    about=db.Column(String(500))
    timeline = db.Column(String(500))
    resources = db.Column(String(500))

    contact = db.relationship('Contact')
    faqs = db.relationship('FAQ')

    coordinator_id = db.Column(Integer, ForeignKey('user.id'))


    
    

class Contact(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    email = db.Column(String(128), nullable=False, unique=True)
    phone = db.Column(String(10), unique=True)

    event_id = db.Column(Integer, ForeignKey('event.id'))
    workshop_id = db.Column(Integer, ForeignKey('workshop.id'))

class FAQ(db.Model):
    id = db.Column(Integer, primary_key=True)
    question = db.Column(String(100))
    answer = db.Column(String(500))

    event_id = db.Column(Integer, ForeignKey('event.id'))
    workshop_id = db.Column(Integer, ForeignKey('workshop.id'))




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
    us = User("admin","admin","admin@gmail.com","admin",1,"cse", 'XXXXXXXXXX')
    db.session.add(us)
    db.session.commit()


 
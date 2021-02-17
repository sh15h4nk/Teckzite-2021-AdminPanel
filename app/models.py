from enum import unique
from typing import Tuple
from flask_migrate import branches

from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer

from app import db
from sqlalchemy import Column, String, SmallInteger, DateTime
from flask_login import UserMixin


class Base(UserMixin,db.Model):
    __abstract__ = True
    id = db.Column(String(7), nullable=False, primary_key=True)
    date_created = db.Column(DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(Base):
    name = db.Column(String(128), nullable=True)
    email = db.Column(String(128), nullable=True, unique=True)
    password = db.Column(String(192), nullable=False)
    role = db.Column(SmallInteger, nullable=False)
    branch = db.Column(String(5), nullable=False)
    
    

    event_organised_id = db.Column(Integer, ForeignKey('event.id'))
    event_coordinated_id = db.Column(Integer, ForeignKey("event.id"))
    
    workshop_organised_id = db.Column(Integer, ForeignKey('workshop.id'))
    workshop_coordinated_id = db.Column(Integer, ForeignKey("workshop.id"))



    def __init__(self, id, password, role):
        self.id = id
        self.role = role
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


class Event(Base):
    name = db.Column(String(128), nullable=False)
    
    details = db.Column(String(2000))
    teamsize = db.Column(SmallInteger, nullable=False)
    department = db.Column(String(256))
    organiser = db.relationship("User", backref="org_event", foreign_keys=[User.event_organised_id], uselist=False)         # backreference from User to retiieve user hosted event ORGANISER
    coordinator =  db.relationship("User", backref="cord_event",foreign_keys=[User.event_coordinated_id], uselist=False)     # backreference from User to retiieve user hosted event COORDINATOR
    # teams = db.relationship("Team", backref="event")

    def __init__(self, id, name, teamsize, details) -> None:
        self.id = id
        self.name = name
        self.teamsize = teamsize
        self.details = details

class Workshop(Base):
    name = db.Column(String(128), nullable=False)
    department = db.Column(String(256))
    details = db.Column(String(256))
    organiser = db.relationship("User", backref="org_workshop" ,foreign_keys=[User.workshop_organised_id] ,uselist=False)
    coordinator =  db.relationship("User", backref="cord_workshop", foreign_keys=[User.workshop_coordinated_id], uselist=False)

#     tech_user_id = db.Column(String(256), ForeignKey('techUser.id'))




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




 
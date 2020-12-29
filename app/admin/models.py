from enum import unique
from typing import Tuple
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

    def __init__(self, id, password, role):
        self.id = id
        self.role = role
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


db.create_all()

user = User.query.filter_by(id="N170076").first()

if not user:
    user = User("N170076", "p@ss", 1)
    db.session.add(user)
    db.session.commit()


 
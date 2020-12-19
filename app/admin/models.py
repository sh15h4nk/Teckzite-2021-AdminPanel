from enum import unique
from app import db
from sqlalchemy import Column, String, SmallInteger, DateTime

class Base(db.Model):
    __abstract__ = True
    id = db.Column(String(7), primary_key=True)
    date_created = db.Column(DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(Base):
    sid = db.Column(String(128), nullable=False, unique=True)
    name = db.Column(String(128), nullable=False)
    email = db.Column(String(128), nullable=False, unique=True)
    password = db.Column(String(192), nullable=False)
    role = db.Column(SmallInteger, nullable=False)

    def __init__(self, sid, password, role):
        self.sid = sid
        self.role = role
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)





 
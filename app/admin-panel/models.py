from app import db
from sqlalchemy import Column, String, SmallInteger, DateTime

class Base(db.Model):
    __abstract__ = True
    id = Column(String(7), primary_key=True)
    date_created = Column(DateTime, default=db.func.current_timestamp())
    date_modified = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class User(Base):
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(192), nullable=False)
    role = Column(SmallInteger, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)





 
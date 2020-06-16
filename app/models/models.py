from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    google_id = Column('google_id', String(30), primary_key=True)
    subject_id = Column('subject_id', Integer, ForeignKey('subjects.id'))
    subject = relationship('Subject', backref='users', order_by='Subject.id')
    class_number = Column('class_number', Integer)
    is_admin = Column('is_admin', Boolean, nullable=False)
    created = Column('created', DateTime, default=datetime.now(), nullable=False)
    updated = Column('updated', DateTime, default=datetime.now(), nullable=False)
    created_by = Column('created_by', String(31))
    updated_by = Column('updated_by', String(31))



    def __init__(self, google_id, subject_id, is_admin, created_by=None, updated_by=None, class_number=None):
        self.google_id = google_id
        self.subject_id = subject_id
        self.class_number = class_number
        self.is_admin = is_admin
        self.updated = datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'class_number': self.class_number,
            'is_admin': self.is_admin,
            'created': self.created,
            'updated': self.updated,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
    def __repr__(self):
        return '<User: {}>'.format(self.id)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(31), nullable=False)
    user_list = relationship('User', backref='subjects')
    created = Column(DateTime, default=datetime.now(), nullable=False)
    updated = Column(DateTime, default=datetime.now(), nullable=False)
    created_by = Column(String(31))
    updated_by = Column(String(31))

    def __init__(self, name, created_by=None, updated_by=None):
        self.name = name
        self.updated = datetime.now()
        self.created_by = created_by
        self.updated_by = datetime.now()

    def to_dict(self, is_auth=False):
        result = {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'updated': self.updated,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        } 
        if is_auth:
            result['user_list'] = [user.to_dict() for user in self.user_list]   
        return result
    def __repr__(self):
        return '<Subject: {}>'.format(self.name)

class JobOffer(Base):
    __tablename__ = 'job_offers'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    company_id = Column('company_id', Integer)
    occupation = Column('occupation', Integer)
    max_appicants = Column('max_appicants', Integer)
    starting_salary = Column('starting_salary', Integer)
    image_url_text = Column('image_url_text', Text)
    created = Column(DateTime, default=datetime.now(), nullable=False)
    updated = Column(DateTime, default=datetime.now(), nullable=False)
    created_by = Column(String(31))
    updated_by = Column(String(31))

def to_dict(self, is_auth=False):
    result = {
        'id': self.id,
        'name': self.name,
        'created': self.created,
        'updated': self.updated,
        'created_by': self.created_by,
        'updated_by': self.updated_by
    } 
    if is_auth:
        result['user_list'] = [user.to_dict() for user in self.user_list]   
    return result
def __repr__(self):
    return '<Subject: {}>'.format(self.name)


class Company(Base):
    __tablename__ = 'job_offers'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    company_id = Column('company_id', Integer)
    occupation = Column('occupation', Integer)
    max_appicants = Column('max_appicants', Integer)
    starting_salary = Column('starting_salary', Integer)
    image_url_text = Column('image_url_text', Text)
    created = Column(DateTime, default=datetime.now(), nullable=False)
    updated = Column(DateTime, default=datetime.now(), nullable=False)
    created_by = Column(String(31))
    updated_by = Column(String(31))

def to_dict(self, is_auth=False):
    result = {
        'id': self.id,
        'name': self.name,
        'created': self.created,
        'updated': self.updated,
        'created_by': self.created_by,
        'updated_by': self.updated_by
    } 
    if is_auth:
        result['user_list'] = [user.to_dict() for user in self.user_list]   
    return result
def __repr__(self):
    return '<Subject: {}>'.format(self.name)
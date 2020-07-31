from datetime import datetime
from database import db


class User(db.Model):
    __tablename__ = 'users'
    google_id = db.Column('google_id', db.String(30), primary_key=True)
    subject_id = db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'))
    subject = db.relationship('Subject', backref='users', order_by='Subject.id')
    class_number = db.Column('class_number', db.Integer)
    is_admin = db.Column('is_admin', db.Boolean, nullable=False)
    created = db.Column('created', db.DateTime, default=datetime.now(), nullable=False)
    updated = db.Column('updated', db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column('created_by', db.String(31))
    updated_by = db.Column('updated_by', db.String(31))



    def __init__(self, google_id, subject_id, is_admin, created_by='system', updated_by='system', class_number=None):
        self.google_id = google_id
        self.subject_id = subject_id
        self.class_number = class_number
        self.is_admin = is_admin
        self.updated = datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by
    
    def to_dict(self):
        return {
            'google_id': self.google_id,
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


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(31), nullable=False)
    user_list = db.relationship('User', backref='subjects')
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.String(31))
    updated_by = db.Column(db.String(31))

    def __init__(self, name, created_by='system', updated_by='system'):
        self.name = name
        self.updated = datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by

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

class JobOffer(db.Model):
    __tablename__ = 'job_offers'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column('company_name', db.String(31), nullable=False)
    industry_id = db.Column('industry_id', db.ForeignKey("industrys.id"))
    industry = db.relationship('Industry', backref='job_offers')
    occupation = db.Column('occupation', db.String(60), nullable=False)
    max_appicants = db.Column('max_appicants', db.Integer)
    starting_salary = db.Column('starting_salary', db.Integer)
    image_url_text = db.Column('image_url_text', db.Text)
    # company_street_addresses = db.relationship("CompanyStreetAddress",backref="job_offers")
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.String(31))
    updated_by = db.Column(db.String(31), default=None)

    def __init__(self, company_name, industry_id, occupation, max_appicants, starting_salary, image_url_text, created_by='system', updated_by='system'):
        self.company_name = company_name
        self.industry_id = industry_id
        self.occupation = occupation
        self.max_appicants = max_appicants
        self.starting_salary = starting_salary
        self.image_url_text = image_url_text
        self.created_by = created_by
        self.updated_by = updated_by
        self.updated = datetime.now()

    def to_dict(self, is_auth=False):
        result = {
            'id': self.id,
            'company_name': self.company_name,
            # 'industry_id': self.industry_id,
            'occupation': self.occupation,
            'max_appicants': self.max_appicants,
            'starting_salary': self.starting_salary,
            'image_url_text': self.image_url_text,
            'created': self.created,
            'updated': self.updated,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
        }    
        if self.industry is None:
            result['industry'] = {}
        else:
            result['industry'] = self.industry.to_dict(),
        return result
    def __repr__(self):
        return '<JobOffer: {}>'.format(self.company_name)

class Industry(db.Model):
    __tablename__ = 'industrys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name',db.String(40))
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    created_by = db.Column(db.String(31))
    updated_by = db.Column(db.String(31))
    joboffers = db.relationship("JobOffer",backref="industrys")

    def __init__(self, name, created_by='system', updated_by='system'):
        self.name = name
        self.updated = datetime.now()
        self.created_by = created_by
        self.updated_by = updated_by
    
    def to_dict(self, is_auth=False):
        result = {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'updated': self.updated,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }    
        return result
    def __repr__(self):
        return '<Subject: {}>'.format(self.name)

# class CompanyStreetAddress(db.Model):
#     __tablename__ = 'company_street_addresses'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     job_offer_id = db.Column('job_offer_id', db.ForeignKey("job_offers.id"))
#     street_address = db.Column('street_address',db.String(200))
#     is_main = db.Column('is_main', db.Boolean, nullable=False)
#     created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
#     updated = db.Column(db.DateTime, default=datetime.now(), nullable=False)
#     created_by = db.Column(db.String(31))
#     updated_by = db.Column(db.String(31))
#     joboffers = db.relationship("JobOffer",backref="company_street_addresses")

#     def __init__(self, street_address, is_main, created_by='system', updated_by='system'):
#         self.street_address = street_address
#         self.is_main = is_main
#         self.updated = datetime.now()
#         self.created_by = created_by
#         self.updated_by = updated_by
    
#     def to_dict(self, is_auth=False):
#         result = {
#             'id': self.id,
#             'street_address': self.street_address,
#             'is_main': self.is_main,
#             'created': self.created,
#             'updated': self.updated,
#             'created_by': self.created_by,
#             'updated_by': self.updated_by
#         }    
#         return result
#     def __repr__(self):
#         return '<Subject: {}>'.format(self.name)
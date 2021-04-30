from flask_login import UserMixin
from . import db

class person(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True, primary_key=True)
    password = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)

class books(db.Model):
    isbn = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    year = db.Column(db.String(100))

class reviews(db.Model):
    reviewer = db.Column(db.String(80))
    isbn = db.Column(db.String(80), primary_key=True)
    rating = db.Column(db.String(80))
    review = db.Column(db.String(80))

class bookshelf(db.Model):
    reviewer = db.Column(db.String(100))
    book = db.Column(db.String(100), primary_key=True)
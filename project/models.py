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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class books(UserMixin, db.Model):
    isbn = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    year = db.Column(db.Integer)


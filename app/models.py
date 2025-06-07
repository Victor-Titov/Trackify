from . import db
from datetime import time
from flask_sqlalchemy import SQLAlchemy



class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    time = db.Column(db.Time)
    desc = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)



class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    habits = db.relationship('Habit', backref='person', lazy=True)


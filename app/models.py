from . import db
from datetime import time, datetime
from flask_sqlalchemy import SQLAlchemy




class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    time = db.Column(db.Time)
    desc = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    habits = db.relationship('Habit', backref='person', lazy=True)
    habits_completed_today = db.Column(db.Integer, default=0)



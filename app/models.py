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
    done_today = db.Column(db.Boolean, default=False)
    completion_history = db.relationship('HabitCompletion', back_populates='habit', lazy=True, cascade='all, delete-orphan')


person_leaderboard = db.Table(
    'person_leaderboard',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('leaderboard_id', db.Integer, db.ForeignKey('leaderboard.id'), primary_key=True)
)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    habits = db.relationship('Habit', backref='person', lazy=True)
    habits_completed_today = db.Column(db.Integer, default=0)
    
    leaderboards = db.relationship('Leaderboard', secondary=person_leaderboard, backref=db.backref('participants', lazy='dynamic'),lazy='dynamic')


class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())


class HabitCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, default=db.func.current_date())
    completed = db.Column(db.Boolean, default=True)

    habit = db.relationship('Habit', back_populates='completion_history')
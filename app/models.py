from datetime import datetime
from app import db

class Commserv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    hostname = db.Column(db.String(120))
    servicepack = db.Column(db.String(120))
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<Commserv %s>' % self.name


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    inputs = db.Column(db.Text)

    def __repr__(self):
        return '<TestCase %s>' % self.number


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<TestRun %s>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %s>' % self.name
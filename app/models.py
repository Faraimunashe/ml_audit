from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Time
from flask_login import UserMixin
import datetime
from app import db
from datetime import date

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Integer)

    def __init__(self, email, password, name, role):
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role
        }

        

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100))
    model_id = db.Column(db.Integer)
    action = db.Column(db.String(50)) 
    previous_data = db.Column(db.JSON)
    new_data = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, model_name, model_id, action, previous_data, new_data, user_id):
        self.model_name = model_name
        self.model_id = model_id
        self.action = action
        self.previous_data = previous_data
        self.new_data = new_data
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "model_name": self.model_name,
            "model_id": self.model_id,
            "action": self.action,
            "previous_data": self.previous_data,
            "new_data": self.new_data,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id
        }



from datetime import datetime
from shawspace import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(60), nullable=False)
    role=db.Column(db.String(60), nullable=False)
    Web_development=db.Column(db.Boolean, default=False)
    App_development=db.Column(db.Boolean, default=False)
    Competitive_Programming=db.Column(db.Boolean, default=False)
    Machine_Learning=db.Column(db.Boolean, default=False)
    CyberSecurity=db.Column(db.Boolean, default=False)
    Finance=db.Column(db.Boolean, default=False)

class Mentee(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(60), nullable=False)
    Web_development=db.Column(db.Boolean, default=False)
    App_development=db.Column(db.Boolean, default=False)
    Competitive_Programming=db.Column(db.Boolean, default=False)
    Machine_Learning=db.Column(db.Boolean, default=False)
    CyberSecurity=db.Column(db.Boolean, default=False)
    Finance=db.Column(db.Boolean, default=False)
    mentor_id=db.Column(db.Integer, db.ForeignKey('mentor.id') )

class Mentor(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(60), nullable=False)
    Web_development=db.Column(db.Boolean, default=False)
    App_development=db.Column(db.Boolean, default=False)
    Competitive_Programming=db.Column(db.Boolean, default=False)
    Machine_Learning=db.Column(db.Boolean, default=False)
    CyberSecurity=db.Column(db.Boolean, default=False)
    Finance=db.Column(db.Boolean, default=False)
    mentees=db.relationship('Mentee', backref='mentor', lazy=True)
    mentee_count=db.Column(db.Integer, default=0, nullable=False)    

class Messages(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    mentor_id=db.Column(db.Integer, db.ForeignKey('mentor.id'))
    sender=db.Column(db.String(100),nullable=False)
    message_content=db.Column(db.String(1000),nullable=False)
    time_stamp=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

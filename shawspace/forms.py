from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from shawspace.models import Mentor, Mentee, User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email= StringField('Email',
                       validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role=BooleanField('Are you a mentor?')
    web_development=BooleanField('Web Development')
    app_development=BooleanField('App Development')
    machine_learning=BooleanField('Machine Learning')
    competitive_programming=BooleanField('Competitive Programming')
    cybersecurity=BooleanField('CyberSecurity')
    finance=BooleanField('Finance')
    submit= SubmitField('Sign Up')

    def validate_username(self, username):
        x=Mentor.query.filter_by(username=username.data).first()
        y=Mentee.query.filter_by(username=username.data).first()
        if x or y:
            raise ValidationError('That username is taken. Please choose another username.')
        
    def validate_email(self, email):
        x=Mentor.query.filter_by(email=email.data).first()
        y=Mentee.query.filter_by(email=email.data).first()
        if x or y:
            raise ValidationError('That email is taken. Please choose another email.')

class LoginForm(FlaskForm):
    email=StringField('Email',
                       validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    role=BooleanField('Are you a mentor?')
    remember=BooleanField('Remember me')
    submit= SubmitField('Login')

class ReminderForm_Mentor(FlaskForm):
    subject=StringField('Subject', validators=[DataRequired()])
    mail_content=StringField('Mail', validators=[DataRequired()])

class ReminderForm_Mentee(FlaskForm):
    subject=StringField('Subject', validators=[DataRequired()])
    mail_content=StringField('Mail', validators=[DataRequired()])

class GroupChatForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    room_code = StringField('Room Code', validators=[DataRequired()])
    action = RadioField ('Action', choices=[('create', 'Create Room'),('join', 'Join Room')], default='create')



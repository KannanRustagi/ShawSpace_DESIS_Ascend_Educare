
from flask import render_template, url_for, redirect, request
from shawspace import app, db, bcrypt
from shawspace.forms import RegistrationForm, LoginForm
from shawspace.models import User,Mentor, Mentee
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///students.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db1 = SQLAlchemy(app)
# app.secret_key = "akanksha"
# Bootstrap(app)
#
#
# class Signup(db1.Model):
#     __tablename__ = 'signup'
#     first_name = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#
#     def add_newuser(self, first_name, password):
#         new_user = Signup(first_name=first_name, password=password)
#
#         db1.session.add(new_user)
#         db1.session.commit()
#
#
# db1.create_all()


@app.route('/')
def index():
    return render_template('index.html')

def match(x1,x2,x3,x4,x5,x6):
    mentor_list=Mentor.query.filter(Mentor.mentee_count<5)
    max_interests_matched=0
    mentor_id=0
    for mentor in mentor_list:
        interests_matched=0
        if x1==True and x1==mentor.Web_development:
            interests_matched=interests_matched+1
        if x2==True and x2==mentor.App_development:
            interests_matched=interests_matched+1
        if(x3==True and x3==mentor.Competitive_Programming):
            interests_matched=interests_matched+1
        if(x4==True and x4==mentor.Machine_Learning):
            interests_matched=interests_matched+1
        if(x5==True and x5==mentor.CyberSecurity):
            interests_matched=interests_matched+1
        if(x6==True and x6==mentor.Finance):
            interests_matched=interests_matched+1

        if max_interests_matched<interests_matched:
            mentor_id=mentor.id
            
    
    return mentor_id

@app.route("/register",methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.role.data==True:
            mentor=Mentor(username=form.username.data, email=form.email.data, password=hashed_pw,
                            Web_development=form.web_development.data, App_development=form.app_development.data,
                           Competitive_Programming=form.competitive_programming.data, Machine_Learning=form.machine_learning.data,
                           CyberSecurity=form.cybersecurity.data, Finance=form.finance.data)
            user=User(username=form.username.data, email=form.email.data, password=hashed_pw, role="mentor",
                            Web_development=form.web_development.data, App_development=form.app_development.data,
                           Competitive_Programming=form.competitive_programming.data, Machine_Learning=form.machine_learning.data,
                           CyberSecurity=form.cybersecurity.data, Finance=form.finance.data)
            db.session.add(mentor)
            db.session.add(user)
            db.session.commit()
            # flash('your account has been created, you are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            mentor_id=match(form.web_development.data, form.app_development.data,form.competitive_programming.data,
                             form.machine_learning.data,form.cybersecurity.data,form.finance.data )
            mentee=Mentee(username=form.username.data, email=form.email.data, password=hashed_pw,
                            Web_development=form.web_development.data, App_development=form.app_development.data,
                           Competitive_Programming=form.competitive_programming.data, Machine_Learning=form.machine_learning.data,
                           CyberSecurity=form.cybersecurity.data, Finance=form.finance.data, mentor_id=mentor_id)
            user=User(username=form.username.data, email=form.email.data, password=hashed_pw, role="mentee",
                            Web_development=form.web_development.data, App_development=form.app_development.data,
                           Competitive_Programming=form.competitive_programming.data, Machine_Learning=form.machine_learning.data,
                           CyberSecurity=form.cybersecurity.data, Finance=form.finance.data)
            db.session.add(mentee)
            db.session.add(user)
            mentor1=Mentor.query.filter_by(id=mentor_id).first()
            mentor1.mentee_count=mentor1.mentee_count+1
            db.session.commit()
            # flash('your account has been created, you are now able to log in', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     users = Signup.query.all()
    #     for user in users:
    #         if username == user.first_name and password == user.password:
    #             return render_template('mentee.html')
    #
    #     else:
    #         # Failed login
    #         return "Incorrect username or password"
    # else:
    #     # GET request, render the login form
    #     return render_template('login.html')
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
            # flash('Login Unsuccessful', 'danger')
    return render_template('login1.html', title='Login', form=form)


@app.route("/404")
def error():
     return render_template('404.html', title='404')



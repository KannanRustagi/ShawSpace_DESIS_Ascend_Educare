from curses import flash
from flask import render_template, url_for, redirect, request
from shawspace import app, db, bcrypt,mail
from shawspace.forms import RegistrationForm, LoginForm, ReminderForm_Mentor
from shawspace.models import User,Mentor, Mentee, Messages
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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


@app.route("/login",methods=['GET', 'POST'])
def login():
    print("hhhh")
    if current_user.is_authenticated:
        print("hello")
        return redirect(url_for('index'))
    print("hi")
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
            # flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/404")
def error():
     return render_template('404.html', title='404')


@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for('index'))

@app.route("/reminder")
@login_required
def reminder():
    if current_user.role=='mentor':
        form=ReminderForm_Mentor()
        recipients_id=Mentee.query.filter_by(mentor_id=current_user.id)
        recipients_mails=[]
        for mentee in recipients_id:
            recipients_mails.append(mentee.email)
        msg = Message(
                form.subject.data,
                sender =current_user.email,
                recipients = recipients_mails
               )
        msg.body = form.mail_content.data
        mail.send(msg)
        return render_template('mentors.html', title='Reminder', form=form)

@app.route("/chat")
@login_required
def chat():
    if current_user.role=='mentor':
        group_id=current_user.id
    else:
        group_id=current_user.mentor_id

    messages=Messages.query.filter_by(mentor_id=group_id)
       

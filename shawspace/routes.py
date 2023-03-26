import random
from flask import flash, render_template, url_for, redirect, request, session
from shawspace import app, db, bcrypt,mail, socketio
from shawspace.forms import RegistrationForm, LoginForm, ReminderForm_Mentor, GroupChatForm, ReminderForm_Mentee
from shawspace.models import User,Mentor, Mentee, Messages
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask_socketio import join_room, leave_room, send, SocketIO, emit
from string import ascii_uppercase

@app.route('/')
def index():
    return render_template('index.html')

def match(x1,x2,x3,x4,x5,x6):
    mentor_list=Mentor.query.filter(Mentor.mentee_count<5)
    max_interests_matched=0
    mentor_id=-1
    if len(mentor_list)>0:
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
    if(mentor_id==-1 and len(mentor_list)>0):
        mentor_id=mentor_list[0].id
            
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
            flash('your account has been created, you are now able to log in')
            return redirect(url_for('login'))
        else:
            mentor_id=match(form.web_development.data, form.app_development.data,form.competitive_programming.data,
                             form.machine_learning.data,form.cybersecurity.data,form.finance.data )
            if mentor_id==-1:
                flash('No free mentors available right now, please try later :)')
                return redirect(url_for('register'))
            else:
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
                flash('your account has been created, you are now able to log in', 'success')
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
            flash('Login Unsuccessful')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


@app.route("/404")
def error():
     return render_template('404.html', title='404')


@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for('index'))

@app.route("/reminder", methods=['POST', 'GET'])
@login_required
def reminder():
    if current_user.role=='mentor':
        form=ReminderForm_Mentor()
        subject=request.form.get('subject')
        body=request.form.get('mail_content')
        recipients_id=Mentee.query.filter_by(mentor_id=current_user.id)
        recipients_mails=[]
        for mentee in recipients_id:
            recipients_mails.append(mentee.email)
        msg = Message(
                subject,
                sender ='shawspace8@gmail.com',
                recipients = recipients_mails
               )
        msg.body = body
        mail.send(msg)
        return render_template('mentors.html', title='Reminder', form=form)
    
    if current_user.role=='mentee':
        form=ReminderForm_Mentee()
        subject=request.form.get('subject')
        body=request.form.get('mail_content')
        mentee=Mentee.query.filter_by(username=current_user.username).first()
        mentor=Mentor.query.filter_by(id=mentee.mentor_id).first()
        recipients_mails=[]
        recipients_mails.append(mentor.email)
        msg = Message(
                subject,
                sender ='shawspace8@gmail.com',
                recipients = recipients_mails
               )
        msg.body = body
        mail.send(msg)
        return render_template('mentee.html', title='Reminder', form=form)


@app.route("/profile")
@login_required
def profile():
    if current_user.role=='mentor':
        mentees=Mentee.query.filter_by(mentor_id=current_user.id)
        return render_template('mentor_profile.html', title='Profile', mentees=mentees)
    if current_user.role=='mentee':
        mentee=Mentee.query.filter_by(email=current_user.email).first()
        mentor=Mentor.query.filter_by(id=mentee.mentor_id).first()
    return render_template('mentee_profile.html', title='Profile', mentor=mentor)

@app.route("/vc")
@login_required
def vc():
    return render_template('home.html')
    
rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@app.route("/group_chat", methods=["POST", "GET"])
def group_chat():
    session.clear()
    form=GroupChatForm()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home1.html", error="Please enter a name.", code=code, name=name, form=form)

        if join != False and not code:
            return render_template("home1.html", error="Please enter a room code.", code=code, name=name, form=form)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home1.html", error="Room does not exist.", code=code, name=name, form=form)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home1.html", form=form)


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


    


# @app.route("/chat")
# @login_required
# def chat():
#     if current_user.role=='mentor':
#         group_id=current_user.id
#     else:
#         group_id=current_user.mentor_id

#     messages=Messages.query.filter_by(mentor_id=group_id)   
    
    


       

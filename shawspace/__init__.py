from flask import Flask
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import join_room, leave_room, send, SocketIO

app=Flask(__name__)

csrf = CSRFProtect(app)
socketio=SocketIO(app)

app.config['SECRET_KEY']='bd73c0dd78b2092e561807c2f9c76d40'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.app_context().push()
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shawspace8@gmail.com'
app.config['MAIL_PASSWORD'] = 'sbzpwxckgvomdbmm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


from shawspace import routes
from flask import Flask
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

csrf = CSRFProtect(app)

app.config['SECRET_KEY']='bd73c0dd78b2092e561807c2f9c76d40'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.app_context().push()

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

from shawspace import routes
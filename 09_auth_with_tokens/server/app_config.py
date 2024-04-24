from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
# from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
from datetime import timedelta
app = Flask(__name__)
#! Flask SQLALCHEMY configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#! Flask Session configuration
# app.secret_key = environ.get("SESSION_SECRET")
# app.config["SESSION_TYPE"] = "sqlalchemy"
# app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"
# app.config["SESSION_SQLALCHEMY"] = db

#! Flask JWT Extended configuration
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET")
# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=30)

#! Extensions Setup
# flask-sqlalchemy connection to app
db = SQLAlchemy(app)
# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")
# flask-marshmallow connection to app
ma = Marshmallow(app)
# flask-session
# session = Session(app)
# session.app.session_interface.db.create_all()
flask_bcrypt = Bcrypt(app)
#! Flask JWT Extended configuration
jwt = JWTManager(app)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
# from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from os import environ

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

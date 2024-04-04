from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# flask-sqlalchemy connection to app
db = SQLAlchemy(app)
# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")
# flask-marshmallow connection to app
ma = Marshmallow(app)
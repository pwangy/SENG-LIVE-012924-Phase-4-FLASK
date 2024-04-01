from flask import Flask, request, g, jsonify, render_template, make_response
from sqlite3 import IntegrityError
from flask_migrate import Migrate
from models import db, Production, CrewMember

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def welcome():
    return render_template("home.html", name="Matteo")

@app.route("/productions", methods=["GET", "POST"])
def productions():
    if request.method == "GET":
        serialized_prods = [prod.as_dict() for prod in Production.query]
        # return jsonify(serialized_prods), 200
        # return make_response(serialized_prods, 200)
        return serialized_prods, 200
    else:
        try:
            data = request.get_json() #! to jsonify data a Content-Type headers has to be set on the requester side of things
            prod = Production(**data) #! model validations will kick in here
            db.session.add(prod)
            db.session.commit() #! db constraints will kick in here 
            return prod.as_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

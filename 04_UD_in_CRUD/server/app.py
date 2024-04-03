#!/usr/bin/env python3

#! 📚 Review With Students:
# API Fundamentals
# MVC Architecture and Patterns / Best Practices
# RESTful Routing
# Serialization
# Postman

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py


from flask import Flask, request, g, jsonify, render_template, make_response
from sqlite3 import IntegrityError
from flask_migrate import Migrate
from models import db, Production, CrewMember
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, InternalServerError, MethodNotAllowed
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-sqlalchemy connection to app
db.init_app(app)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")


@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404

@app.before_request
def before_request():
    #! calculate current time
    #! set it on g
    if request.endpoint == "productionbyid":
        id = request.view_args.get("id")
        prod = db.session.get(Production, id)
        g.prod = prod

@app.after_request
def after_request():
    #! calculate current time
    #! subtrack current from g.original_time
    #! add a response headers to point to the total time elapsed
    pass

@app.route("/")
def welcome():
    return render_template("home.html", name="Matteo")
class Productions(Resource):
    def get(self):
        try:
            serialized_prods = [
                prod.to_dict(
                    only=(
                        "id",
                        "title",
                        "genre",
                        "director",
                        "description",
                        "budget",
                        "image",
                        "ongoing",
                    )
                )
                for prod in Production.query
            ]
            # return make_response(jsonify(serialized_prods), 200)
            return serialized_prods, 200
        except Exception as e:
            return str(e), 400

    def post(self):
        try:
            data = request.get_json() #! to jsonify data a Content-Type headers has to be set on the requester side of things
            prod = Production(**data) #! model validations will kick in here
            db.session.add(prod)
            db.session.commit() #! db constraints will kick in here
            return prod.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 422

api.add_resource(Productions, "/productions")

class ProductionById(Resource):
    def get(self, id):
        if g.prod:
            return g.prod.to_dict(rules=("-crew_members",)), 200
        return {"message": f"Could not find Production with id #{id}"}, 404

    def patch(self, id):
        if g.prod:
            try:
                data = request.json #! extract data out of the request (json OR get_json())
                for attr, value in data.items(): #! unpack dict keys and values to mass assign onto the object
                    setattr(g.prod, attr, value)
                db.session.commit()
                return g.prod.to_dict(), 200
            except Exception as e:
                return {"message": str(e)}, 422
        return {"message": f"Could not find Production with id #{id}"}, 404

    def delete(self, id):
        if g.prod:
            db.session.delete(g.prod)
            db.session.commit()
            return "", 204
        return {"message": f"Could not find Production with id #{id}"}, 404

api.add_resource(ProductionById, "/productions/<int:id>")
if __name__ == "__main__":
    app.run(port=5555, debug=True)

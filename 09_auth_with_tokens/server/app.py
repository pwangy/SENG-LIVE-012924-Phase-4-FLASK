#!/usr/bin/env python3

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py

#! External libraries imports
from flask import request, g, render_template, make_response, session
from time import time
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from functools import wraps
#! Internal imports
from app_config import app, api, db
from models.production import Production
from models.crew_member import CrewMember
from models.user import User
from schemas.crew_member_schema import crew_member_schema, crew_members_schema
from schemas.production_schema import production_schema, productions_schema


#! ==================
#! GENERAL ROUTE CONCERNS
@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404


@app.before_request
def before_request():
    #! First refactor when inserting crew routes BUT not very DRY right?
    # if request.endpoint == "productionbyid":
    #     id = request.view_args.get("id")
    #     prod = db.session.get(Production, id)
    #     g.prod = prod
    # elif request.endpoint == "crewmemberbyid":
    #     id = request.view_args.get("id")
    #     crew = db.session.get(CrewMember, id)
    #     g.crew = crew
    #! Better Approach
    path_dict = {"productionbyid": Production, "crewmemberbyid": CrewMember}
    if request.endpoint in path_dict:
        id = request.view_args.get("id")
        record = db.session.get(path_dict.get(request.endpoint), id)
        key_name = "prod" if request.endpoint == "productionbyid" else "crew"
        setattr(g, key_name, record)

    #! calculate current time
    #! set it on g
    g.time = time()
    # if request.endpoint not in ['login', 'signup']:
    #     if 'user_id' not in session:
    #         return {"message": "Access Denied, please log in!"}, 422

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return {"message": "Access Denied, please log in!"}, 422
        return func(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):  #! notice the response argument automatically passsed in
    diff = time() - g.time
    print(f"Request took {diff} seconds")
    response.headers["X-Response-Time"] = str(diff)
    response.set_cookie("max-reads", "3")
    return response


#!======================
#! API ROUTES
@app.route("/")
def welcome():
    return render_template("home.html", name="Matteo")


class Productions(Resource):

    @login_required
    def get(self):
        try:
            #! Pre-marshmallow code
            # serialized_prods = [
            #     prod.to_dict(
            #         only=(
            #             "id",
            #             "title",
            #             "genre",
            #             "director",
            #             "description",
            #             "budget",
            #             "image",
            #             "ongoing",
            #         )
            #     )
            #     for prod in Production.query
            # ]
            #! Marshmallow code
            serialized_prods = productions_schema.dump(Production.query)
            # resp = make_response((serialized_prods), 200, {"Content-Type": "application/json"})
            # resp.set_cookie()
            # return resp
            return serialized_prods, 200
        except Exception as e:
            return str(e), 400
    @login_required
    def post(self):
        try:
            data = (
                request.get_json()
            )  #! to jsonify data a Content-Type headers has to be set on the requester side of things
            # prod = Production(**data) #! Pre-marshmallow: model validations will kick in here
            prod = production_schema.load(
                data
            )  #! marshmallow: marshmallow first and then model validations will kick in here
            db.session.add(prod)
            db.session.commit()  #! db constraints will kick in here
            return production_schema.dump(prod), 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 422


api.add_resource(Productions, "/productions")


class ProductionById(Resource):
    def get(self, id):
        if g.prod:
            # return g.prod.to_dict(), 200 #! Pre-marshmallow code
            return production_schema.dump(g.prod), 200
        return {"message": f"Could not find Production with id #{id}"}, 404

    def patch(self, id):
        if g.prod:
            try:
                #! Pre-marshmallow code
                # data = request.json #! extract data out of the request (json OR get_json())
                # for attr, value in data.items(): #! unpack dict keys and values to mass assign onto the object
                #     setattr(g.prod, attr, value)
                # db.session.commit()
                # return g.prod.to_dict(), 200
                #! Marshmallow refactor of patch
                data = (
                    request.json
                )  #! extract data out of the request (json OR get_json())
                # * partial = True allows partial updates, meaning only the provided fields
                # * in the JSON data will be updated, and the rest will remain unchanged.
                # * Remember what we said about passing the instance to load() in order
                # * for marshmallow to reuse an existing object rather than recreating one?
                updated_prod = production_schema.load(
                    data, instance=g.prod, partial=True
                )
                db.session.commit()
                return production_schema.dump(updated_prod), 200  #! or 202 (accepted)
            except Exception as e:
                db.session.rollback()
                return {"message": str(e)}, 422
        return {"message": f"Could not find Production with id #{id}"}, 404

    def delete(self, id):
        #! NOT TOUCHED DURING THE MARSHMALLOW REFACTOR
        if g.prod:
            db.session.delete(g.prod)
            db.session.commit()
            return "", 204
        return {"message": f"Could not find Production with id #{id}"}, 404


api.add_resource(ProductionById, "/productions/<int:id>")


class CrewMembers(Resource):
    def get(self):
        try:
            serialized_crew = crew_members_schema.dump(CrewMember.query)
            return serialized_crew, 200
        except Exception as e:
            return str(e), 400

    def post(self):
        try:
            data = (
                request.get_json()
            )  #! to jsonify data a Content-Type headers has to be set on the requester side of things
            crew = crew_member_schema.load(
                data
            )  #! marshmallow: marshmallow first and then model validations will kick in here
            db.session.add(crew)
            db.session.commit()  #! db constraints will kick in here
            return crew_member_schema.dump(crew), 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 422


api.add_resource(CrewMembers, "/crew-members")


class CrewMemberById(Resource):
    def get(self, id):
        if g.crew:
            return crew_member_schema.dump(g.crew), 200
        return {"message": f"Could not find CrewMember with id #{id}"}, 404

    def patch(self, id):
        if g.crew:
            try:
                data = (
                    request.json
                )  #! extract data out of the request (json OR get_json())
                updated_crew = crew_member_schema.load(
                    data, instance=g.crew, partial=True
                )
                db.session.commit()
                return crew_member_schema.dump(updated_crew), 200  #! or 202 (accepted)
            except Exception as e:
                db.session.rollback()
                return {"message": str(e)}, 422
        return {"message": f"Could not find Production with id #{id}"}, 404

    def delete(self, id):
        #! NOT TOUCHED DURING THE MARSHMALLOW REFACTOR
        if g.crew:
            db.session.delete(g.crew)
            db.session.commit()
            return "", 204
        return {"message": f"Could not find Production with id #{id}"}, 404


api.add_resource(CrewMemberById, "/crew-members/<int:id>")


@app.route("/api/v1/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        user = User(username=data.get("username"), email=data.get("email"))
        user.password_hash = data.get("password")
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return user.to_dict(), 201
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 422

@app.route("/api/v1/login", methods=["POST"])
def login():
    try:
        data = request.json #! we have username and password
        user = User.query.filter_by(email=data.get("email")).first() #! returns user object or None
        if user and user.authenticate(data.get("password")):
            session["user_id"] = user.id
            return user.to_dict(), 200
        else:
            return {"message": "Invalid Credentials"}, 422
    except Exception as e:
        return {"message": str(e)}, 422

@app.route("/api/v1/logout", methods=["DELETE"])
def logout():
    try:
        if "user_id" in session:
            del session['user_id'] #! delete the entire key-value pair
        return {}, 204
    except Exception as e:
        raise e

@app.route("/api/v1/me", methods=["GET"])
def me():
    #! check if we have a user_id key inside session
    if "user_id" in session:
        user = db.session.get(User, session.get("user_id"))
        return user.to_dict(), 200
    else:
        return {"message": "Please log in"}, 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)

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
from flask_marshmallow import Marshmallow
from models import db, Production, CrewMember
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, InternalServerError, MethodNotAllowed
from marshmallow import validates, ValidationError, fields, validate
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
# flask-marshmallow connection to app
ma = Marshmallow(app)


#! ==================
#! Marshmallow Schemas
class CrewMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # name of model
        model = CrewMember
        # avoid recreating objects on updates, only applies to deserialization (load())
        # in order for this to work, flask-marshmallow (is specific to this wrapper)
        # needs to know how an instance even looks like, note how we invoked load() on line 222
        load_instance = True
        #  if you set to True, Marshmallow will preserve the order of fields as defined in the schema.
        ordered = True

    #! Setup some app-level (aka no DB involved) validations
    # * See more here https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#module-marshmallow.validate
    name = fields.String(required=True)
    role = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=1000,
            error="Role should be at least 3 chars long and 1000 chars max"
        )
    )
    production_id = fields.Integer(required=True)
    production = fields.Nested("ProductionSchema", exclude=("crew_members",))
    #! Create hyperlinks for easy navigation of your api
    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("crewmemberbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("crewmembers"),
        }
    )

    #! Example of custom validation with marshmallow
    #! (DANGER -> VERY similar to the syntax in the models)
    @validates("name")
    def validate_word_count(self, name):
        words = name.split()
        if len(words) < 2:
            raise ValidationError("Name must contain at least two words")


#! Create schema for a single crew_member
crew_member_schema = CrewMemberSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
crew_members_schema = CrewMemberSchema(many=True)


class ProductionSchema(ma.SQLAlchemyAutoSchema):
    #! The notes are the same as above in CrewMemberSchema ^^^
    class Meta:
        model = Production
        load_instance = True

    crew_members = fields.Nested(
        "CrewMemberSchema",
        only=("id", "name", "role"),
        exclude=("production",),
        many=True,
    )
    title = fields.String(required=True, validate=validate.Length(min=2, max=50))
    director = fields.String(required=True, validate=validate.Length(min=2, max=50))
    description = fields.String(
        required=True, validate=validate.Length(min=30, max=500)
    )
    genre = fields.String(required=True, validate=validate.Length(min=2, max=50))
    image = fields.String(
        required=True,
        validate=validate.Regexp(
            r".*\.(jpeg|png|jpg)", error="File URI must be in JPEG, JPG, or PNG format"
        ),
    )
    budget = fields.Float(
        required=True, validate=validate.Range(min=0.99, max=500000000)
    )

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("productionbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("productions"),
            # "crewmembers": ma.URLFor("crewmembers"),
        }
    )


#! Create schema for a single crew_member
production_schema = ProductionSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
productions_schema = ProductionSchema(many=True, exclude=("crew_members",))

#! ==================
#! GENERAL ROUTE CONCERNS
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

# @app.after_request
# def after_request():
#     #! calculate current time
#     #! subtrack current from g.original_time
#     #! add a response headers to point to the total time elapsed
#     pass

#!======================
#! API ROUTES
@app.route("/")
def welcome():
    return render_template("home.html", name="Matteo")
class Productions(Resource):
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
            # return make_response(jsonify(serialized_prods), 200)
            return serialized_prods, 200
        except Exception as e:
            return str(e), 400

    def post(self):
        try:
            data = request.get_json() #! to jsonify data a Content-Type headers has to be set on the requester side of things
            # prod = Production(**data) #! Pre-marshmallow: model validations will kick in here
            prod = production_schema.load(
                data
            )  #! marshmallow: marshmallow first and then model validations will kick in here
            db.session.add(prod)
            db.session.commit() #! db constraints will kick in here
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
                data = request.json #! extract data out of the request (json OR get_json())
                # * partial = True allows partial updates, meaning only the provided fields
                # * in the JSON data will be updated, and the rest will remain unchanged.
                # * Remember what we said about passing the instance to load() in order
                # * for marshmallow to reuse an existing object rather than recreating one?
                updated_prod = production_schema.load(data, instance=g.prod, partial=True)
                db.session.commit()
                return production_schema.dump(updated_prod), 200 #! or 202 (accepted)
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
if __name__ == "__main__":
    app.run(port=5555, debug=True)

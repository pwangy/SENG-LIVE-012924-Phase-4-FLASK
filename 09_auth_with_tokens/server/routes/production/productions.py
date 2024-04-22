from .. import request, Resource, login_required, Production, db, production_schema, productions_schema


class Productions(Resource):

    # @login_required
    def get(self):
        try:
            serialized_prods = productions_schema.dump(Production.query)
            return serialized_prods, 200
        except Exception as e:
            return str(e), 400

    # @login_required
    def post(self):
        try:
            data = (
                request.get_json()
            )  #! to jsonify data a Content-Type headers has to be set on the requester side of things
            prod = production_schema.load(
                data
            )  #! marshmallow: marshmallow first and then model validations will kick in here
            db.session.add(prod)
            db.session.commit()  #! db constraints will kick in here
            return production_schema.dump(prod), 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 422

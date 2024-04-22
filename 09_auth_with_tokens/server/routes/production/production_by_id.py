from .. import (
    request,
    g,
    Resource,
    db,
    production_schema
)

class ProductionById(Resource):
    def get(self, id):
        if g.prod:
            return production_schema.dump(g.prod), 200
        return {"message": f"Could not find Production with id #{id}"}, 404

    # @login_required
    def patch(self, id):
        if g.prod:
            try:
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
        if g.prod:
            db.session.delete(g.prod)
            db.session.commit()
            return "", 204
        return {"message": f"Could not find Production with id #{id}"}, 404

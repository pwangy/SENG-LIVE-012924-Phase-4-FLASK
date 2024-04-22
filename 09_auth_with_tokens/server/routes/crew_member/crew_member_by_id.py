from .. import (
    request,
    Resource,
    db,
    g,
    crew_member_schema,
)

class CrewMemberById(Resource):
    def get(self, id):
        if g.crew:
            return crew_member_schema.dump(g.crew), 200
        return {"message": f"Could not find CrewMember with id #{id}"}, 404

    # @login_required
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

    # @login_required
    def delete(self, id):
        if g.crew:
            db.session.delete(g.crew)
            db.session.commit()
            return "", 204
        return {"message": f"Could not find Production with id #{id}"}, 404

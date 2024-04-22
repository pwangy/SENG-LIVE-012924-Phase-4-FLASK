from .. import (
    request,
    Resource,
    db,
    crew_members_schema,
    crew_member_schema,
    CrewMember,
)


class CrewMembers(Resource):
    def get(self):
        try:
            serialized_crew = crew_members_schema.dump(CrewMember.query)
            return serialized_crew, 200
        except Exception as e:
            return str(e), 400

    # @login_required
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

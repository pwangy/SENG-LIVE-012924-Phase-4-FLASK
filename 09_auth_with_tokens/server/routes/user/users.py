from .. import (
    request,
    Resource,
    db,
    user_schema
)

class Users(Resource):
    def post(self):
        try:
            data = request.json
            user = user_schema.load(data)
            db.session.add(user)
            db.session.commit()
            # session["user_id"] = user.id
            return user_schema.dump(user), 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 422

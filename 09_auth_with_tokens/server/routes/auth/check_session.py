from .. import (
    Resource,
    db,
    User,
    user_schema,
    jwt_required,
    current_user
)
class CheckSession(Resource):
    @jwt_required()
    def get(self):    
        #! check if we have a user_id key inside session
        if current_user:
            # user = db.session.get(User, session.get("user_id"))
            return user_schema.dump(current_user), 200
        else:
            return {"message": "Please log in"}, 401
        # import ipdb; ipdb.set_trace()
from .. import (
    Resource,
    db,
    User,
    user_schema
)
class CheckSession(Resource):
    def get(self):    
        #! check if we have a user_id key inside session
        # if "user_id" in session:
        #     user = db.session.get(User, session.get("user_id"))
        #     return user_schema.dump(user), 200
        # else:
        #     return {"message": "Please log in"}, 400
        import ipdb; ipdb.set_trace()
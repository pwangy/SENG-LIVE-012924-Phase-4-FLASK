from .. import (
    request,
    Resource,
    User,
    user_schema,
)

class Login(Resource):
    def post(self):
        try:
            data = request.json #! we have username and password
            user = User.query.filter_by(email=data.get("email")).first() #! returns user object or None
            if user and user.authenticate(data.get("password")):
                # session["user_id"] = user.id
                import ipdb; ipdb.set_trace()
                return user_schema.dump(user), 200
            else:
                return {"message": "Invalid Credentials"}, 422
        except Exception as e:
            return {"message": str(e)}, 422

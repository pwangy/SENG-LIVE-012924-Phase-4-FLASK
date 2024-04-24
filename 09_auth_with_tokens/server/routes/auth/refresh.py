from .. import (
    Resource,
    db,
    User,
    user_schema,
    jwt_required,
    current_user,
    create_access_token,
    make_response,
    set_access_cookies
)


class Refresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        new_access_token = create_access_token(identity=current_user.id, fresh=False)
        response = make_response(user_schema.dump(current_user), 200)
        set_access_cookies(response, new_access_token)
        return response

from functools import wraps
from flask import request, g, render_template
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from schemas.crew_member_schema import crew_member_schema, crew_members_schema
from schemas.production_schema import production_schema, productions_schema
from schemas.user_schema import user_schema, users_schema
from models.production import Production
from models.crew_member import CrewMember
from models.user import User
from app_config import db, app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    unset_refresh_cookies,
    unset_access_cookies,
    current_user,
    get_jwt,
    verify_jwt_in_request,
    decode_token,
)

#! ==================
#! GENERAL ROUTE CONCERNS
@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404


@app.before_request
def before_request():
    path_dict = {"productionbyid": Production, "crewmemberbyid": CrewMember}
    if request.endpoint in path_dict:
        id = request.view_args.get("id")
        record = db.session.get(path_dict.get(request.endpoint), id)
        key_name = "prod" if request.endpoint == "productionbyid" else "crew"
        setattr(g, key_name, record)


#!======================
#! API ROUTES
@app.route("/")
def welcome():
    return render_template("home.html", name="Matteo")


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # if "user_id" not in session:
        #     return {"message": "Access Denied, please log in!"}, 422
        return func(*args, **kwargs)

    return decorated_function

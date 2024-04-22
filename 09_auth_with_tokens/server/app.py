#!/usr/bin/env python3

#! Internal imports
from app_config import app, api
from routes.production.productions import Productions
from routes.production.production_by_id import ProductionById
from routes.crew_member.crew_members import CrewMembers
from routes.crew_member.crew_member_by_id import CrewMemberById
from routes.user.users import Users
from routes.auth.login import Login
from routes.auth.logout import Logout
from routes.auth.check_session import CheckSession


api.add_resource(Productions, "/productions")
api.add_resource(ProductionById, "/productions/<int:id>")
api.add_resource(CrewMembers, "/crew-members")
api.add_resource(CrewMemberById, "/crew-members/<int:id>")
api.add_resource(Users, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/me")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

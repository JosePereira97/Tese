import logging

from flask import make_response, g, abort, request
from flask_restful import Resource, wraps
from database.app_BD import Users
from app import db

from database.app_BD import Users

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id" not in g.cookie:
            logging.warning("No authorization provided!")
            abort(401)

        g.user = Users.query.get(g.cookie["id"])

        if not g.user:
            response = make_response("", 401)
            response.set_cookie("user", "")
            return response

        return func(*args, **kwargs)

    return wrapper


class AuthenticatedView(Resource):
    method_decorators = [require_login]

from flask import Blueprint
from flask_restful import Api

from app.resources.user import UserResource

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

# Add user resource endpoints
user_api.add_resource(UserResource, '/users', '/users/<int:user_id>')

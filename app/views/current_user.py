from flask import Blueprint
from flask_restful import Api

from app.resources.current_user import CurrentUserResource

current_user_bp = Blueprint('current-user', __name__)
current_user_api = Api(current_user_bp)

# Add user resource endpoints
current_user_api.add_resource(CurrentUserResource, '/current-user')

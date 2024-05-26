from flask import Blueprint
from flask_restful import Api

from app.resources.login import LoginResource

login_bp = Blueprint('login', __name__)
login_api = Api(login_bp)

login_api.add_resource(LoginResource, '/login')

from flask import Blueprint
from flask_restful import Api
from app.resources.thread import ThreadResource

thread_bp = Blueprint('thread', __name__)
thread_api = Api(thread_bp)

# Add thread resource endpoints
thread_api.add_resource(ThreadResource, '/threads', '/threads/<int:thread_id>')

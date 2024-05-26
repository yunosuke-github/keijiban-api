from flask import Blueprint
from flask_restful import Api
from app.resources.comment import CommentResource

comment_bp = Blueprint('comment', __name__)
comment_api = Api(comment_bp)

comment_api.add_resource(CommentResource, '/comments', '/comments/<int:comment_id>')

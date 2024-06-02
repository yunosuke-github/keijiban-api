from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app import db
from app.models.comment import Comment
from app.schemas.comment import CommentSchema

comment_schema = CommentSchema()


class CommentReactionResource(Resource):

    @jwt_required()
    def post(self, comment_id, action):
        comment = Comment.query.get(comment_id)
        if comment is None:
            return {'message': 'Comment not found'}, 404

        if action == 'like':
            comment.likes += 1
        elif action == 'dislike':
            comment.dislikes += 1
        else:
            return {'message': 'Invalid action'}, 400

        db.session.commit()
        return comment_schema.dump(comment)

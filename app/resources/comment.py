from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.models.comment import Comment
from app.schemas.comment import CommentSchema

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


class CommentResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            comment_data = comment_schema.load(data)
            comment = Comment(user_id=user_id, **comment_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201

    @jwt_required()
    def get(self, comment_id=None):
        if comment_id:
            comment = Comment.query.get(comment_id)
            if comment is None:
                return {'message': 'Comment not found'}, 404
            return comment_schema.dump(comment)

        # クエリパラメータの取得
        thread_id = request.args.get('thread_id', type=int)
        limit = request.args.get('limit', type=int)
        sort_field = request.args.get('sort_by', 'created_at')  # デフォルトはcreated_atでソート
        order = request.args.get('order', 'desc')  # デフォルトは降順

        if sort_field not in ['created_at', 'views', 'like', 'dislike']:
            return {'message': 'Invalid sort field'}, 400
        if order not in ['asc', 'desc']:
            return {'message': 'Invalid order'}, 400

        # ソート順に応じてクエリを変更
        if order == 'asc':
            order_by = Comment.__table__.c[sort_field].asc()
        else:
            order_by = Comment.__table__.c[sort_field].desc()

        # クエリの構築
        query = Comment.query
        if thread_id is not None:
            query = query.filter_by(thread_id=thread_id)

        query = query.order_by(order_by)

        if limit is not None:
            query = query.limit(limit)

        comments = query.all()
        return comments_schema.dump(comments)

    @jwt_required()
    def put(self, comment_id):
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'message': 'Comment not found'}, 404

        data = request.get_json()
        user_id = get_jwt_identity()

        # Separate fields that any user can update
        updateable_fields = ['likes', 'dislikes']
        protected_fields = ['content']

        # Load updateable fields data
        try:
            updateable_data = {key: data[key] for key in updateable_fields if key in data}
            if len(updateable_data) > 0:
                comment_data = comment_schema.load(updateable_data, partial=True)
                # Apply updates to updateable fields
                for key, value in comment_data.items():
                    setattr(comment, key, value)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        # If the current user is the comment owner, allow updating protected fields
        if comment.user_id == user_id:
            try:
                protected_data = {key: data[key] for key in protected_fields if key in data}
                protected_comment_data = comment_schema.load(protected_data, partial=True)
                for key, value in protected_comment_data.items():
                    setattr(comment, key, value)
            except ValidationError as err:
                return {"errors": err.messages}, 422

        db.session.commit()
        return comment_schema.dump(comment)

    @jwt_required()
    def delete(self, comment_id):
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'message': 'Comment not found'}, 404

        user_id = get_jwt_identity()
        if comment.user_id != user_id:
            return {'message': 'Permission denied'}, 403

        db.session.delete(comment)
        db.session.commit()
        return '', 204

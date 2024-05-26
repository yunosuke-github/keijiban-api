from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.models.comment import Comment
from app.models.thread import Thread
from app.schemas.thread import ThreadSchema

thread_schema = ThreadSchema()
threads_schema = ThreadSchema(many=True)


class ThreadResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            thread_data = thread_schema.load(data)
            thread = Thread(user_id=user_id, **thread_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        db.session.add(thread)
        db.session.commit()
        return thread_schema.dump(thread), 201

    @jwt_required()
    def get(self, thread_id=None):
        if thread_id:
            thread = Thread.query.get(thread_id)
            if thread is None or thread.deleted:
                return {'message': 'Thread not found'}, 404
            # id指定された場合はviewsをインクリメント
            thread.views += 1
            db.session.commit()
            thread_data = thread_schema.dump(thread)
            # コメント数を追加
            thread_data['comment_count'] = Comment.query.filter_by(thread_id=thread_id).count()
            return thread_data

        sort_field = request.args.get('sort_by', 'created_at')  # デフォルトはcreated_atでソート
        order = request.args.get('order', 'desc')  # デフォルトは降順
        search_query = request.args.get('query', type=str)
        category = request.args.get('category', type=str)
        limit = request.args.get('limit', type=int)  # デフォルトはNone、すべてのスレッドを取得
        user_id = request.args.get('user_id', type=int)  # user_idでフィルタリング

        if sort_field not in ['created_at', 'views', 'name', 'category']:
            return {'message': 'Invalid sort field'}, 400
        if order not in ['asc', 'desc']:
            return {'message': 'Invalid order'}, 400

        # ソート順に応じてクエリを変更
        if order == 'asc':
            order_by = Thread.__table__.c[sort_field].asc()
        else:
            order_by = Thread.__table__.c[sort_field].desc()

        query = Thread.query.order_by(order_by)

        # 削除済みは除く
        query = query.filter_by(deleted=False)

        if user_id:
            query = query.filter_by(user_id=user_id)
        if category:
            query = query.filter_by(category=category)
        if search_query:
            query = query.filter(Thread.name.ilike(f"%{search_query}%"))
        if limit:
            query = query.limit(limit)

        threads = query.all()
        threads_data = threads_schema.dump(threads)

        # 各スレッドにコメント数を追加
        for thread_data in threads_data:
            thread_data['comment_count'] = Comment.query.filter_by(thread_id=thread_data['id']).count()

        return threads_data

    @jwt_required()
    def put(self, thread_id):
        thread = Thread.query.get(thread_id)
        if not thread:
            return {'message': 'Thread not found'}, 404

        user_id = get_jwt_identity()
        if thread.user_id != user_id:
            return {'message': 'Permission denied'}, 403

        data = request.get_json()
        try:
            thread_data = thread_schema.load(data, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        for key, value in thread_data.items():
            setattr(thread, key, value)

        db.session.commit()
        return thread_schema.dump(thread)

    @jwt_required()
    def delete(self, thread_id):
        thread = Thread.query.get(thread_id)
        if not thread:
            return {'message': 'Thread not found'}, 404

        user_id = get_jwt_identity()
        if thread.user_id != user_id:
            return {'message': 'Permission denied'}, 403

        thread.deleted = True
        db.session.commit()
        return '', 204

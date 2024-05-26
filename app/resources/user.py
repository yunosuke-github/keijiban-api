from datetime import datetime

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from app import db
from app.models.user import User
from app.schemas.user import UserSchema

user_schema = UserSchema(partial=True)  # Enable partial updates
users_schema = UserSchema(many=True)


class UserResource(Resource):

    @jwt_required()
    def get(self, user_id):
        i = get_jwt_identity()
        if user_id != i:
            return {'message': 'Permission denied'}, 403

        user = User.query.get(user_id)
        if user is None:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user)

    def post(self):
        data = request.get_json()
        try:
            user = User(**user_schema.load(data))
            user.created_at = datetime.now()
            user.updated_at = datetime.now()
        except ValidationError as err:
            return {"errors": err.messages}, 422

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    @jwt_required()
    def put(self, user_id):
        i = get_jwt_identity()
        if user_id != i:
            return {'message': 'Permission denied'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        data = request.get_json()

        # Load data with partial schema
        try:
            user_data = user_schema.load(data, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        # Update only the fields present in the request body
        for key, value in user_data.items():
            setattr(user, key, value)

        db.session.commit()
        return user_schema.dump(user)

    @jwt_required()
    def delete(self, user_id):
        i = get_jwt_identity()
        if user_id != i:
            return {'message': 'Permission denied'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return '', 204

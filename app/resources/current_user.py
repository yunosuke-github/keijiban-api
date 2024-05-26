from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.models.user import User
from app.schemas.user import UserSchema

user_schema = UserSchema(partial=True)


class CurrentUserResource(Resource):

    @jwt_required()
    def get(self):
        i = get_jwt_identity()
        user = User.query.get(i)
        if user is None:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user)

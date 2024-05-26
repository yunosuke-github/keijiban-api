import logging
from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from app.middleware import log_request_response
from config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # エンジンのロギング設定
    if app.config.get('SQLALCHEMY_ECHO', False):
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.INFO)

    # app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # セキュアなキーを設定してください
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)

    from app.views.user import user_bp
    from app.views.current_user import current_user_bp
    from app.views.login import login_bp
    from app.views.thread import thread_bp
    from app.views.comment import comment_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(current_user_bp, url_prefix='/api')
    app.register_blueprint(login_bp, url_prefix='/api')
    app.register_blueprint(thread_bp, url_prefix='/api')
    app.register_blueprint(comment_bp, url_prefix='/api')

    log_request_response(app)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({'errors': e.messages}), 422

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(e)
        return jsonify({'message': 'Internal Server Error'}), 500

    return app

import logging

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from app.middleware import log_request_response
from config import Config

db = SQLAlchemy()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)

    from app.views.user import user_bp

    app.register_blueprint(user_bp, url_prefix='/api')

    log_request_response(app)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({'errors': e.messages}), 422

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(e)
        return jsonify({'message': 'Internal Server Error'}), 500

    return app

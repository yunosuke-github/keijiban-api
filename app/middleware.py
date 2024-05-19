import json
import logging

from flask import request, g

from app.utils import generate_request_id

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_request_response(app):
    @app.before_request
    def log_request():
        request_id = generate_request_id()
        g.request_id = request_id
        if request.method in ['POST', 'PUT']:
            logging.info(f"Request: {request.method} {request.url} Pyload: {request.get_json()}")
        else:
            logging.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response(response):
        logging.info(f"Response: {response.status} Pyload: {json.loads(response.get_data(as_text=True))}")
        return response

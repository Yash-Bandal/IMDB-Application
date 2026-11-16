import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException


logger = logging.getLogger("imdb_api")


class ApiError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify(error=str(error)), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        if isinstance(error, HTTPException):
            return error

        logger.exception("Unhandled application error")
        return jsonify(error="Internal server error"), 500

import logging
import os

import jwt
from flask import Flask, g, jsonify, request
from flask_cors import CORS

from imdb_api.config import cors_origins, required_settings, setting
from imdb_api.controllers.auth_controller import auth_blueprint
from imdb_api.controllers.genres_controller import genres_blueprint
from imdb_api.controllers.health_controller import health_blueprint
from imdb_api.controllers.movies_controller import movies_blueprint
from imdb_api.controllers.people_controller import create_people_blueprint
from imdb_api.controllers.posters_controller import posters_blueprint
from imdb_api.controllers.reviews_controller import reviews_blueprint
from imdb_api.errors import ApiError, register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    CORS(
        app,
        resources={r"/api/*": {"origins": cors_origins()}},
        allow_headers="*",
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )
    register_error_handlers(app)

    @app.before_request
    def authenticate_request():
        print("REQUEST RECEIVED:", request.method, request.path)
        print("JWT SECRET EXISTS:", bool(setting("JWT_SECRET_KEY")))
        print("JWT ISSUER:", setting("JWT_ISSUER"))

        if request.method == "OPTIONS" or request.path == "/api/auth/login":
            return None

        if request.path.startswith("/api/"):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify(error="Authentication token is required."), 401

            token = auth_header.split(" ", 1)[1].strip()
            try:
                g.current_user = jwt.decode(
                    token,
                    setting("JWT_SECRET_KEY"),
                    algorithms=["HS256"],
                    issuer=setting("JWT_ISSUER"),
                    audience=setting("JWT_AUDIENCE"),
                )
            except jwt.ExpiredSignatureError:
                return jsonify(error="Token expired."), 401
            except jwt.InvalidTokenError:
                return jsonify(error="Invalid token."), 401

        return None

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(create_people_blueprint("actors", "Foundation.Actors", "Actor"))
    app.register_blueprint(create_people_blueprint("producers", "Foundation.Producers", "Producer"))
    app.register_blueprint(genres_blueprint)
    app.register_blueprint(movies_blueprint)
    app.register_blueprint(posters_blueprint)
    app.register_blueprint(reviews_blueprint)
    app.register_blueprint(health_blueprint)
    return app


__all__ = ["ApiError", "create_app", "required_settings", "setting"]

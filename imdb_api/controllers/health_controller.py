from flask import Blueprint


health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/")
def root():
    return "IMDB API is running", 200


@health_blueprint.get("/health")
def health():
    return "healthy", 200, {"Content-Type": "text/plain"}

from flask import Blueprint, jsonify, request

from imdb_api.errors import ApiError
from imdb_api.services import movies_service
from imdb_api.utils.validation import body_json


movies_blueprint = Blueprint("movies", __name__)


@movies_blueprint.get("/api/movies")
def get_movies():
    year = request.args.get("year", type=int)
    if request.args.get("year") is not None and (year is None or year <= 0):
        raise ApiError("Year must be greater than zero.")
    return jsonify(data=movies_service.list_movies(year))


@movies_blueprint.get("/api/movies/<int:movie_id>")
def get_movie(movie_id):
    return jsonify(data=movies_service.get_movie(movie_id))


@movies_blueprint.post("/api/movies")
def add_movie():
    movie_id = movies_service.create_movie(body_json())
    return jsonify(id=movie_id), 201


@movies_blueprint.put("/api/movies/<int:movie_id>")
def update_movie(movie_id):
    movies_service.update_movie(movie_id, body_json())
    return "", 200


@movies_blueprint.delete("/api/movies/<int:movie_id>")
def delete_movie(movie_id):
    movies_service.delete_movie(movie_id)
    return "", 204
